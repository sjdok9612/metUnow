import requests
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
        base_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(base_dir)
        token_path = os.path.join(parent_dir, "tokens", "youtube_token.txt")
        try:
            with open(token_path, "r", encoding="utf-8") as f:
                self.api_key = SecretString(f.read().strip())
        except FileNotFoundError:
            print("YouTube API 키 파일을 찾을 수 없습니다: tokens/youtube_token.txt")
            self.api_key = SecretString("")
        except Exception as e:
            print(f"API 키 로딩 중 오류: {e}")
            self.api_key = SecretString("")

    def get_key(self):
        return self.api_key.get()


def is_live(uid: str) -> bool:
    key = YoutubeAPI().get_key()
    if not key:
        return False
    try:
        params = {
            "part": "snippet",
            "channelId": uid,
            "eventType": "live",
            "type": "video",
            "key": key,
        }
        r = requests.get(
            YOUTUBE_SEARCH_URL,
            params=params,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=TIMEOUT,
        )
        r.raise_for_status()
        return len(r.json().get("items", [])) > 0
    except Exception:
        return False
