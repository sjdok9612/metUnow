import json
from tool.creator import ChannelStatus

def load_channels_status(json_path="streamers.json") -> list[ChannelStatus]:
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            InfoFromJson = json.load(f)
    except FileNotFoundError:
        print("streamers.json 파일을 찾을 수 없습니다.")
        return []
    except json.JSONDecodeError as e:
        print(f"JSON 파싱 오류 발생: {e}")
        return []
    except Exception as e:
        print(f"알 수 없는 오류 발생: {e}")
        return []

    channels_status = []
    for creator in InfoFromJson:
        channel_status = ChannelStatus(
            name=creator.get("name", "알 수 없음"),
            nickname=creator.get("nickname", ""),
            main_platform=creator.get("mainPlatform", ""),
            UID=creator.get("UID", ""),
            fan_cafe=creator.get("FanCafe", ""),
            youtube=creator.get("Youtube", ""),
            chzzk_url=creator.get("Chzzk", ""),
            soop_url=creator.get("SOOP", ""),
            twitter_url=creator.get("Twitter", ""),
            is_live=False  # 초기값은 False, 이후 갱신
        )
        channels_status.append(channel_status)
    return channels_status
