from api.chzzk_api import get_channel_info as chzzk_get_channel_info, is_live as chzzk_is_live
from api.soop_api import get_channel_info as soop_get_channel_info, is_live as soop_is_live
from api.youtube_api import is_live as youtube_is_live
from tool.downloader import run_yt_dlp
from gui.notif import send_notification

import time
from notifypy import Notify
import logging


def updateLive(channels_status, update_event, live_download=True):
    last_checked = {channel.UID: 0 for channel in channels_status}

    while True:
        now = time.time()

        for channel in channels_status:
            UID = channel.UID
            platform = channel.main_platform.lower()

            # 체크 주기 설정
            check_interval = 300 if channel.is_live else 60
            time_since_last = now - last_checked[UID]

            # 아직 체크할 시간이 안 됐으면 skip
            if time_since_last > check_interval:
                # === 체크 시각 갱신 ===
                last_checked[UID] = now

                # === API 호출 ===
                try:
                    if platform == "chzzk":
                        liveFlag = chzzk_is_live(UID)
                    elif platform == "soop":
                        liveFlag = soop_is_live(UID)
                    elif platform == "youtube" :
                        liveFlag = youtube_is_live(UID)
                    else:
                        logging.warning(f"{channel.name} is_live ERROR")
                        continue
                except Exception as e:
                    logging.warning(f"{channel.name} API 호출 실패: {e}")
                    continue

                # 상태 변경 감지 시
                if liveFlag != channel.is_live:
                    
                    logging.info(f"{channel.name} 방송상태변경됌")
                    if liveFlag==True:
                        send_notification(f"{channel.nickname} 방송ON")
                    else:
                        send_notification(f"{channel.nickname} 방송OFF")
                logging.info(f"CHECK    {channel.name}  {liveFlag}")
                channel.is_live = liveFlag
                # 채널 간 간격 조절
                time.sleep(1)  # 너무 빠른 호출 방지
                update_event.set()
            else:
                logging.info(f"SKIP {channel.name} {time_since_last:3.1f} / {check_interval}")
                time.sleep(0.5)