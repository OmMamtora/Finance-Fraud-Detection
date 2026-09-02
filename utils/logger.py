import logging
from pathlib import Path

from config.settings import settings


def get_logger(name: str) -> logging.Logger:
    Path(settings.log_dir).mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    return logging.getLogger(name)

