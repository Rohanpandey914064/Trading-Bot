from __future__ import annotations

from typing import Optional

from .exceptions import ValidationError


VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT", "STOP_LIMIT"}


def validate_symbol(symbol: Optional[str]) -> str:
    if not symbol or not isinstance(symbol, str):
        raise ValidationError("Symbol is required and must be a non-empty string.")

    normalized = symbol.strip().upper()
    if not normalized.isalnum():
        raise ValidationError("Symbol must contain only alphanumeric characters.")

    return normalized


def validate_side(side: Optional[str]) -> str:
    if not side or not isinstance(side, str):
        raise ValidationError("Side is required and must be BUY or SELL.")

    normalized = side.strip().upper()
    if normalized not in VALID_SIDES:
        raise ValidationError("Side must be either BUY or SELL.")

    return normalized


def validate_order_type(order_type: Optional[str]) -> str:
    if not order_type or not isinstance(order_type, str):
        raise ValidationError("Order type is required and must be MARKET, LIMIT, or STOP_LIMIT.")

    normalized = order_type.strip().upper()
    if normalized not in VALID_ORDER_TYPES:
        raise ValidationError("Order type must be MARKET, LIMIT, or STOP_LIMIT.")

    return normalized


def validate_stop_price(stop_price: Optional[str], order_type: str) -> Optional[float]:
    if order_type == "STOP_LIMIT":
        if stop_price is None:
            raise ValidationError("Stop price is required for STOP_LIMIT orders.")

        try:
            result = float(stop_price)
        except (ValueError, TypeError):
            raise ValidationError("Stop price must be a valid number.")

        if result <= 0:
            raise ValidationError("Stop price must be greater than 0.")

        return result

    return None


def validate_quantity(quantity: Optional[str]) -> float:
    if quantity is None:
        raise ValidationError("Quantity is required and must be a positive number.")

    try:
        result = float(quantity)
    except (ValueError, TypeError):
        raise ValidationError("Quantity must be a valid number.")

    if result <= 0:
        raise ValidationError("Quantity must be greater than 0.")

    return result


def validate_price(price: Optional[str], order_type: str) -> Optional[float]:
    if order_type in {"LIMIT", "STOP_LIMIT"}:
        if price is None:
            raise ValidationError("Price is required for LIMIT and STOP_LIMIT orders.")

        try:
            result = float(price)
        except (ValueError, TypeError):
            raise ValidationError("Price must be a valid number.")

        if result <= 0:
            raise ValidationError("Price must be greater than 0.")

        return result

    return None
