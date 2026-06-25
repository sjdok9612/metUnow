import json
import logging
from tool.paths import CONFIG_JSON


def load_config(config_path=None) -> dict:
    config_path = config_path or CONFIG_JSON
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
            logging.info(f"Config 로딩 성공: {config}")
            return config
    except FileNotFoundError:
        logging.warning(f"Config 파일 없음: {config_path}")
        return {}
    except json.JSONDecodeError as e:
        logging.error(f"Config 파싱 오류: {e}")
        return {}
    except Exception as e:
        logging.error(f"Config 로딩 오류: {e}")
        return {}
