import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from datetime import datetime
from ..config import LOG_FILE

LOG_PATH = Path(LOG_FILE)
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("ip_monitor")
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(LOG_PATH, maxBytes=1_000_000, backupCount=3, encoding="utf-8")
fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
handler.setFormatter(fmt)
logger.addHandler(handler)

def log(msg, level="info"):
    getattr(logger, level)(msg)
