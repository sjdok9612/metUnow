import sys
import json
import signal
import logging

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from gui.app_window import AppWindow
from tool.config import load_config
from tool.Streamers import load_streamer_dict_from_json
from tool.mutex import check_mutex, release_mutex
from tool.fetch_images import ensure_all_images
from tool.paths import ensure_dirs, CONFIG_JSON, STREAMERS_JSON

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

_DEFAULTS = {
    STREAMERS_JSON: [],
    CONFIG_JSON:    {"live_download": False},
}


def ensure_defaults():
    ensure_dirs()
    for path, default in _DEFAULTS.items():
        if not path.exists():
            path.write_text(json.dumps(default, ensure_ascii=False, indent=2))
            logging.info(f"최초 실행: {path.name} 생성됨")


def main():
    ensure_defaults()
    config = load_config()
    streamer_dict = load_streamer_dict_from_json()

    ensure_all_images(streamer_dict)

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setStyleSheet(
        "QToolTip { color:#ddd; background:#1e1e1e; border:1px solid #444;"
        "padding:5px; font-size:12px; }"
    )

    signal.signal(signal.SIGINT, lambda *_: app.quit())
    sig_timer = QTimer()
    sig_timer.start(300)
    sig_timer.timeout.connect(lambda: None)

    window = AppWindow(streamer_dict)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    if check_mutex():
        try:
            main()
        finally:
            release_mutex()
    else:
        print("프로그램이 이미 실행 중입니다.")
        sys.exit(0)
