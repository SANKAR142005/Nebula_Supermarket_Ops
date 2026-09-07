from app.storage.connection import SessionFactory
from app.storage.entities import Product

def purchase_suggestions():
    db=SessionFactory()
    try:
        rows=db.query(Product).filter(Product.quantity<=Product.reorder_point).all(); data=[]
        for p in rows:
            target=max(p.reorder_point*2,10); data.append({'product':p.name,'sku':p.sku,'current':p.quantity,'suggested':max(0,target-p.quantity),'estimated_cost':round(max(0,target-p.quantity)*p.cost_price,2)})
        return {'success':True,'recommendations':data}
    finally: db.close()
