import json
from logging import getLogger, config

def get_logger(name: str, json_path: str = None):
    if not json_pth is None:
        with open(json_path, 'r') as fd:
            log_conf = json.load(f)
            config.dictConfig(log_conf)
   
    return getLogger(name)

