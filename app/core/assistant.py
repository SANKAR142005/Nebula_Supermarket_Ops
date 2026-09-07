import json
import os

from dotenv import load_dotenv
from app.core.actions import ACTIONS, run_action

load_dotenv()


SYSTEM = """
You are SmartStore AI, an intelligent supermarket operations assistant.

You help with:
- Product search
- Stock checking
- Customer management
- Shopping/billing
- Payments
- Credit/khata
- Sales
- Inventory
- Reports and analytics

IMPORTANT RULES:

1. NEVER invent product names, prices, stock, totals, customers or sales data.
   Always use the available business tools for real data.

2. When the user wants to BUY something:
   - First identify the product using find_items.
   - If the product is clear, create a sale using open_sale.
   - Add the requested quantity using add_sale_line.
   - Show the bill/total to the customer.
   - DO NOT complete the sale yet.
   - Ask the customer to confirm the purchase.

3. A purchase must NOT be completed until the customer explicitly confirms.
   Examples of confirmation:
   "yes", "confirm", "confirm purchase", "go ahead", "proceed".

4. After confirmation:
   - If payment method is already provided, use it.
   - Otherwise ask for payment method.
   - Supported payment methods are cash, upi, card and credit.

5. After complete_sale succeeds:
   - Immediately generate the PDF invoice using create_receipt.
   - Tell the user that the invoice has been generated.
   - The Telegram application will send the PDF automatically.

6. Maintain the sale_id from previous tool calls.
   If the user says "yes", "confirm", "cash", "upi", etc., use the existing sale.

7. If the user asks "I want to buy 2 Rice 5kg", interpret:
   product = Rice 5kg
   quantity = 2

8. If a product cannot be uniquely identified, ask the user for clarification.

9. Do not repeatedly call the same tool with the same arguments.

10. Keep responses short and useful.

11. Never complete a purchase merely because the user said "I want to buy".
   Explicit confirmation is required.

12. When a tool returns an error, explain the error to the user instead of repeatedly
   calling the same tool.

13. The operation limit is 10 tool calls per user message.
"""


try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


class RetailAssistant:

    def __init__(self):
        self.history = []

        key = os.getenv("OPENAI_API_KEY")

        self.client = (
            OpenAI(
                api_key=key,
                base_url=os.getenv(
                    "OPENAI_BASE_URL",
                    "https://openrouter.ai/api/v1"
                ),
            )
            if OpenAI and key
            else None
        )

        self.model = os.getenv(
            "AI_MODEL",
            "openai/gpt-4o-mini"
        )

    def _tool_specs(self):

        specs = {
            "find_items": {
                "description": "Search the product catalog by product name, SKU or keyword.",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Product name, SKU or search keyword."
                    }
                },
                "required": ["query"]
            },

            "add_item": {
                "description": "Add a new product to inventory.",
                "properties": {
                    "name": {"type": "string"},
                    "sku": {"type": "string"},
                    "sell_price": {"type": "number"},
                    "quantity": {"type": "integer"},
                    "gst_rate": {"type": "number"}
                },
                "required": ["name", "sku", "sell_price", "quantity"]
            },

            "receive_inventory": {
                "description": "Increase stock for an existing product.",
                "properties": {
                    "product_id": {"type": "integer"},
                    "quantity": {"type": "integer"}
                },
                "required": ["product_id", "quantity"]
            },

            "stock_status": {
                "description": "Get stock information for a product.",
                "properties": {
                    "product_id": {"type": "integer"}
                },
                "required": ["product_id"]
            },

            "low_inventory": {
                "description": "Find products whose inventory is low.",
                "properties": {},
                "required": []
            },

            "create_client": {
                "description": "Create a customer.",
                "properties": {
                    "name": {"type": "string"},
                    "phone": {"type": "string"}
                },
                "required": ["name"]
            },

            "find_clients": {
                "description": "Search customers.",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            },

            "client_details": {
                "description": "Get details of a customer.",
                "properties": {
                    "client_id": {"type": "integer"}
                },
                "required": ["client_id"]
            },

            "client_balance": {
                "description": "Get customer's outstanding credit balance.",
                "properties": {
                    "client_id": {"type": "integer"}
                },
                "required": ["client_id"]
            },

            "record_credit_payment": {
                "description": "Record a payment against customer credit.",
                "properties": {
                    "client_id": {"type": "integer"},
                    "amount": {"type": "number"}
                },
                "required": ["client_id", "amount"]
            },

            "credit_summary": {
                "description": "Get overall customer credit summary.",
                "properties": {},
                "required": []
            },

            "open_sale": {
                "description": "Create a new shopping sale/cart.",
                "properties": {
                    "client_id": {
                        "type": ["integer", "null"],
                        "description": "Customer ID if known, otherwise null."
                    }
                },
                "required": []
            },

            "add_sale_line": {
                "description": "Add a product and quantity to an open sale.",
                "properties": {
                    "sale_id": {"type": "integer"},
                    "product_id": {"type": "integer"},
                    "quantity": {"type": "integer"}
                },
                "required": ["sale_id", "product_id", "quantity"]
            },

            "revise_sale_line": {
                "description": "Change the quantity of an existing sale line.",
                "properties": {
                    "sale_id": {"type": "integer"},
                    "line_id": {"type": "integer"},
                    "quantity": {"type": "integer"}
                },
                "required": ["sale_id", "line_id", "quantity"]
            },

            "sale_details": {
                "description": "Show the current shopping cart/bill.",
                "properties": {
                    "sale_id": {"type": "integer"}
                },
                "required": ["sale_id"]
            },

            "complete_sale": {
                "description": "Complete a confirmed sale using a payment method.",
                "properties": {
                    "sale_id": {"type": "integer"},
                    "payment": {
                        "type": "string",
                        "enum": ["cash", "upi", "card", "credit"]
                    }
                },
                "required": ["sale_id", "payment"]
            },

            "purchase_suggestions": {
                "description": "Suggest products that should be reordered.",
                "properties": {},
                "required": []
            },

            "sales_overview": {
                "description": "Get sales overview.",
                "properties": {},
                "required": []
            },

            "daily_revenue": {
                "description": "Get revenue for a day.",
                "properties": {},
                "required": []
            },

            "profitability": {
                "description": "Get profitability information.",
                "properties": {},
                "required": []
            },

            "health_check": {
                "description": "Check application and database health.",
                "properties": {},
                "required": []
            },

            "save_setting": {
                "description": "Save a store setting.",
                "properties": {
                    "key": {"type": "string"},
                    "value": {"type": "string"}
                },
                "required": ["key", "value"]
            },

            "read_setting": {
                "description": "Read a store setting.",
                "properties": {
                    "key": {"type": "string"}
                },
                "required": ["key"]
            },

            "all_settings": {
                "description": "Get all store settings.",
                "properties": {},
                "required": []
            },

            "remove_setting": {
                "description": "Remove a store setting.",
                "properties": {
                    "key": {"type": "string"}
                },
                "required": ["key"]
            },

            "create_receipt": {
                "description": "Generate a PDF receipt for a completed sale.",
                "properties": {
                    "sale_id": {"type": "integer"},
                    "output": {
                        "type": "string",
                        "description": "PDF output path."
                    }
                },
                "required": ["sale_id"]
            },

            "create_report": {
                "description": "Generate a sales report.",
                "properties": {
                    "output": {"type": "string"}
                },
                "required": []
            }
        }

        tools = []

        for name, config in specs.items():

            if name not in ACTIONS:
                continue

            tools.append({
                "type": "function",
                "function": {
                    "name": name,
                    "description": config["description"],
                    "parameters": {
                        "type": "object",
                        "properties": config["properties"],
                        "required": config["required"],
                        "additionalProperties": False
                    }
                }
            })

        return tools

    def _message_to_dict(self, message):

        if hasattr(message, "model_dump"):
            return message.model_dump(exclude_none=True)

        return {
            "role": message.role,
            "content": message.content,
            "tool_calls": getattr(message, "tool_calls", None)
        }

    def ask(self, text):

        if not self.client:
            return {
                "success": False,
                "message": (
                    "AI provider is not configured. "
                    "Please check OPENAI_API_KEY in your .env file."
                )
            }

        self.history.append({
            "role": "user",
            "content": text
        })

        messages = [
            {
                "role": "system",
                "content": SYSTEM
            }
        ]

        messages.extend(self.history[-30:])

        invoice_file = None

        for _ in range(10):

            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    tools=self._tool_specs(),
                    tool_choice="auto"
                )

            except Exception as exc:

                return {
                    "success": False,
                    "message": f"AI service error: {exc}"
                }

            msg = response.choices[0].message

            tool_calls = getattr(msg, "tool_calls", None)

            if not tool_calls:

                answer = msg.content or "Done."

                self.history.append({
                    "role": "assistant",
                    "content": answer
                })

                result = {
                    "success": True,
                    "message": answer
                }

                if invoice_file:
                    result["invoice_file"] = invoice_file

                return result

            assistant_message = self._message_to_dict(msg)

            messages.append(assistant_message)

            for call in tool_calls:

                name = call.function.name

                try:
                    args = json.loads(
                        call.function.arguments or "{}"
                    )
                except json.JSONDecodeError:

                    result = {
                        "success": False,
                        "message": "Invalid tool arguments."
                    }

                    messages.append({
                        "role": "tool",
                        "tool_call_id": call.id,
                        "content": json.dumps(result)
                    })

                    continue

                result = run_action(
                    name,
                    **args
                )

                # After completing the sale, automatically create invoice.
                if (
                    name == "complete_sale"
                    and result.get("success")
                ):

                    sale_id = result.get("sale_id")

                    if sale_id:

                        receipt_result = run_action(
                            "create_receipt",
                            sale_id=sale_id,
                            output=f"generated/receipt_{sale_id}.pdf"
                        )

                        if receipt_result.get("success"):

                            invoice_file = receipt_result.get("file")

                            result["invoice_generated"] = True
                            result["invoice_file"] = invoice_file

                        else:

                            result["invoice_generated"] = False
                            result["invoice_error"] = (
                                receipt_result.get("message")
                            )

                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": json.dumps(
                        result,
                        default=str
                    )
                })

        return {
            "success": False,
            "message": (
                "I could not complete that operation. "
                "Please try the request again."
            )
        }