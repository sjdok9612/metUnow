# config.py
import json
import logging

def load_config(config_path="config.json"):
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
            logging.info(f"Config 로딩 성공: {config}")
            return config
    except FileNotFoundError:
        logging.warning(f"Config 파일이 존재하지 않음: {config_path}")
    except json.JSONDecodeError as e:
        logging.error(f"Config 파싱 오류: {e}")
    except Exception as e:
        logging.error(f"Config 로딩 중 알 수 없는 오류: {e}")
    return {}