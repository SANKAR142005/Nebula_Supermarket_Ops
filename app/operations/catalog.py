from app.storage.connection import SessionFactory
from app.storage.entities import Product

def find_items(query):
    db=SessionFactory()
    try:
        q=(query or '').strip()
        if not q: return {'success':False,'message':'Search text is required.'}
        rows=db.query(Product).filter(Product.name.ilike(f'%{q}%')).all()
        return {'success':True,'items':[{'id':p.id,'name':p.name,'sku':p.sku,'price':p.sell_price,'stock':p.quantity,'unit':p.unit,'gst':p.gst_rate} for p in rows]}
    finally: db.close()
