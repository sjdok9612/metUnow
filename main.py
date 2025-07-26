#main.py
from tool.mutex import check_mutex, release_mutex

import sys
import logging

logging.basicConfig(
    level=logging.INFO,  # DEBUG 이상의 로그만 출력
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    #
    ()   
    
if __name__ == "__main__":
    if check_mutex("Global\\MyApp_MeChuNow"):
        try:
            main()
        finally:
            release_mutex()
    else:
        print("프로그램이 이미 실행 중입니다. 종료합니다.")
        sys.exit(0)
