from app.storage.connection import SessionFactory
from app.storage.entities import Product

def add_item(name,sku,unit='pcs',sell_price=0,cost_price=0,mrp=0,reorder_point=5,gst_rate=0,hsn=''):
    db=SessionFactory()
    try:
        if db.query(Product).filter_by(sku=sku).first(): return {'success':False,'message':'SKU already exists.'}
        p=Product(name=name,sku=sku,unit=unit,sell_price=sell_price,cost_price=cost_price,mrp=mrp or sell_price,quantity=0,reorder_point=reorder_point,gst_rate=gst_rate,hsn=hsn)
        db.add(p); db.commit(); return {'success':True,'product_id':p.id}
    finally: db.close()

def receive_inventory(product_id,quantity):
    db=SessionFactory()
    try:
        p=db.get(Product,product_id)
        if not p or quantity<=0: return {'success':False,'message':'Invalid product or quantity.'}
        p.quantity+=quantity; db.commit(); return {'success':True,'stock':p.quantity}
    finally: db.close()

def stock_status(product_id):
    db=SessionFactory()
    try:
        p=db.get(Product,product_id)
        return {'success':bool(p),'product':p.name if p else None,'stock':p.quantity if p else None,'reorder_point':p.reorder_point if p else None}
    finally: db.close()

def low_inventory():
    db=SessionFactory()
    try:
        rows=db.query(Product).filter(Product.quantity<=Product.reorder_point).all()
        return {'success':True,'items':[{'id':p.id,'name':p.name,'sku':p.sku,'stock':p.quantity,'reorder_point':p.reorder_point} for p in rows]}
    finally: db.close()
