from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

from .exceptions import ConfigurationError


@dataclass(frozen=True)
class Settings:
    api_key: str
    api_secret: str
    testnet: bool
    base_url: Optional[str]


def load_settings() -> Settings:
    load_dotenv()

    api_key = os.getenv("BINANCE_API_KEY", "").strip()
    api_secret = os.getenv("BINANCE_API_SECRET", "").strip()
    testnet_string = os.getenv("TESTNET", "True").strip().lower()

    if not api_key or not api_secret:
        raise ConfigurationError(
            "Missing Binance API credentials. Please set BINANCE_API_KEY and BINANCE_API_SECRET in the .env file."
        )

    testnet = testnet_string in {"true", "1", "yes", "y"}
    base_url = "https://testnet.binancefuture.com" if testnet else None

    return Settings(api_key=api_key, api_secret=api_secret, testnet=testnet, base_url=base_url)
