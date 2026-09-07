from app.modules.settings import save_setting
def test_transaction_setting(): assert save_setting('shop_name','SmartStore')['success']
