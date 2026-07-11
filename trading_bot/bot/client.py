from __future__ import annotations

import logging
from typing import Any

from binance.client import Client

from .config import load_settings
from .exceptions import APIRequestError

LOGGER = logging.getLogger(__name__)


def create_client() -> Client:
    settings = load_settings()

    try:
        client = Client(settings.api_key, settings.api_secret, testnet=settings.testnet)
        if settings.testnet and settings.base_url:
            client.API_URL = settings.base_url
        LOGGER.info("Binance client created for testnet environment.")
        return client
    except Exception as error:
        LOGGER.error("Failed to create Binance client. %s", error)
        raise APIRequestError("Unable to initialize Binance client. Please check API credentials and network connectivity.") from error


def ping(client: Client) -> bool:
    try:
        client.ping()
        LOGGER.info("Binance API ping successful.")
        return True
    except Exception as error:
        LOGGER.error("Binance API ping failed. %s", error)
        raise APIRequestError("Unable to reach Binance Testnet API. Please verify network connectivity and endpoint settings.") from error
