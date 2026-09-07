from app.core.assistant import RetailAssistant
def test_assistant_without_key(): assert RetailAssistant().ask('hello')['success']
