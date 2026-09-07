from app.operations.stock import low_inventory
def test_stock(): assert low_inventory()['success']
