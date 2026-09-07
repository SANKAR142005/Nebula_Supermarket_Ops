from app.storage.connection import SessionFactory
from app.storage.entities import Product

def load_demo_products():
    db=SessionFactory()
    try:
        if db.query(Product).count(): return
        rows=[('Rice 5kg','RICE5',1,320,280,350,18,5,5,'1006'),('Wheat Flour 5kg','ATTA5',1,260,225,290,12,5,5,'1101'),('Milk 1L','MILK1',1,62,52,65,25,10,5,'0401'),('Tea 250g','TEA250',1,145,120,160,8,4,5,'0902'),('Biscuits Pack','BISC01',1,30,22,35,20,8,5,'1905')]
        for n,sku,u,sp,cp,mrp,q,r,g,hsn in rows: db.add(Product(name=n,sku=sku,unit='pack',sell_price=sp,cost_price=cp,mrp=mrp,quantity=q,reorder_point=r,gst_rate=g,hsn=hsn))
        db.commit()
    finally: db.close()
