from app.operations.stock import add_item, receive_inventory, stock_status, low_inventory
from app.operations.catalog import find_items
from app.operations.clients import create_client, find_clients, client_details
from app.operations.credit import client_balance, record_credit_payment, credit_summary
from app.operations.transactions import open_sale, add_sale_line, revise_sale_line, sale_details, complete_sale
from app.operations.purchasing import purchase_suggestions
from app.operations.insights import sales_overview, daily_revenue
from app.operations.revenue import profitability
from app.operations.system_health import health_check
from app.modules.settings import save_setting, read_setting, all_settings, remove_setting
from app.modules.receipts import create_receipt
from app.modules.reports import create_report

ACTIONS = {
    'find_items': find_items, 'add_item': add_item, 'receive_inventory': receive_inventory,
    'stock_status': stock_status, 'low_inventory': low_inventory, 'create_client': create_client,
    'find_clients': find_clients, 'client_details': client_details, 'client_balance': client_balance,
    'record_credit_payment': record_credit_payment, 'credit_summary': credit_summary,
    'open_sale': open_sale, 'add_sale_line': add_sale_line, 'revise_sale_line': revise_sale_line,
    'sale_details': sale_details, 'complete_sale': complete_sale, 'purchase_suggestions': purchase_suggestions,
    'sales_overview': sales_overview, 'daily_revenue': daily_revenue, 'profitability': profitability,
    'health_check': health_check, 'save_setting': save_setting, 'read_setting': read_setting,
    'all_settings': all_settings, 'remove_setting': remove_setting, 'create_receipt': create_receipt,
    'create_report': create_report,
}

def run_action(name, **kwargs):
    fn=ACTIONS.get(name)
    if not fn: return {'success':False,'message':f'Unknown action: {name}'}
    try: return fn(**kwargs)
    except Exception as exc: return {'success':False,'message':str(exc)}
