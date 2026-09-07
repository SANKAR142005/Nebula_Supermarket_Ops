import os

from dotenv import load_dotenv

from app.core.assistant import RetailAssistant
from app.modules.conversation import save_chat


load_dotenv()


def build_bot():

    from telegram import Update
    from telegram.request import HTTPXRequest

    from telegram.ext import (
        Application,
        CommandHandler,
        MessageHandler,
        ContextTypes,
        filters,
    )

    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN is not configured."
        )

    agents = {}

    async def start(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):

        chat_id = update.effective_chat.id

        agents[chat_id] = RetailAssistant()

        await update.message.reply_text(
            "Welcome to SmartStore AI.\n\n"
            "You can ask me about products, stock, "
            "billing, customers and sales.\n\n"
            "Example:\n"
            "I want to buy 2 Rice 5kg"
        )

    async def reset(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):

        chat_id = update.effective_chat.id

        agents.pop(chat_id, None)

        save_chat(
            chat_id,
            []
        )

        await update.message.reply_text(
            "Conversation context cleared."
        )

    async def message(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):

        if not update.message or not update.message.text:
            return

        chat_id = update.effective_chat.id

        agent = agents.setdefault(
            chat_id,
            RetailAssistant()
        )

        # Tell user that the assistant is processing.
        await update.message.chat.send_action(
            action="typing"
        )

        result = agent.ask(
            update.message.text
        )

        message_text = result.get(
            "message",
            "I could not process that request."
        )

        await update.message.reply_text(
            message_text
        )

        # Send generated PDF invoice automatically.
        invoice_file = result.get(
            "invoice_file"
        )

        if invoice_file and os.path.exists(invoice_file):

            with open(
                invoice_file,
                "rb"
            ) as document:

                await update.message.reply_document(
                    document=document,
                    filename=os.path.basename(
                        invoice_file
                    ),
                    caption="🧾 Your invoice is attached."
                )

    # Explicit Telegram network configuration.
    request = HTTPXRequest(
        connect_timeout=60.0,
        read_timeout=60.0,
        write_timeout=60.0,
        pool_timeout=60.0,
    )

    app = (
        Application.builder()
        .token(token)
        .request(request)
        .build()
    )

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
        CommandHandler(
            "reset",
            reset
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            message
        )
    )

    return app


if __name__ == "__main__":

    print(
        "Starting SmartStore AI Telegram Bot..."
    )

    app = build_bot()

    print(
        "Bot is running. Open Telegram and send /start."
    )

    app.run_polling()