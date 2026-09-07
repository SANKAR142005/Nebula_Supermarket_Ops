from app.storage.connection import SessionFactory
from app.storage.entities import Client

def create_client(name,phone=None):
    db=SessionFactory()
    try:
        if phone and db.query(Client).filter_by(phone=phone).first(): return {'success':False,'message':'Phone already registered.'}
        c=Client(name=name,phone=phone); db.add(c); db.commit(); return {'success':True,'client_id':c.id}
    finally: db.close()

def find_clients(query):
    db=SessionFactory()
    try:
        rows=db.query(Client).filter(Client.name.ilike(f'%{query}%')).all()
        return {'success':True,'clients':[{'id':c.id,'name':c.name,'phone':c.phone,'credit_due':c.credit_due} for c in rows]}
    finally: db.close()

def client_details(client_id):
    db=SessionFactory()
    try:
        c=db.get(Client,client_id)
        return {'success':bool(c),'client':{'id':c.id,'name':c.name,'phone':c.phone,'credit_due':c.credit_due} if c else None}
    finally: db.close()
