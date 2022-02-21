import os
from pathlib import Path
import yaml


def read_config():
    env = os.getenv('GNELIST', 'local')
    path = Path('config', f'{env}.yml')
    if not path.exists():
        raise Exception('配置文件不存在！')
    with open(path) as f:
        config = yaml.safe_load(f.read())
        return config


conf = read_config()
