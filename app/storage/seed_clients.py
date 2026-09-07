from app.storage.connection import SessionFactory
from app.storage.entities import Client

def load_demo_clients():
    db=SessionFactory()
    try:
        if db.query(Client).count(): return
        db.add_all([Client(name='Arun Kumar',phone='9000000001'),Client(name='Priya S',phone='9000000002')])
        db.commit()
    finally: db.close()
