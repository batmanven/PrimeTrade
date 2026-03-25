import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logging(log_file='trading_bot.log'):
    """Sets up recording of API calls and errors."""
    
    # Create logs directory if it doesn't exist
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_path = os.path.join(log_dir, log_file)
    
    # Setup formatter
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(log_format)
    
    # Root logger
    logger = logging.getLogger('trading_bot')
    logger.setLevel(logging.INFO)
    
    # File handler
    file_handler = RotatingFileHandler(log_path, maxBytes=10*1024*1024, backupCount=5)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger
