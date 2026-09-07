from app.operations.catalog import find_items
def test_catalog(): assert find_items('Rice')['success']
