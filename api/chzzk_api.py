import requests

CHZZK_API_URL = "https://api.chzzk.naver.com/service/v1/channels/{}"
CHZZK_DETAIL_URL = "https://api.chzzk.naver.com/service/v2/channels/{}/live-detail"
TIMEOUT = 5

def get_channel_info(uid: str) -> dict:
    try:
        url = CHZZK_API_URL.format(uid)
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json().get("content", {})
    except requests.RequestException as e:
        print(f"네트워크 오류: {e}")
        return {}
    except ValueError as e:
        print(f"JSON Parse Error: {e}")
        return {}

def get_live_detail(uid: str) -> dict:
    try:
        url = CHZZK_DETAIL_URL.format(uid)
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=TIMEOUT)
        r.raise_for_status()
        c = r.json().get("content", {})
        live = c.get("status") == "OPEN"
        return {
            "is_live": live,
            "title": c.get("liveTitle", ""),
            "category": c.get("liveCategoryValue", ""),
            "since": c.get("openDate", ""),
            "end": "" if live else c.get("closeDate", ""),
        }
    except Exception:
        return {"is_live": False, "title": "", "category": "", "since": ""}


def is_live(uid: str) -> bool:
    try:
        url = CHZZK_API_URL.format(uid)
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json().get("content", {}).get("openLive", False)
    except Exception:
        return False
