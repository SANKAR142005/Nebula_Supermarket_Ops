
## 📌 Project Description

SmartStore AI is an intelligent supermarket operations assistant that allows store owners and customers to interact with supermarket services through a Telegram bot.

The system combines an AI-powered conversational interface with a database-driven backend to handle common supermarket operations such as product search, inventory management, shopping and billing, customer management, credit/Khata tracking, payments, sales analytics, purchase suggestions, and automatic PDF invoice generation.

Instead of manually managing each operation through separate systems, the user can communicate with the Telegram bot using natural language.

### Example

User: I want to buy 2 Rice 5kg

Bot: Rice 5kg is available.
     Quantity: 2
     Price: ₹320 each
     Total: ₹672 including GST
     Do you want to confirm the purchase?

User: Yes, confirm

Bot: Payment method?

User: Cash

Bot: Purchase completed successfully.
     Your invoice is attached 

# ✨ Features
  
  <img width="1200" height="1000" alt="Features" src="https://github.com/user-attachments/assets/eb7bfcf1-4f75-4be2-89b7-dbd113c1428a" />

# 🏗️ System Architecture

The application follows a modular architecture where the Telegram bot acts as the user interface, the AI assistant interprets natural-language requests, and the business operation modules perform the actual database operations.

                    ┌─────────────────────┐
                    │       User          │
                    │  Natural Language   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Telegram Bot     │
                    │  User Interface     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    AI Assistant     │
                    │ Intent & Tool Call  │
                    └──────────┬──────────┘
                               │
                               ▼
              ┌─────────────────────────────────┐
              │      Business Operations        │
              │                                 │
              │ Product │ Inventory │ Billing   │
              │ Customer│ Credit    │ Analytics │
              │ Payment │ Purchasing│ Health    │
              └───────────────┬─────────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │      Database       │
                    │       SQLite        │
                    └─────────────────────┘
                              │
                ┌─────────────┴─────────────┐
                ▼                           ▼
      ┌──────────────────┐        ┌──────────────────┐
      │  PDF Invoice     │        │ Reports &        │
      │  Generation      │        │ Analytics        │
      └──────────────────┘        └──────────────────┘

# 🔄 Purchase Workflow

The main shopping workflow is:

                            User
                              │
                              ▼
                            " I want to buy 2 Rice 5kg "
                              │
                              ▼
                            AI Assistant
                              │
                              ▼
                            Product Search
                              │
                              ▼
                            Check Product & Stock
                              │
                              ▼
                            Create Shopping Sale
                              │
                              ▼
                            Add Product + Quantity
                              │
                              ▼
                            Calculate Bill
                              │
                              ▼
                            Ask User for Confirmation
                              │
                              ▼
                            User Confirms
                              │
                              ▼
                            Select Payment Method
                              │
                              ▼
                            Complete Sale
                              │
                              ▼
                            Update Inventory
                              │
                              ▼
                            Generate PDF Invoice
                              │
                              ▼
                            Send Invoice through Telegram

# ⚙️ Technologies Used

- Python – Backend development
- OpenAI / OpenRouter – AI-powered natural language processing
- python-telegram-bot – Telegram bot communication
- SQLAlchemy – Database ORM
- SQLite – Application database
- ReportLab – PDF invoice generation
- Python-PPTX – Report generation
- Matplotlib – Data visualization
- python-dotenv – Environment configuration

# 🛠️ Project Setup
1. Clone the Repository
   ```bash
    git clone https://github.com/SANKAR142005/Nebula_Supermarket_Ops.git
    cd Nebula_Supermarket_Ops
   ```
2. Create a Virtual Environment
   ```bash
    python -m venv venv
    venv\Scripts\activate
   ```
4. Install Dependencies
   ```bash
    pip install -r requirements.txt
    ```
5. 🔐 Environment Configuration
Create a .env file in the project root.
  ```bash
  OPENAI_API_KEY=your_api_key_here
  OPENAI_BASE_URL=https://openrouter.ai/api/v1
  AI_MODEL=openai/gpt-4o-mini
  TELEGRAM_BOT_TOKEN=your_telegram_bot_token
 ```
6. 🗄️ Database Initialization
Initialize the database and load the demo products and customers:
    ```bash
    python main.py
    ```
The database file will be created locally: smartstore.db

7. ▶️ Start the Telegram Bot
 ```bash
   python -m app.messenger.telegram_service
 ```
You should see:
```bash
   Starting SmartStore AI Telegram Bot...
   Bot is running.
```
Open Telegram and send /start.
Open your Telegram bot and send:
/start
        <img width="702" height="1600" alt="image" src="https://github.com/user-attachments/assets/f7e5ea3f-bfb8-4263-9785-ecaa718f18de" />
