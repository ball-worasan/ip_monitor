import subprocess, platform, requests
from .utils.logger import log
from .config import CHECK_HOST, IP_API_URL

def ping_ok(host: str = CHECK_HOST) -> bool:
    cmd = ["ping", "-n", "1", host] if platform.system() == "Windows" else ["ping", "-c", "1", host]
    try:
        result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        ok = result.returncode == 0
        if not ok:
            log("Ping failed")
        return ok
    except FileNotFoundError:
        log("Ping command not found.", level="error")
        return False

def public_ip() -> str | None:
    try:
        r = requests.get(IP_API_URL, timeout=5)
        r.raise_for_status()
        return r.json().get("ip")
    except Exception as e:
        log(f"Get IP error: {e}", level="error")
        return None
