#.py
import json
from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class Streamer:
    index: int
    name: str
    oshi_mark: str
    live_url: str
    UID: str
    is_live: bool = False
    fan_cafe: str = ""
    youtube_url: str = ""
    twitter_url: str = ""
    extra_fields: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, data: dict, index: int):
        known_keys = {
            'name', 'oshi_mark', 'live_url', 'UID',
            'fan_cafe', 'youtube_url', 'twitter_url'
        }
        known_data = {k: data.get(k, "") for k in known_keys}
        known_data['index'] = index
        known_data['is_live'] = data.get('is_live', False)
        known_data['is_live'] = data.get('is_live', False)
        extra = {k: v for k, v in data.items() if k not in known_keys}
        known_data['extra_fields'] = extra
        return cls(**known_data)
   
def load_streamers(json_path="streamers.json") -> list[Streamer]:
    #     {
    #     "name": "",
    #     "oshi_mark": "",
    #     "main_platform": "",
    #     "UID": "",
    #     "fan_cafe": "",
    #     "youtube": "",
    #     "chzzk_url": "",
    #     "soop_url": "",
    #     "twitter_url": ""
    #     },
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
            oshi_mark=creator.get("oshi_mark", "오시마크 없음"),
            main_platform=creator.get("main_platform", ""),
            UID=creator.get("UID", ""),
            fan_cafe=creator.get("fan_cafe", ""),
            youtube=creator.get("youtube", ""),
            chzzk_url=creator.get("chzzk_url", ""),
            soop_url=creator.get("soop_url", ""),
            twitter_url=creator.get("twitter_url", ""),
            is_live=False  # 기본값
        )
        streamers.append(streamer)
    return streamers

def main():
    streamers = load_streamers("streamers.json")
    if streamers:
        print(f"총 {len(streamers)}명의 스트리머를 불러왔습니다.")
        for s in streamers:
            ()
    else:
        print("스트리머 목록이 비어있거나 불러오기 실패했습니다.")

if __name__ == "__main__":
    main()