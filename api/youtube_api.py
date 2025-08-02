import requests

YOUTUBE_API_KEY = "YOUR_API_KEY"  # ← 여기에 너의 유튜브 API 키를 넣어줘
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
TIMEOUT = 5


def is_youtube_live(channel_id: str) -> bool:
    """
    YouTube 채널에서 현재 라이브 방송 중인지 확인
    """
    try:
        params = {
            "part": "snippet",
            "channelId": channel_id,
            "eventType": "live",
            "type": "video",
            "key": YOUTUBE_API_KEY,
        }
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(YOUTUBE_SEARCH_URL, params=params, headers=headers, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()

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
    # 예시: Kim Luya 유튜브 채널 ID 넣어보세요
    channel_id = "UCABCDEF1234567890"  # ← 너가 확인할 유튜브 채널 ID
    if is_youtube_live(channel_id):
        print("라이브 중입니다!")
    else:
        print("현재 라이브가 아닙니다.")


if __name__ == "__main__":
    main()
