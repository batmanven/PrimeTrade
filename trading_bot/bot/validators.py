import re

def validate_symbol(symbol):
    """Checks if symbol format is valid (e.g., BTCUSDT)."""
    if not isinstance(symbol, str) or not symbol:
        return False
    return bool(re.match(r'^[A-Z0-9-]{3,12}$', symbol))

def validate_side(side):
    """Checks if side is BUY or SELL."""
    return side.upper() in ['BUY', 'SELL']

def validate_order_type(order_type):
    """Checks supported order types."""
    return order_type.upper() in ['MARKET', 'LIMIT', 'STOP_LIMIT']

def validate_numeric(val, field_name):
    """Ensure price/quantity are positive numbers."""
    try:
        f_val = float(val)
        if f_val <= 0:
            raise ValueError(f"{field_name} must be greater than zero.")
        return f_val
    except (ValueError, TypeError):
        raise ValueError(f"Invalid {field_name}. Must be a valid number.")

def validate_all(symbol, side, order_type, quantity, price=None, stop_price=None):
    """Consolidated validation logic."""
    if not validate_symbol(symbol.upper()):
        raise ValueError(f"Invalid Symbol: {symbol}")
    if not validate_side(side.upper()):
        raise ValueError(f"Invalid Side: {side}. Use BUY or SELL.")
    if not validate_order_type(order_type.upper()):
        raise ValueError(f"Invalid Order Type: {order_type}. Use MARKET, LIMIT, or STOP_LIMIT.")
    
    q_val = validate_numeric(quantity, "Quantity")
    p_val = None
    sp_val = None
    if order_type.upper() in ['LIMIT', 'STOP_LIMIT']:
        p_val = validate_numeric(price, "Price")
    
    if order_type.upper() == 'STOP_LIMIT':
        sp_val = validate_numeric(stop_price, "Stop Price")
        
    return symbol.upper(), side.upper(), order_type.upper(), q_val, p_val, sp_val
