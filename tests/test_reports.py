from app.modules.reports import create_report
def test_report(tmp_path): assert create_report(str(tmp_path/'r.pptx'))['success']
