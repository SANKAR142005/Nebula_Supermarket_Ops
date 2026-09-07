from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from app.operations.transactions import sale_details
from app.modules.settings import read_setting

def create_receipt(sale_id,output='generated/receipt.pdf'):
    data=sale_details(sale_id)
    if not data.get('success'): return data
    Path(output).parent.mkdir(parents=True,exist_ok=True); c=canvas.Canvas(output,pagesize=A4); y=800
    shop=read_setting('shop_name').get('value') or 'SmartStore'
    c.setFont('Helvetica-Bold',16); c.drawString(50,y,shop); y-=30; c.setFont('Helvetica',10)
    s=data['sale']; c.drawString(50,y,f'Receipt #{s["id"]}'); y-=25
    for line in s['lines']:
        c.drawString(50,y,f'{line["product"]} x {line["qty"]}'); c.drawRightString(540,y,f'{line["unit_price"]*line["qty"]:.2f}'); y-=18
    y-=10; c.drawString(50,y,f'Subtotal: {s["subtotal"]:.2f}'); y-=18; c.drawString(50,y,f'Tax: {s["tax"]:.2f}'); y-=18; c.drawString(50,y,f'Total: {s["total"]:.2f}'); y-=18; c.drawString(50,y,f'Payment: {s["payment"] or "-"}'); c.save(); return {'success':True,'file':output}
