import time, sys
from pathlib import Path
from .config import CHECK_INTERVAL, IP_HISTORY_FILE
from .utils.logger import log
from .network import ping_ok, public_ip
from .dns.client import update_dns
from .notifiers.line import push_message
from .notifiers.discord import send_discord

def read_history(file_path: Path) -> set[str]:
    if file_path.exists():
        return set(file_path.read_text().splitlines())
    return set()

def append_history(ip: str, file_path: Path):
    with file_path.open("a") as f:
        f.write(ip + "\n")

def craft_message(ip: str, domains: list[str]) -> str:
    if domains:
        domain_list = "\n".join(f"- {d}" for d in domains)
        return f"📡 IP Address Changed\nIP: {ip}\n\n✅ DNS updated for:\n{domain_list}"
    return f"⚠️ IP Address Changed to {ip}\n(No DNS records updated)"

def run():
    history_file = Path(IP_HISTORY_FILE)
    seen = read_history(history_file)
    log("ip_monitor started.")
    while True:
        if not ping_ok():
            log("No internet. Retry after 60s.", level="warning")
            time.sleep(60)
            continue

        ip = public_ip()
        if not ip:
            time.sleep(60)
            continue

        if ip not in seen:
            domains = update_dns(ip)
            msg = craft_message(ip, domains)
            push_message(msg)
            send_discord(msg)
            append_history(ip, history_file)
            seen.add(ip)
            log(f"New IP processed: {ip}")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        log("Stopped by user.")
        sys.exit(0)
