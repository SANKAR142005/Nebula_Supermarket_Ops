ALLOWED_PAYMENTS={'cash','upi','card','credit'}

def valid_payment(mode): return str(mode).lower() in ALLOWED_PAYMENTS

def positive_number(value):
    try:return float(value)>0
    except (TypeError,ValueError):return False
