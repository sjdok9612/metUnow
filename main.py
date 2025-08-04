#main.py
from api.liveCheck import updateLive
from gui.app_window import AppWindow

from tool.Streamers import load_streamers
from tool.config import load_config
from tool.mutex import check_mutex, release_mutex

import logging
import threading
import sys

logging.basicConfig(
    level=logging.INFO,  # DEBUG 이상의 로그만 출력
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    config = load_config()
    live_download = config.get("live_download", True)  # 기본 True
    
    Streamers = load_streamers("streamers.json")    
    update_event = threading.Event()
    threading.Thread(target=updateLive, args=(Streamers, update_event,live_download), daemon=True).start()
    
    app = AppWindow(Streamers, update_event)
    app.run()

if __name__ == "__main__":
    if check_mutex("Global\\MyApp_MeChuNow"):
        try:
            main()
        finally:
            release_mutex()
    else:
        print("프로그램이 이미 실행 중입니다. 종료합니다.")
        sys.exit(0)
