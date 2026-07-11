from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException

from .exceptions import APIRequestError, OrderExecutionError

LOGGER = logging.getLogger(__name__)


def place_market_order(
    client: Client,
    symbol: str,
    side: str,
    quantity: float,
) -> Dict[str, Any]:
    try:
        LOGGER.info("Placing market order: symbol=%s side=%s quantity=%s", symbol, side, quantity)
        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity,
        )
        LOGGER.info("Market order response received: orderId=%s", response.get("orderId"))
        return response
    except (BinanceAPIException, BinanceOrderException) as error:
        LOGGER.error("Binance API rejected market order: %s", error)
        raise OrderExecutionError(f"Market order failed: {error}") from error
    except Exception as error:
        LOGGER.error("Unexpected error placing market order: %s", error)
        raise APIRequestError("Unexpected error while placing market order.") from error


def place_limit_order(
    client: Client,
    symbol: str,
    side: str,
    quantity: float,
    price: float,
) -> Dict[str, Any]:
    try:
        LOGGER.info(
            "Placing limit order: symbol=%s side=%s quantity=%s price=%s",
            symbol,
            side,
            quantity,
            price,
        )
        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            quantity=quantity,
            price=str(price),
            timeInForce="GTC",
        )
        LOGGER.info("Limit order response received: orderId=%s", response.get("orderId"))
        return response
    except (BinanceAPIException, BinanceOrderException) as error:
        LOGGER.error("Binance API rejected limit order: %s", error)
        raise OrderExecutionError(f"Limit order failed: {error}") from error
    except Exception as error:
        LOGGER.error("Unexpected error placing limit order: %s", error)
        raise APIRequestError("Unexpected error while placing limit order.") from error


def place_stop_limit_order(
    client: Client,
    symbol: str,
    side: str,
    quantity: float,
    price: float,
    stop_price: float,
) -> Dict[str, Any]:
    try:
        LOGGER.info(
            "Placing stop-limit order: symbol=%s side=%s quantity=%s price=%s stopPrice=%s",
            symbol,
            side,
            quantity,
            price,
            stop_price,
        )
        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="STOP",
            quantity=quantity,
            stopPrice=str(stop_price),
            price=str(price),
            timeInForce="GTC",
        )
        LOGGER.info("Stop-limit order response received: orderId=%s", response.get("orderId"))
        return response
    except (BinanceAPIException, BinanceOrderException) as error:
        LOGGER.error("Binance API rejected stop-limit order: %s", error)
        raise OrderExecutionError(f"Stop-limit order failed: {error}") from error
    except Exception as error:
        LOGGER.error("Unexpected error placing stop-limit order: %s", error)
        raise APIRequestError("Unexpected error while placing stop-limit order.") from error
