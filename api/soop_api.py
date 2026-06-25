import requests

SOOP_API = "https://live.sooplive.co.kr/afreeca/player_live_api.php"
TIMEOUT = 5

_PAYLOAD_BASE = {
    "bno": "null",
    "type": "live",
    "pwd": "",
    "player_type": "html5",
    "stream_type": "common",
    "quality": "HD",
    "mode": "landing",
    "from_api": "0",
    "is_revive": "false",
}

def _post(uid: str) -> dict:
    payload = {**_PAYLOAD_BASE, "bid": uid}
    r = requests.post(
        SOOP_API,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=payload,
        timeout=TIMEOUT,
    )
    r.raise_for_status()
    return r.json().get("CHANNEL", {})

def get_channel_info(uid: str) -> dict:
    try:
        ch = _post(uid)
        return {
            "title": ch.get("TITLE", ""),
            "is_live": ch.get("STATE") == "live",
            "bj_nickname": ch.get("BJ_NICK", ""),
            "viewer": ch.get("VIEWER", 0),
        }
    except Exception as e:
        print(f"[ERROR] soop 방송 정보 요청 실패: {e}")
        return {"title": "", "is_live": False, "bj_nickname": "", "viewer": 0}

def is_live(uid: str) -> bool:
    try:
        ch = _post(uid)
        return int(ch.get("BNO", 0)) > 0
    except Exception:
        return False
