from app.operations.transactions import open_sale,add_sale_line,complete_sale
def test_flow():
 s=open_sale(); assert s['success']; assert add_sale_line(s['sale_id'],1,1)['success']; assert complete_sale(s['sale_id'],'cash')['success']
