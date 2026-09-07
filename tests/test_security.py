from app.modules.rules import valid_payment
def test_payment_rule(): assert valid_payment('upi'); assert not valid_payment('bitcoin')
