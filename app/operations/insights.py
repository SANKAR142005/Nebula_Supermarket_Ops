from datetime import datetime,timedelta
from app.storage.connection import SessionFactory
from app.storage.entities import Sale

def sales_overview(days=1):
    db=SessionFactory();
    try:
        start=datetime.utcnow()-timedelta(days=days); rows=db.query(Sale).filter(Sale.status=='completed',Sale.created_at>=start).all(); total=sum(s.total for s in rows); return {'success':True,'bills':len(rows),'revenue':round(total,2),'average_bill':round(total/len(rows),2) if rows else 0}
    finally: db.close()

def daily_revenue(date=None):
    # Uses UTC-neutral date for the demo; production can apply store timezone boundaries.
    db=SessionFactory();
    try:
        target=datetime.strptime(date,'%Y-%m-%d').date() if date else datetime.utcnow().date(); rows=[s for s in db.query(Sale).filter(Sale.status=='completed').all() if s.created_at.date()==target]; return {'success':True,'date':str(target),'revenue':round(sum(s.total for s in rows),2),'bills':len(rows)}
    finally: db.close()
