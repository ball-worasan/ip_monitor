import requests, time
from ..utils.logger import log
from ..config import ZCLOUD_USERNAME, ZCLOUD_PASSWORD, ZCLOUD_TENANT_ID

AUTH_ENDPOINT = "https://identity.bkk1.cloud.z.com/v2.0/tokens"
BASE_ENDPOINT = "https://dns-service.bkk1.cloud.z.com/v1"

def _auth_token():
    payload = {
        "auth": {
            "passwordCredentials": {
                "username": ZCLOUD_USERNAME,
                "password": ZCLOUD_PASSWORD
            },
            "tenantId": ZCLOUD_TENANT_ID
        }
    }
    try:
        r = requests.post(AUTH_ENDPOINT, json=payload, timeout=10)
        r.raise_for_status()
        return r.json()["access"]["token"]["id"]
    except Exception as e:
        log(f"DNS auth error: {e}", level="error")
        return None

def _request(method, url, token, **kwargs):
    headers = kwargs.pop("headers", {})
    headers.update({
        "Accept": "application/json",
        "X-Auth-Token": token
    })
    return requests.request(method, url, headers=headers, timeout=10, **kwargs)

def _domain_ids(token):
    url = f"{BASE_ENDPOINT}/domains"
    try:
        r = _request("get", url, token)
        r.raise_for_status()
        return [d["id"] for d in r.json().get("domains", [])]
    except Exception as e:
        log(f"Fetch domain ids error: {e}", level="error")
        return []

def _a_records(token, domain_id):
    url = f"{BASE_ENDPOINT}/domains/{domain_id}/records"
    try:
        r = _request("get", url, token)
        r.raise_for_status()
        return [rec for rec in r.json().get("records", []) if rec.get("type") == "A"]
    except Exception as e:
        log(f"Fetch records error: {e}", level="error")
        return []

def _update_record(token, domain_id, record_id, name, ip):
    url = f"{BASE_ENDPOINT}/domains/{domain_id}/records/{record_id}"
    payload = {"name": name, "type": "A", "data": ip}
    try:
        r = _request("put", url, token, json=payload)
        r.raise_for_status()
        return True
    except Exception as e:
        log(f"Update record error: {e}", level="error")
        return False

def update_dns(ip_address: str):
    token = _auth_token()
    if not token:
        return []

    updated = []
    for domain_id in _domain_ids(token):
        for rec in _a_records(token, domain_id):
            success = _update_record(token, domain_id, rec["id"], rec["name"], ip_address)
            time.sleep(1)
            if success:
                updated.append(rec["name"])
                log(f"Updated {rec['name']} to {ip_address}")
    return updated
