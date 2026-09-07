from app.operations.system_health import health_check
def test_health(): assert health_check()['success']
