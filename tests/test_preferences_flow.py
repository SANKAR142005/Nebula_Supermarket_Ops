from app.modules.settings import save_setting,read_setting
def test_preference_flow(): save_setting('default_payment','upi'); assert read_setting('default_payment')['value']=='upi'
