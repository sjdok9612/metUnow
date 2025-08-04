#main.py
from api.liveCheck import updateLive
from gui.app_window import AppWindow

from tool.Streamers import load_streamer_dict_from_json
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
    live_download = config.get("live_download", False)  # 기본 False
    
    streamer_dict = load_streamer_dict_from_json("streamers.json")    
    update_event = threading.Event()
    threading.Thread(target=updateLive, args=(streamer_dict, update_event,live_download), daemon=True).start()
    
    app = AppWindow(streamer_dict, update_event)
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
