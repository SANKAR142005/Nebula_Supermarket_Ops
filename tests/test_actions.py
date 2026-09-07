from app.core.actions import run_action
def test_unknown_action(): assert not run_action('missing')['success']
