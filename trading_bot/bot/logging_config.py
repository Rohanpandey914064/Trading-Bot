from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_FILE = Path(__file__).resolve().parents[1] / "logs" / "trading.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
LOG_LEVEL = logging.INFO
MAX_BYTES = 5 * 1024 * 1024
BACKUP_COUNT = 3


def configure_logging() -> None:
    logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)

    rotating_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=MAX_BYTES,
        backupCount=BACKUP_COUNT,
        encoding="utf-8",
    )
    rotating_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    rotating_handler.setLevel(LOG_LEVEL)

    root_logger = logging.getLogger()
    root_logger.handlers = [rotating_handler]
    root_logger.setLevel(LOG_LEVEL)
