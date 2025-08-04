import requests
import json
import os

YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
TIMEOUT = 5
    
class SecretString:
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return "****"

    def __repr__(self):
        return "<SecretString ****>"

    def get(self):
        return self._value

class YoutubeAPI:
    def __init__(self):
        
        base_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 파일 위치
        if os.path.isfile(base_dir):#실행주체가 main.py일경우
            token_path = os.path.join(base_dir, "tokens", "youtube_token.txt")    
        else:
            parent_dir = os.path.dirname(base_dir)  # 그 상위 폴더
            token_path = os.path.join(parent_dir, "tokens", "youtube_token.txt")    
        
        try:
            with open(token_path, "r", encoding="utf-8") as f:
                raw_key = f.read().strip()
                self.api_key = SecretString(raw_key)
        except FileNotFoundError:
            print("API 키 파일을 찾을 수 없습니다")
            self.api_key = SecretString("")
        except Exception as e:
            print(f"API 키 로딩 중 오류: {e}")
            self.api_key = SecretString("")

    def get_key(self):
        return self.api_key.get()

def is_live(channel_id: str) -> bool:
    """
    channel_id : youtube uid, not handel name
    YouTube 채널에서 현재 라이브 방송 중인지 확인
    """
    api = YoutubeAPI()   # 인스턴스 생성
    key = api.get_key()
    try:
        params = {
            "part": "snippet",
            "channelId": channel_id,
            "eventType": "live",
            "type": "video",
            "key": key,
        }
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(YOUTUBE_SEARCH_URL, params=params, headers=headers, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()

        #items = data.get("items", [])
        #print("items:", json.dumps(items, indent=4, ensure_ascii=False))
        
        # items에 내용이 있으면 라이브 중
        return len(data.get("items", [])) > 0

    except requests.RequestException as e:
        print(f"요청 오류: {e}")
    except ValueError as e:
        print(f"JSON 파싱 오류: {e}")
    except Exception as e:
        print(f"기타 오류: {e}")

    return False


def main():
    # # 예시: 유튜브 채널 ID 넣어보세요
    
    #channel_id = "UCtLTQj-aLL3ov7AYEE2SofA"  #일반 버튜버 방송채널
    #channel_id = "UCF4Wxdo3inmxP-Y59wXDsFw"  #뉴스채널. 목적) 여러개의 라이브가 동시송출될때 응답의 구조 파악
    #channel_id ="UCJ46YTYBQVXsfsp8-HryoUA" #일반 버튜버 + 예약 라이브가 항상 달려있는채널 -> 예약라이브는 비어있는채로 나옴!
    channel_id ="UCPUcv2Zv9WhH6y8H1A9uWfg"
    if is_live(channel_id):
        print("라이브 중입니다!")
    else:
        print("현재 라이브중인지 파악 불가능!")


if __name__ == "__main__":
    main()
