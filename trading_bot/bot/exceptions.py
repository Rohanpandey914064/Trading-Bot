from __future__ import annotations


class TradingBotError(Exception):
    """Base exception for the trading bot."""


class ValidationError(TradingBotError):
    """Raised when validation of input values fails."""


class ConfigurationError(TradingBotError):
    """Raised when configuration loading or validation fails."""


class APIRequestError(TradingBotError):
    """Raised when Binance API request fails."""


class OrderExecutionError(TradingBotError):
    """Raised when an order cannot be executed."""
