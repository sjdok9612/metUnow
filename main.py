#main.py
from tool.mutex import check_mutex, release_mutex

import sys
import logging

logging.basicConfig(
    level=logging.INFO,  # DEBUG 이상의 로그만 출력
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main(input_file: str, output_dir: str):
    if "venv" not in sys.executable:
        raise RuntimeError(f"❌ 가상환경이 아님! 경로: {sys.executable}")
    else:
        print("✅ 가상환경 사용 중:", sys.executable)
        print("Python 실행 경로:", sys.executable)

if __name__ == "__main__":
    # 중복 실행 방지
    if not check_mutex("Global\\MyApp_MeChuNow"):
        print("프로그램이 이미 실행 중입니다. 종료합니다.")
        sys.exit(0)

    exit_code = 0
    try:
        # 인수 확인
        if len(sys.argv) < 3:
            input_file = ".\\vods\\output_silent_10s.mp4"
            output_dir = ".\\vods\\"
            logging.info(f"argv 3개 미만, dump로 실행")
        else:
            input_file = sys.argv[1]
            output_dir = sys.argv[2]

        # 주요 처리
        main(input_file, output_dir)

    except Exception as e:
        logging.error(f"오류 발생: {e}")
        exit_code = 1

    finally:
        # 항상 실행됨 → mutex 해제
        release_mutex()

    # 종료 코드 반환
    sys.exit(exit_code)