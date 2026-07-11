# Binance Futures Testnet Trading Bot

## Overview

This project is a lightweight command-line trading bot for Binance USDT-M Futures Testnet. It lets you place market, limit, and stop-limit orders with validation, clear error handling, and rotating file logs.

## What the bot supports

- Market orders
- Limit orders
- Stop-limit orders
- BUY and SELL order sides
- Input validation for symbol, order type, quantity, price, and stop price
- Secure configuration through environment variables
- Structured logs written to the local logs folder

## Project structure

- [cli.py](cli.py) - CLI entry point and user-facing flow
- [trading_bot/bot/client.py](trading_bot/bot/client.py) - Binance client initialization
- [trading_bot/bot/orders.py](trading_bot/bot/orders.py) - Order execution logic
- [trading_bot/bot/validators.py](trading_bot/bot/validators.py) - Input sanitization and validation
- [trading_bot/bot/config.py](trading_bot/bot/config.py) - Environment configuration loading
- [trading_bot/bot/logging_config.py](trading_bot/bot/logging_config.py) - Rotating log setup
- [trading_bot/bot/exceptions.py](trading_bot/bot/exceptions.py) - Custom error types

## Requirements

- Python 3.11+
- Binance Futures Testnet API credentials

## Setup

1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies

```powershell
pip install -r requirements.txt
```

3. Create a local environment file

```powershell
Copy-Item .env.example .env
```

4. Fill in your Binance Futures Testnet credentials in [.env](.env)

```env
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_api_secret_here
TESTNET=True
```

## How to get Binance Testnet keys

1. Sign in to the Binance Futures Testnet portal
2. Open API Management
3. Create a new API key and secret for the testnet account
4. Paste them into your [.env](.env) file

## Running the bot

Once your [.env](.env) file contains valid Binance Futures Testnet API credentials, you can place orders:

### Market order

```powershell
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### Limit order

```powershell
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 120000
```

### Stop-limit order

```powershell
python cli.py --symbol BTCUSDT --side BUY --type STOP_LIMIT --quantity 0.01 --price 120000 --stop-price 119500
```

You can also use the alias flag name `--order-type` instead of `--type`.

## Expected behavior

The CLI prints:

- A request summary
- A formatted Binance response
- A success or failure message

Errors and order activity are also written to [logs/trading.log](logs/trading.log).

## Notes

- This bot targets Binance Futures Testnet only.
- Keep your API keys private and do not commit [.env](.env) to version control.
- The bot validates the request before contacting Binance, which helps avoid avoidable API errors.
