# SmartStore AI

A conversational retail operations assistant for inventory, billing, customers, credit, analytics and purchasing.

## Run
1. Create `.env` with `OPENAI_API_KEY` and optionally `TELEGRAM_BOT_TOKEN`.
2. Install dependencies: `pip install -r requirements.txt`
3. Initialize the database: `python main.py`
4. Start the Telegram service: `python -m app.messenger.telegram_service`
