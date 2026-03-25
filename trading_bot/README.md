# 🤖 Simplified Binance Futures Trading Bot (Testnet)

A Python-based CLI tool to place Market and Limit orders on the **Binance Futures Testnet (USDT-M)**.

## Features
- **Place Market & Limit Orders**: Support for both BUY and SELL sides.
- **Bonus Implementation**: Enhanced CLI interface with `rich` formatting.
- **Bonus Implementation**: `Stop-Limit` support included in the client layer.
- **Robustness**: Comprehensive input validation and structured error handling.
- **Logging**: Detailed logs of all API requests, responses, and errors.
- **Account View**: Ability to check testnet account balances.

## Prerequisites
- Python 3.8+
- [Binance Futures Testnet Credentials](https://testnet.binancefuture.com) (API Key & Secret Key).

## Setup Instructions

1. **Clone or Extract** the project directory.
2. **Create a Virtual Environment** (Optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or venv\Scripts\activate on Windows
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure Environment**:
   Create a `.env` file in the root directory and add your Binance Testnet keys:
   ```env
   BINANCE_API_KEY=your_testnet_api_key
   BINANCE_API_SECRET=your_testnet_api_secret
   ```

## 🏗️ Project Structure
```text
trading_bot/
  bot/
    client.py        # Binance API wrapper (USDT-M Futures Testnet)
    orders.py        # Business logic for order management
    validators.py    # Input data validation
    logging_config.py# Centralized logging configuration
  cli.py             # CLI entry point (Click + Rich)
  README.md          # Project documentation
  requirements.txt   # Dependencies
  logs/              # Directory where log files are stored
```

## Usage & Run Examples

### 1. Check Account Balance
Ensure your API keys are working:
```bash
python trading_bot/cli.py balance
```

### 2. Place a MARKET Order
Example: BUY 0.001 BTCUSDT at market price.
```bash
python trading_bot/cli.py order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### 3. Place a LIMIT Order
Example: SELL 0.001 BTCUSDT at $70,000.
```bash
python trading_bot/cli.py order -s BTCUSDT -d SELL -t LIMIT -q 0.01 -p 70000
```

## Assumptions & Constraints
- **Testnet Only**: The bot is hardcoded to use `testnet=True` for safety.
- **USDT-M**: Designed specifically for USDT-Margined Futures.
- **Symbol Format**: Expects standard Binance symbols (e.g., `BTCUSDT`).
- **Leverage**: Assumes the default leverage of the testnet account.

## Logging
All activities are logged to `logs/trading_bot.log`. This file contains the full JSON response from Binance for auditing and debugging.
