from app.operations.credit import credit_summary
def test_credit(): assert credit_summary()['success']
