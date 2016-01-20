import json
import os


def get_config():
    with open( os.path.join(os.path.dirname(os.path.dirname(__file__)), 'configs/config.json')) as json_data_file:
        config = json.load(json_data_file)
    return config
