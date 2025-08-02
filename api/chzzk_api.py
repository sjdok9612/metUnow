import requests
import json

CHZZK_API_URL = "https://api.chzzk.naver.com/service/v1/channels/{}"
TIMEOUT = 5

def get_channel_info(uid: str) -> dict:
    try:
        #url = CHZZK_API_URL.format(nickname)
        url = CHZZK_API_URL.format(uid)
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=TIMEOUT)
        try:
            response.raise_for_status()  # HTTP 오류 체크
        except requests.RequestException as e:
            print(f"HTTP 오류 발생: {e}")
            return {}
        try:
            data = response.json()
        except ValueError as e:
            print(f"JSON Parse Error : {e}")
            return{}

        # #JSON 데이터를 들여쓰기 포함해서 예쁘게 출력
        # print(json.dumps(data, indent=4, ensure_ascii=False))
        return data.get("content", {})
    
    except requests.RequestException as e:
            print(f"네트워크 오류: {e}")
    except Exception as e:
        print(f"알 수 없는 오류: {e}")        
    return {}

def is_live(UID: str) -> bool:
    """
    치지직 방송 중인지 확인
    """
    try:
        url = CHZZK_API_URL.format(UID)
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=TIMEOUT)
        r.raise_for_status()
        data = r.json()
        return data.get("content", {}).get("openLive", False)
    except requests.RequestException:
        # 네트워크 오류 등
        return False
    except ValueError:
        # JSON 파싱 오류 등
        return False
    except Exception:
        # 기타 예외
        return False

def main():
    uid = "324423cf78e5f3cd04423453cf8f1299"  # 입력 대신 변수로 직접 지정
    #하쁘 79bc9b927d5c187f9d8fa5a56b194c37
    #루야 324423cf78e5f3cd04423453cf8f1299
    info = get_channel_info(uid)
    if not info:
        print("정보를 가져올 수 없습니다.")
        return
    print("main입니다")
    print(json.dumps(info, indent=4, ensure_ascii=False))
    print(is_live(uid))

    
if __name__ == "__main__":
    main()

# {
#     "channelId": "324423cf78e5f3cd04423453cf8f1299", 고유식별자
#     "channelName": "김루야", 닉네임
#     "channelImageUrl": "https://nng-phinf.pstatic.net/MjAyNTA0MjZfMjQx/MDAxNzQ1NjM2MTY1Njc1.1ytTvx2YWBVaq3bJ6d6G0ZSpvwKCC1zwGgEUsgfheusg.5WwMYM5zmamgqBrVtnJqCMLxHu0uuheoAo7gYmQd2TUg.JPEG/NNG-17456361649611756584535803917775.jpg",
#     "verifiedMark": false, 공식인증
#     "channelType": "STREAMING",
#     "channelDescription": "마인크래프트 일짱 버튜버\n💙미츄 소속 심해 탐사 잠수함 함장 김루땡💙",
#     "followerCount": 2501,
#     "openLive": true, 방송중?
#     "subscriptionAvailability": false,
#     "subscriptionPaymentAvailability": {
#         "iapAvailability": false,
#         "iabAvailability": false
#     },
#     "adMonetizationAvailability": false,
#     "activatedChannelBadgeIds": [],
#     "paidProductSaleAllowed": false
# }