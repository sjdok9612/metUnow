import requests
import json

SOOP_API = "https://live.sooplive.co.kr/afreeca/player_live_api.php"
AFREECA_API = "https://live.afreecatv.com/afreeca/player_live_api.php"
TIMEOUT = 5

def get_channel_info(uid: str) -> dict:
    payload = {
        "bid": uid,
        "bno": "null",
        "type": "live",
        "pwd": "",
        "player_type": "html5",
        "stream_type": "common",
        "quality": "HD",
        "mode": "landing",
        "from_api": "0",
        "is_revive": "false",
    }
    
    try:
        res = requests.post(
            SOOP_API,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=payload,
            timeout=TIMEOUT
        )
        res.raise_for_status()
        ch = res.json().get("CHANNEL", {})
        return {
            "title": ch.get("TITLE", ""),
            "is_live": ch.get("STATE") == "live",
            "bj_nickname": ch.get("BJ_NICK", ""),
            "viewer": ch.get("VIEWER", 0),
            "thumbnail": ch.get("THUMBNAIL", ""),
            "stream_url": ch.get("STREAM", "")
        }
    except Exception as e:
        print(f"[ERROR] soop 방송 정보 요청 실패: {e}")
        return {
            "title": "",
            "is_live": False,
            "bj_nickname": "",
            "viewer": 0,
            "thumbnail": "",
            "stream_url": ""
        }

def is_live(uid: str) -> bool:
    api_url = SOOP_API
    payload = {
        "bid": uid,
        "bno": "null",
        "type": "live",
        "pwd": "",
        "player_type": "html5",
        "stream_type": "common",
        "quality": "HD",
        "mode": "landing",
        "from_api": "0",
        "is_revive": "false",
    }
    try:
        r = requests.post(api_url, headers={"Content-Type": "application/x-www-form-urlencoded"}, data=payload, timeout=TIMEOUT)
        r.raise_for_status()
        data = r.json()
        bno = int(data.get("CHANNEL", {}).get("BNO", 0))
        return bno > 0
    except Exception:
        return False



def main():
    #uid="2omong"
    uid="razvlup"
    print("main입니다")
    info = get_channel_info(uid)
    print(json.dumps(info, indent=4, ensure_ascii=False))
    print(is_live(uid))
    
if __name__ == "__main__":
    main()