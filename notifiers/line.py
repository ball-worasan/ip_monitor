import requests, json
from ..config import LINE_TOKEN, LINE_USER_ID
from ..utils.logger import log

def push_message(message: str):
    if not LINE_TOKEN or not LINE_USER_ID:
        log("LINE credentials missing. Skipping LINE push.")
        return
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "to": LINE_USER_ID,
        "messages": [{
            "type": "text",
            "text": message
        }]
    }
    try:
        r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
        if r.status_code == 200:
            log("LINE message sent.")
        else:
            log(f"LINE push failed {r.status_code}: {r.text}", level="warning")
    except requests.RequestException as e:
        log(f"LINE push error: {e}", level="error")
