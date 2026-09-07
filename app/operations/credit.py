from app.storage.connection import SessionFactory
from app.storage.entities import Client

def client_balance(client_id):
    db=SessionFactory();
    try:
        c=db.get(Client,client_id); return {'success':bool(c),'client':c.name if c else None,'balance':round(c.credit_due,2) if c else None}
    finally: db.close()

def record_credit_payment(client_id,amount):
    db=SessionFactory()
    try:
        c=db.get(Client,client_id)
        if not c or amount<=0: return {'success':False,'message':'Invalid client or amount.'}
        c.credit_due=max(0,c.credit_due-amount); db.commit(); return {'success':True,'balance':c.credit_due}
    finally: db.close()

def credit_summary():
    db=SessionFactory()
    try:
        rows=db.query(Client).filter(Client.credit_due>0).all(); return {'success':True,'total_due':round(sum(c.credit_due for c in rows),2),'clients':[{'id':c.id,'name':c.name,'due':c.credit_due} for c in rows]}
    finally: db.close()
