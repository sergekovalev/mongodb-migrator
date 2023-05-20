import os
import json
import re
from .constants import CONFIG_FILE_NAME, CONFIG_FILE_TEMPLATE


class ConfigManager(object):
    @staticmethod
    def init_config():
        if not os.path.exists(CONFIG_FILE_NAME):
            conf = json.dumps(CONFIG_FILE_TEMPLATE, indent=4)
            
            with open(CONFIG_FILE_NAME, 'w') as f:
                f.write(conf)

    @staticmethod
    def read_config() -> dict:
        def load_env_var(filename: str, varname: str) -> str:
            with open(filename, 'r') as f:
                m = re.match(r'var\s=\s(.+)', f.read())

                if not m:
                    raise Exception(f'Cannot parse {varname} variable from file {filename}')

                return m[1]

        with open(CONFIG_FILE_NAME, 'r') as f:
            cfg = json.loads(f.read())

        for k, v in cfg['connection'].items():
            if v and re.match(r'^.+\[.+\]$', v):
                file, var = re.sub(r'[\[\]]', ' ', v).strip().split(' ')
                cfg['connection'][k] = load_env_var(file, var)

        return cfg

    @staticmethod
    def init_dist(dist: str):
        if not os.path.exists(dist):
            os.mkdir(dist)
