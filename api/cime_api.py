import re
import requests
import logging

_API_LIVE = "https://api.ci.me/api/openapi/v1/{}/live-status"
_CHANNEL_PAGE = "https://ci.me/@{}"
_HEADERS = {"User-Agent": "Mozilla/5.0"}
_TIMEOUT = 5


def resolve_id(handle: str) -> str | None:
    try:
        r = requests.get(_CHANNEL_PAGE.format(handle), headers=_HEADERS, timeout=_TIMEOUT)
        r.raise_for_status()
        m = re.search(r'"id":"(\d+)","slug":"' + re.escape(handle) + '"', r.text)
        if m:
            return m.group(1)
        logging.warning(f"CIME ID 파싱 실패 ({handle})")
        return None
    except Exception as e:
        logging.warning(f"CIME ID 조회 실패 ({handle}): {e}")
        return None


def get_live_detail(channel_id: str) -> dict:
    try:
        r = requests.get(_API_LIVE.format(channel_id), headers=_HEADERS, timeout=_TIMEOUT)
        r.raise_for_status()
        c = r.json().get("content", {})
        live = c.get("isLive", False)
        return {
            "is_live": live,
            "title": c.get("title", "") if live else "",
            "category": "",
            "since": c.get("openedAt", "") if live else "",
        }
    except Exception:
        return {"is_live": False, "title": "", "category": "", "since": ""}


def is_live(channel_id: str) -> bool:
    return get_live_detail(channel_id)["is_live"]
