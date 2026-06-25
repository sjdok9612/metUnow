import logging
import requests
from api.chzzk_api import get_channel_info
from tool.paths import ASSETS_DIR


def image_exists(key: str) -> bool:
    for ext in ("png", "webp", "jpg"):
        if (ASSETS_DIR / f"{key}.{ext}").exists():
            return True
    return False


def fetch_chzzk_image(uid: str) -> bytes | None:
    info = get_channel_info(uid)
    url = info.get("channelImageUrl", "")
    if not url:
        return None
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        return r.content
    except Exception as e:
        logging.warning(f"CHZZK 이미지 다운로드 실패: {e}")
        return None


def fetch_twitter_image(handle: str) -> bytes | None:
    url = f"https://unavatar.io/twitter/{handle}"
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        return r.content
    except Exception as e:
        logging.warning(f"Twitter 이미지 다운로드 실패 ({handle}): {e}")
        return None


def _save(key: str, data: bytes):
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    path = ASSETS_DIR / f"{key}.jpg"
    with open(path, "wb") as f:
        f.write(data)
    logging.info(f"이미지 저장: {path}")


def ensure_streamer_image(streamer) -> bool:
    if image_exists(streamer.key):
        return True

    uid = streamer.chzzk.get("uid", "")
    if uid:
        data = fetch_chzzk_image(uid)
        if data:
            _save(streamer.key, data)
            return True

    for item in streamer.links:
        url = item.get("url", "")
        if "x.com/" in url or "twitter.com/" in url:
            handle = url.rstrip("/").split("/")[-1]
            data = fetch_twitter_image(handle)
            if data:
                _save(streamer.key, data)
                return True

    logging.warning(f"이미지 없음: {streamer.key}")
    return False


def ensure_all_images(streamer_dict):
    for streamer in streamer_dict.values():
        ensure_streamer_image(streamer)
