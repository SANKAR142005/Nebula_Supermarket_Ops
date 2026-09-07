from app.modules.settings import save_setting,read_setting
def test_setting(): save_setting('test_key','abc'); assert read_setting('test_key')['value']=='abc'
