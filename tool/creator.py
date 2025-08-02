#creator.py
from dataclasses import dataclass

@dataclass
class ChannelStatus:
    name: str           #기본이름
    nickname: str       #오시마크붙은 닉네임
    main_platform: str  #메인플랫폼
    UID: str            #유저이름
    fan_cafe: str       #팬카페주소
    youtube: str        #유튜브주소
    chzzk_url: str      #치지직주소
    soop_url: str       #숲주소
    twitter_url: str    #트위터주소
    is_live: bool = False  # 방송 온오프 여부, 기본 False