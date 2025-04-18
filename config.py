"""Configuration loader for ip_monitor."""
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

LINE_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_USER_ID = os.getenv("LINE_TARGET_USER_ID")  # single user or group
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK_URL")

# Cloud Z DNS credentials
ZCLOUD_USERNAME = os.getenv("ZCLOUD_USERNAME")
ZCLOUD_PASSWORD = os.getenv("ZCLOUD_PASSWORD")
ZCLOUD_TENANT_ID = os.getenv("ZCLOUD_TENANT_ID")

# Behaviour
CHECK_HOST = os.getenv("CHECK_HOST", "8.8.8.8")
IP_API_URL = os.getenv("IP_API_URL", "https://api.ipify.org/?format=json")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "1200"))  # seconds
IP_HISTORY_FILE = os.getenv("IP_HISTORY_FILE", "IP_LIST.txt")
LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")
