#main.py
from tool.mutex import check_mutex, release_mutex
from tool.download import download_video
from tool.extract_audio import extract_audio

import sys
import logging

video_url ='https://chzzk.naver.com/video/8440544'

logging.basicConfig(
    level=logging.DEBUG,  #CRITICAL ERROR WARNING INFO DEBUG  /NOTEST(전부)
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    if "venv" not in sys.executable:
        logging.debug(f"❌ 가상환경이 아님! 경로: {sys.executable}")
    else:
        print("✅ 가상환경 사용 중:", sys.executable)
    if not video_url.strip():
        logging.debug("video_url이 비어 있어 다운로드를 건너뜁니다.")
    else:
        video_name = download_video(video_url)
    extract_audio(video_name)
    
if __name__ == "__main__":
    # 중복 실행 방지
    if not check_mutex("Global\\MyApp_MeChuNow"):
        logging.debug("프로그램이 이미 실행 중입니다. 종료합니다.")
        sys.exit(0)
    exit_code = 0
    try:
        # 주요 처리
        main()
    except Exception as e:
        logging.error(f"오류 발생: {e}")
        exit_code = 1
    finally:
        # 항상 실행됨 → mutex 해제
        release_mutex()