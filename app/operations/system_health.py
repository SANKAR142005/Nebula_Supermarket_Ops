from sqlalchemy import text
from app.storage.connection import SessionFactory
from app.storage.entities import Product,Client,Sale

def health_check():
    db=SessionFactory()
    try:
        db.execute(text('SELECT 1')); return {'success':True,'database':'ok','products':db.query(Product).count(),'clients':db.query(Client).count(),'sales':db.query(Sale).count()}
    except Exception as e:return {'success':False,'database':'error','message':str(e)}
    finally: db.close()
