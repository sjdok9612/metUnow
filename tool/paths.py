import os
from pathlib import Path

DATA_DIR = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share")) / "metUnow"
ASSETS_DIR = DATA_DIR / "assets" / "streamers"
STREAMERS_JSON = DATA_DIR / "streamers.json"
CONFIG_JSON = DATA_DIR / "config.json"

def ensure_dirs():
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
