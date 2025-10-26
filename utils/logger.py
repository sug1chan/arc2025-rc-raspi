import json
from logging import getLogger, config

def get_logger(name: str, json_path: str = None):
    if not json_path is None:
        with open(json_path, 'r') as fd:
            log_conf = json.load(fd)
            config.dictConfig(log_conf)
   
    return getLogger(name)

