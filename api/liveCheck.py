from PyQt6.QtCore import QThread, pyqtSignal
from api.chzzk_api import get_live_detail as chzzk_detail
from api.cime_api import get_live_detail as cime_detail, resolve_id as cime_resolve_id
import time
import logging


def _check_streamer(streamer) -> bool:
    live_info = None

    if streamer.chzzk:
        uid = streamer.chzzk.get("uid", "")
        if uid:
            detail = chzzk_detail(uid)
            if detail["title"]:
                streamer.live_title = detail["title"]
                streamer.live_category = detail["category"]
                streamer.live_since = detail["since"]
                streamer.live_end = detail.get("end", "")
            if detail["is_live"]:
                live_info = detail
            time.sleep(1)

    if streamer.cime:
        handle = streamer.cime.get("handle", "")
        if handle:
            channel_id = streamer.cime.get("id", "")
            if not channel_id:
                channel_id = cime_resolve_id(handle)
                if channel_id:
                    streamer.cime["id"] = channel_id
            if channel_id:
                detail = cime_detail(channel_id)
                if detail["is_live"] and not live_info:
                    live_info = detail
                time.sleep(1)

    if live_info:
        streamer.live_title = live_info["title"]
        streamer.live_category = live_info["category"]
        streamer.live_since = live_info["since"]

    return live_info is not None


class LiveCheckWorker(QThread):
    status_changed = pyqtSignal(str, bool)  # (key, is_live)
    first_poll_done = pyqtSignal()

    def __init__(self, streamer_dict):
        super().__init__()
        self._streamer_dict = streamer_dict
        self._running = True
        self._delay: dict[str, float] = {}

    def stop(self):
        self._running = False

    def add_streamer(self, key: str):
        self._delay[key] = 0.0

    def remove_streamer(self, key: str):
        self._delay.pop(key, None)

    def force_check_all(self):
        self._delay.clear()

    def run(self):
        _unchecked = set(self._streamer_dict.keys())
        _first_done = False

        while self._running:
            now = time.time()
            for streamer in list(self._streamer_dict.values()):
                if not self._running:
                    return

                check_interval = 180 if streamer.is_live else 60
                elapsed = now - self._delay.get(streamer.key, 0.0)

                if elapsed > check_interval:
                    self._delay[streamer.key] = now
                    try:
                        live_flag = _check_streamer(streamer)
                    except Exception as e:
                        logging.warning(f"{streamer.name} 체크 실패: {e}")
                        time.sleep(0.5)
                        continue

                    if not _first_done:
                        _unchecked.discard(streamer.key)
                        if not _unchecked:
                            _first_done = True
                            self.first_poll_done.emit()

                    if live_flag != streamer.is_live:
                        label = f"{streamer.name}{streamer.oshi_mark}"
                        status = "방송ON" if live_flag else "방송OFF"
                        logging.info(f"{label} → {status}")
                        streamer.is_live = live_flag
                        self.status_changed.emit(streamer.key, live_flag)

                    time.sleep(1)
                else:
                    logging.debug(
                        f"SKIP {streamer.name} {elapsed:.1f}s/{check_interval}s"
                    )
                    time.sleep(0.5)
