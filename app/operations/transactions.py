from app.storage.connection import SessionFactory
from app.storage.entities import Sale,SaleLine,Product,Client
from app.modules.settings import read_setting

def open_sale(client_id=None):
    db=SessionFactory();
    try:
        if client_id and not db.get(Client,client_id): return {'success':False,'message':'Client not found.'}
        s=Sale(client_id=client_id); db.add(s); db.commit(); return {'success':True,'sale_id':s.id}
    finally: db.close()

def _recalc(s):
    subtotal=sum(x.quantity*x.unit_price for x in s.lines); tax=sum(x.tax for x in s.lines); s.subtotal=round(subtotal,2); s.tax=round(tax,2); s.total=round(subtotal+tax,2)

def add_sale_line(sale_id,product_id,quantity):
    db=SessionFactory()
    try:
        s=db.get(Sale,sale_id); p=db.get(Product,product_id)
        if not s or s.status!='open' or not p or quantity<=0: return {'success':False,'message':'Invalid sale, product or quantity.'}
        already=sum(x.quantity for x in s.lines if x.product_id==product_id)
        if p.quantity<already+quantity: return {'success':False,'message':f'Only {p.quantity} units available.'}
        tax=quantity*p.sell_price*p.gst_rate/100; s.lines.append(SaleLine(product_id=product_id,quantity=quantity,unit_price=p.sell_price,tax=tax)); _recalc(s); db.commit(); return {'success':True,'total':s.total}
    finally: db.close()

def revise_sale_line(sale_id,line_id,quantity):
    db=SessionFactory()
    try:
        s=db.get(Sale,sale_id); line=db.get(SaleLine,line_id)
        if not s or not line or s.status!='open' or quantity<=0: return {'success':False,'message':'Invalid line or sale.'}
        p=db.get(Product,line.product_id)
        if p.quantity<quantity: return {'success':False,'message':'Insufficient stock.'}
        line.quantity=quantity; line.tax=quantity*line.unit_price*p.gst_rate/100; _recalc(s); db.commit(); return {'success':True,'total':s.total}
    finally: db.close()

def sale_details(sale_id):
    db=SessionFactory()
    try:
        s=db.get(Sale,sale_id)
        if not s:return {'success':False,'message':'Sale not found.'}
        return {'success':True,'sale':{'id':s.id,'status':s.status,'subtotal':s.subtotal,'tax':s.tax,'total':s.total,'payment':s.payment,'lines':[{'id':x.id,'product':x.product.name,'qty':x.quantity,'unit_price':x.unit_price} for x in s.lines]}}
    finally: db.close()

def complete_sale(sale_id,payment=None):
    db=SessionFactory()
    try:
        s=db.get(Sale,sale_id)
        if not s or s.status!='open': return {'success':False,'message':'Sale is unavailable or already completed.'}
        if not s.lines: return {'success':False,'message':'Add at least one item.'}
        mode=payment or read_setting('default_payment').get('value')
        if not mode:return {'success':False,'message':'Payment mode is required.'}
        for line in s.lines:
            p=db.get(Product,line.product_id)
            if p.quantity<line.quantity: return {'success':False,'message':f'Insufficient stock for {p.name}.'}
        for line in s.lines: db.get(Product,line.product_id).quantity-=line.quantity
        s.payment=mode.lower(); s.status='completed'
        if s.payment=='credit' and s.client: s.client.credit_due+=s.total
        db.commit(); return {'success':True,'sale_id':s.id,'total':s.total,'payment':s.payment}
    finally: db.close()
