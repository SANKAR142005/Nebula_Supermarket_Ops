from app.operations.clients import create_client
def test_client(): assert create_client('Test User','9888888888')['success']
