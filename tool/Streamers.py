import json
from dataclasses import dataclass, field
from typing import Dict
from tool.paths import STREAMERS_JSON


@dataclass
class Streamer:
    key: str
    name: str
    oshi_mark: str = ""
    is_live: bool = False
    chzzk: Dict[str, str] = field(default_factory=dict)
    cime: Dict[str, str] = field(default_factory=dict)
    links: list = field(default_factory=list)
    live_title: str = ""
    live_category: str = ""
    live_since: str = ""
    live_end: str = ""

    def chzzk_live_url(self) -> str:
        uid = self.chzzk.get("uid", "")
        return f"https://chzzk.naver.com/live/{uid}" if uid else ""

    def cime_live_url(self) -> str:
        handle = self.cime.get("handle", "")
        return f"https://ci.me/@{handle}/live" if handle else ""

    @classmethod
    def from_dict(cls, data: dict) -> "Streamer":
        return cls(
            key=data.get("key", ""),
            name=data.get("name", ""),
            oshi_mark=data.get("oshi_mark", ""),
            is_live=False,
            chzzk=data.get("chzzk", {}),
            cime=data.get("cime", {}),
            links=data.get("links", {}),
        )

    def to_dict(self) -> dict:
        d: dict = {"key": self.key, "name": self.name, "oshi_mark": self.oshi_mark}
        if self.chzzk:
            d["chzzk"] = self.chzzk
        if self.cime:
            d["cime"] = self.cime
        if self.links:
            d["links"] = self.links
        return d


def load_streamer_dict_from_json(json_path=None) -> Dict[str, Streamer]:
    json_path = json_path or STREAMERS_JSON
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data_list = json.load(f)
    except FileNotFoundError:
        return {}
    return {
        data.get("key", f"unknown_{i}"): Streamer.from_dict(data)
        for i, data in enumerate(data_list)
    }


def save_streamers_to_json(streamer_dict: Dict[str, Streamer], json_path=None):
    json_path = json_path or STREAMERS_JSON
    data_list = [s.to_dict() for s in streamer_dict.values()]
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data_list, f, ensure_ascii=False, indent=2)
