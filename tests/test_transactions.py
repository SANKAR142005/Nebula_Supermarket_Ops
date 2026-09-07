from app.operations.transactions import open_sale
def test_open_sale(): assert open_sale()['success']
