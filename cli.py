from __future__ import annotations

import argparse
import logging
from time import perf_counter
from typing import Optional

from trading_bot.bot.client import create_client, ping
from trading_bot.bot.logging_config import configure_logging
from trading_bot.bot.orders import place_limit_order, place_market_order, place_stop_limit_order
from trading_bot.bot.validators import (
    validate_order_type,
    validate_price,
    validate_quantity,
    validate_side,
    validate_symbol,
    validate_stop_price,
)
from trading_bot.bot.exceptions import OrderExecutionError, TradingBotError

LOGGER = logging.getLogger(__name__)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot")
    parser.add_argument("--symbol", required=True, help="Trading symbol, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, help="Order side: BUY or SELL")
    parser.add_argument(
        "--type",
        "--order-type",
        required=True,
        dest="order_type",
        help="Order type: MARKET, LIMIT, or STOP_LIMIT",
    )
    parser.add_argument("--quantity", required=True, help="Order quantity as a positive number")
    parser.add_argument("--price", help="Limit price as a positive number, required for LIMIT and STOP_LIMIT orders")
    parser.add_argument("--stop-price", dest="stop_price", help="Stop price as a positive number, required for STOP_LIMIT orders")

    return parser.parse_args()


def format_order_summary(symbol: str, side: str, order_type: str, quantity: float, price: Optional[float], stop_price: Optional[float]) -> str:
    lines = [
        "=====================================",
        "Order Summary",
        "=====================================",
        f"Symbol\n{symbol}",
        f"Side\n{side}",
        f"Type\n{order_type}",
        f"Quantity\n{quantity}",
    ]

    if price is not None:
        lines.append(f"Price\n{price}")

    if stop_price is not None:
        lines.append(f"Stop Price\n{stop_price}")

    lines.append("=====================================")
    return "\n".join(lines)


def format_response(response: dict[str, object]) -> str:
    lines = [
        "After execution",
        "=====================================",
        "Response",
        "=====================================",
        f"Order ID\n{response.get('orderId')}",
        f"Status\n{response.get('status')}",
        f"Executed Quantity\n{response.get('executedQty')}",
        f"Average Price\n{response.get('avgPrice')}",
        f"Time\n{response.get('transactTime') or response.get('updateTime')}",
        "====================================="
    ]
    return "\n".join(lines)


def main() -> int:
    configure_logging()
    LOGGER.info("Application started.")

    start_time = perf_counter()

    try:
        args = parse_arguments()
        LOGGER.info(
            "Parsed arguments: symbol=%s side=%s type=%s quantity=%s price=%s stop_price=%s",
            args.symbol,
            args.side,
            args.order_type,
            args.quantity,
            args.price,
            args.stop_price,
        )

        symbol = validate_symbol(args.symbol)
        side = validate_side(args.side)
        order_type = validate_order_type(args.order_type)
        quantity = validate_quantity(args.quantity)
        price = validate_price(args.price, order_type)
        stop_price = validate_stop_price(args.stop_price, order_type)

        LOGGER.info("Validation succeeded for order request.")

        print(format_order_summary(symbol, side, order_type, quantity, price, stop_price))

        client = create_client()
        ping(client)

        if order_type == "MARKET":
            response = place_market_order(client, symbol, side, quantity)
        elif order_type == "LIMIT":
            response = place_limit_order(client, symbol, side, quantity, price)  # type: ignore[arg-type]
        else:
            response = place_stop_limit_order(client, symbol, side, quantity, price, stop_price)  # type: ignore[arg-type]

        print(format_response(response))
        print("Order placed successfully.")
        LOGGER.info("Order placed successfully. orderId=%s", response.get("orderId"))
        return 0

    except TradingBotError as error:
        LOGGER.error("TradingBotError: %s", error)
        print(f"Error: {error}")
        print("Order failed.")
        return 1
    except Exception as error:
        LOGGER.exception("Unexpected exception occurred.")
        print("An unexpected error occurred. Please check the logs for details.")
        return 1
    finally:
        duration = perf_counter() - start_time
        LOGGER.info("Execution completed in %.3f seconds.", duration)


if __name__ == "__main__":
    raise SystemExit(main())
