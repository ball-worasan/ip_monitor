# IP Monitor & DNS Updater

A lightweight service to monitor your public IP address, update Z.com DNS A-records when it changes,
and send beautifully formatted notifications to **LINE Messaging API** and **Discord**.

## Features
- Cross‑platform ping check
- Fast public IP retrieval (ipify)
- Automatic Z.com API authentication & bulk A‑record update
- Dual‑channel notifications (LINE push + Discord webhook)
- Rotating log files (`logs/app.log`) for long‑term evidence
- Configurable via `.env`

# 1) สร้าง virtual env ชื่อ venv
python3 -m venv venv

# 2) เปิดใช้งาน venv
source venv/bin/activate

# 3) ติดตั้งไลบรารีที่ต้องใช้
pip install --upgrade pip
pip install -r requirements.txt


## Quick Start
```bash
# clone or download the repo
pip install -r requirements.txt
cp .env.example .env  # fill your tokens
python -m main
```

## Environment Variables (`.env`)
```
LINE_CHANNEL_ACCESS_TOKEN=...
LINE_TARGET_USER_ID=...
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
ZCLOUD_USERNAME=...
ZCLOUD_PASSWORD=...
ZCLOUD_TENANT_ID=...
CHECK_INTERVAL=1200
```

## Log retention
- Logs rotate at 1 MB with 3 backups (`utils/logger.py`).
- Suitable as legal evidence; timestamps are in ISO‑8601.

## Run as a service (systemd)
```ini
[Unit]
Description=IP Monitor
After=network.target

[Service]
ExecStart=/usr/bin/python -m ip_monitor.main
WorkingDirectory=/opt/ip_monitor
Restart=always
User=ipmon

[Install]
WantedBy=multi-user.target
```

