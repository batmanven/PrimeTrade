from bot.client import BinanceFuturesClient
from bot.validators import validate_all
import logging

logger = logging.getLogger('trading_bot.orders')

class OrderManager:
    """Orchestrates order placement with validation and error handling."""
    
    def __init__(self, api_key=None, api_secret=None):
        self.client = BinanceFuturesClient(api_key, api_secret)

    def process_order(self, symbol, side, order_type, quantity, price=None, stop_price=None):
        """Validates input, then sends order request."""
        try:
            # 1. Validate Input
            v_symbol, v_side, v_type, v_qty, v_price, v_stop_price = validate_all(symbol, side, order_type, quantity, price, stop_price)
            
            # 2. Log intention
            logger.info(f"Preparing {v_type} {v_side} order: {v_qty} {v_symbol}")
            
            # 3. Place order through client
            response = self.client.place_order(
                symbol=v_symbol,
                side=v_side,
                order_type=v_type,
                quantity=v_qty,
                price=v_price,
                stop_price=v_stop_price
            )
    
            summary = {
                'orderId': response.get('orderId'),
                'status': response.get('status'),
                'symbol': response.get('symbol'),
                'executedQty': response.get('executedQty'),
                'avgPrice': response.get('avgPrice') or response.get('price'),
                'origQty': response.get('origQty')
            }
            logger.info(f"Order Success Summary: {summary}")
            return True, summary

        except ValueError as ve:
            # User input error
            logger.error(f"Input Validation Error: {ve}")
            return False, str(ve)
        except Exception as e:
            # API or network error
            logger.error(f"Execution Error: {str(e)}")
            return False, f"Execution failed: {str(e)}"
