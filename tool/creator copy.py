#stramers.py

import json

class Streamer:
    def __init__(
        self,
        index: int,
        name: str,
        oshi_mark: str,
        main_platform: str,
        UID: str,
        fan_cafe: str,
        youtube: str,
        chzzk_url: str,
        soop_url: str,
        twitter_url: str,
        is_live: bool = False
    ):
        self._index = index
        self._name = name
        self._oshi_mark = oshi_mark
        self._address = address
        self._main_platform = main_platform
        self._UID = UID
        self._fan_cafe = fan_cafe
        self._youtube = youtube
        self._chzzk_url = chzzk_url
        self._soop_url = soop_url
        self._twitter_url = twitter_url
        self.is_live = is_live
    
    @property
    def index(self):
        return self._index

    @property
    def name(self):
        return self._name

    @property
    def oshi_mark(self):
        return self._oshi_mark

    @property
    def main_platform(self):
        return self._main_platform

    @property
    def UID(self):
        return self._UID

    @property
    def fan_cafe(self):
        return self._fan_cafe

    @property
    def youtube(self):
        return self._youtube

    @property
    def chzzk_url(self):
        return self._chzzk_url

    @property
    def soop_url(self):
        return self._soop_url

    @property
    def twitter_url(self):
        return self._twitter_url

def load_streamers(json_path="streamers.json") -> list[Streamer]:
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("streamers.json 파일을 찾을 수 없습니다.")
        return []
    except json.JSONDecodeError as e:
        print(f"JSON 파싱 오류 발생: {e}")
        return []
    except Exception as e:
        print(f"알 수 없는 오류 발생: {e}")
        return []

    streamers = []
    for i, creator in enumerate(data):
        streamer = Streamer(
            index=i,
            name=creator.get("name", "알 수 없음"),
            oshi_mark=creator.get("oshi_mark", ""),
            main_platform=creator.get("mainPlatform", ""),
            UID=creator.get("UID", ""),
            fan_cafe=creator.get("FanCafe", ""),
            youtube=creator.get("Youtube", ""),
            chzzk_url=creator.get("Chzzk", ""),
            soop_url=creator.get("SOOP", ""),
            twitter_url=creator.get("Twitter", ""),
            is_live=False  # 기본값
        )
        streamers.append(streamer)
    return streamers

def main():
    ()

if __name__ == "__main__":
    main()
    

# from dataclasses import dataclass

# @dataclass
# class ChannelStatus:
#     name: str           #기본이름
#     oshi_mark: str       #오시마크
#     main_platform: str  #메인플랫폼
#     UID: str            #유저이름
#     fan_cafe: str       #팬카페주소
#     youtube: str        #유튜브주소
#     chzzk_url: str      #치지직주소
#     soop_url: str       #숲주소
#     twitter_url: str    #트위터주소
#     is_live: bool = False  # 방송 온오프 여부, 기본 False
    
    