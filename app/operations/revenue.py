from datetime import datetime,timedelta
from app.storage.connection import SessionFactory
from app.storage.entities import Sale

def profitability(days=30):
    db=SessionFactory()
    try:
        rows=db.query(Sale).filter(Sale.status=='completed',Sale.created_at>=datetime.utcnow()-timedelta(days=days)).all(); revenue=sum(s.total for s in rows); cost=sum(x.quantity*x.product.cost_price for s in rows for x in s.lines); return {'success':True,'revenue':round(revenue,2),'cost':round(cost,2),'gross_profit':round(revenue-cost,2),'margin_percent':round((revenue-cost)/revenue*100,2) if revenue else 0}
    finally: db.close()
