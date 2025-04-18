import requests, json
from ..config import DISCORD_WEBHOOK
from ..utils.logger import log

def send_discord(message: str):
    if not DISCORD_WEBHOOK:
        log("Discord webhook missing. Skipping Discord notification.")
        return
    payload = {"content": message}
    try:
        r = requests.post(DISCORD_WEBHOOK, json=payload, timeout=10)
        if r.status_code in (200, 204):
            log("Discord message sent.")
        else:
            log(f"Discord webhook failed {r.status_code}: {r.text}", level="warning")
    except requests.RequestException as e:
        log(f"Discord webhook error: {e}", level="error")
