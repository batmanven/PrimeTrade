import os
import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from dotenv import load_dotenv

# Load API keys
load_dotenv()

# Logger for the client
logger = logging.getLogger('trading_bot.client')

class BinanceFuturesClient:
    """A simple wrapper for Binance Futures Testnet interaction."""
    
    BASE_URL_TESTNET = "https://testnet.binancefuture.com"
    API_URL_TESTNET = "https://testnet.binancefuture.com/fapi/v1"

    def __init__(self, api_key=None, api_secret=None):
        self.api_key = api_key or os.getenv('BINANCE_API_KEY')
        self.api_secret = api_secret or os.getenv('BINANCE_API_SECRET')
        
        if not self.api_key or not self.api_secret:
            logger.error("API Key and Secret must be provided.")
            raise ValueError("API Key and Secret must be provided in .env or as arguments.")
        
        # Initialize Binance Client for Futures Testnet
        try:
            self.client = Client(self.api_key, self.api_secret, testnet=True)
            # Binance Futures specific check if API is working
            # Note: python-binance 'testnet=True' should handle URLs but Binance APIs often need explicit base URLs for some wrapper libs or specific FAPI calls
            # For python-binance it handles it internally when testnet=True.
            logger.info("Successfully connected to Binance Futures Testnet.")
        except Exception as e:
            logger.error(f"Failed to connect: {str(e)}")
            raise

    def get_account_balance(self):
        """Debug check to ensure connectivity and see funds."""
        try:
            return self.client.futures_account_balance()
        except (BinanceAPIException, BinanceRequestException) as e:
            logger.error(f"API Request failed: {e}")
            raise

    def place_order(self, symbol, side, order_type, quantity, price=None, stop_price=None):
        """Places various order types."""
        params = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'quantity': str(quantity)
        }
        
        if order_type == 'LIMIT':
            if not price:
                raise ValueError("Price is required for LIMIT order.")
            params['price'] = str(price)
            params['timeInForce'] = 'GTC' # Default Good Till Cancelled
        
        # STOP_MARKET/STOP_LIMIT can be bonuses later
        if order_type == 'STOP_LIMIT':
            if not price or not stop_price:
                 raise ValueError("Price and Stop Price are required for STOP_LIMIT.")
            params['price'] = str(price)
            params['stopPrice'] = str(stop_price)
            params['timeInForce'] = 'GTC'

        logger.info(f"Sending Order Request: {params}")
        
        try:
            response = self.client.futures_create_order(**params)
            logger.info(f"Order Response: {response}")
            return response
        except (BinanceAPIException, BinanceRequestException) as e:
            logger.error(f"Order Placement Error: {e}")
            raise
