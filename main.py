#main.py
from api.liveCheck import updateLive
from gui.app_window import AppWindow
from tool.channels import load_channels_status
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
    
    channels_status = load_channels_status()    
    update_event = threading.Event()
    threading.Thread(target=updateLive, args=(channels_status, update_event,live_download), daemon=True).start()
    
    app = AppWindow(channels_status, update_event)  # 이벤트 넘김
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
