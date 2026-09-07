from app.operations.purchasing import purchase_suggestions
def test_purchase(): assert purchase_suggestions()['success']
