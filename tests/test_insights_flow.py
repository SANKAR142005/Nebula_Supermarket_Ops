from app.operations.insights import sales_overview
def test_insights(): assert sales_overview()['success']
