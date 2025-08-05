#.py
from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class Streamer:
    key: str
    name: str
    live_url: str
    uid: str
    is_live: bool = False
    extra_fields: Dict[str, Any] = field(default_factory=dict)
    
    def get_extra_field(self, key: str, default=None):
        """contents ch = hebi.get_extra_field('youtube_contents_url')"""
        return self.extra_fields.get(key, default)
    
    """
    def :key, name, live_url, uid, is_live
    others: oshi_mark, youtube_url, official_community_url, twitter_url,
     soop_url,chzzk_url,youtube_contents_url,youtube_music_url,
    """

    @classmethod
    def from_dict(cls, data: dict, index: int = 0):
        return cls(
            key=data.get('key', ''),
            name=data.get('name', ''),
            live_url=data.get('live_url', ''),
            uid=data.get('uid', ''),
            is_live=False,
            extra_fields=data.get('extra', {}) or {}
        )

def load_streamer_dict_from_json(json_path="streamers.json") -> Dict[str, Streamer]:
    import json
    with open(json_path, 'r', encoding='utf-8') as f:
        data_list = json.load(f)
    streamer_dict = {
        data.get('key', f'unknown_{idx}'): Streamer.from_dict(data, idx)
        for idx, data in enumerate(data_list)
    }
    return streamer_dict

def main():
    streamer_dict = load_streamer_dict_from_json()
    if streamer_dict:
        print(f"총 {len(streamer_dict)}명의 스트리머를 불러왔습니다.")
        # 키와 객체 출력
        for key, streamer in streamer_dict.items():
            print(f"{key}: {streamer}")
    
    #키를 통한 extra pop
    print("키값을 통한 접근검증")
    print(f"hebi의 팬카페 : {streamer_dict['hebi'].get_extra_field('fan_cafe')}")
    print("팬카페 값 검증")
    print("yes" if streamer_dict['hebi'].get_extra_field('fan_cafe') is None else "no")
    print(f"hebi의 유튜브 : {streamer_dict['hebi'].get_extra_field('youtube_url')}")
    print(f"hebi의 uid : {streamer_dict['hebi'].uid}")
        
if __name__ == "__main__":
    main()