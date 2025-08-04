from api.chzzk_api import get_channel_info as chzzk_get_channel_info, is_live as chzzk_is_live
from api.soop_api import get_channel_info as soop_get_channel_info, is_live as soop_is_live
from api.youtube_api import is_live as youtube_is_live
from tool.downloader import run_yt_dlp
from gui.notif import send_notification

import time
from notifypy import Notify
import logging

def detect_platform(url: str) -> str:
    if "chzzk.naver.com" in url:
        return "chzzk"
    elif "play.sooplive.co.kr" in url:
        return "soop"
    elif "youtube.com" in url:
        return "youtube"
    else:
        return "unknown"

def updateLive(streamer_dict, update_event, live_download=False):
    streamer_delay: dict[str, float] = {streamer.uid: 0.0 for streamer in streamer_dict.values()}
    while True:
        now = time.time()
        for streamer in streamer_dict.values():
            uid = streamer.uid
            platform = detect_platform(streamer.live_url)
            
            # 체크 주기 설정
            check_interval = 300 if streamer.is_live else 60
            time_since_last = now - streamer_delay[uid]

            # 아직 체크할 시간이 안 됐으면 skip
            if time_since_last > check_interval:
                # === 체크 시각 갱신 ===
                streamer_delay[uid] = now

                # === API 호출 ===
                try:
                    if platform == "chzzk":
                        liveFlag = chzzk_is_live(uid)
                    elif platform == "soop":
                        liveFlag = soop_is_live(uid)
                    elif platform == "youtube" :
                        liveFlag = youtube_is_live(uid)
                    else:
                        logging.warning(f"{streamer.name} is_live ERROR")
                        continue
                except Exception as e:
                    logging.warning(f"{streamer.name} API 호출 실패: {e}")
                    continue

                # 상태 변경 감지 시
                if liveFlag != streamer.is_live:
                    
                    logging.info(f"{streamer.name}{streamer.get_extra_field('oshi_mark')} 방송상태변경됌")
                    if liveFlag==True:
                        send_notification(f"{streamer.name}{streamer.get_extra_field('oshi_mark')} 방송ON")
                    else:
                        send_notification(f"{streamer.name}{streamer.get_extra_field('oshi_mark')} 방송OFF")
                logging.info(f"CHECK    {streamer.name}  {liveFlag}")
                streamer.is_live = liveFlag
                # 채널 간 간격 조절
                time.sleep(1)  # 너무 빠른 호출 방지
                update_event.set()
            else:
                logging.info(f"SKIP {streamer.name} {time_since_last:3.1f} / {check_interval}")
                time.sleep(0.5)