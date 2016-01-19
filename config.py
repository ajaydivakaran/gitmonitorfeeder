import json


def get_config():
    with open('config.json') as json_data_file:
        config = json.load(json_data_file)
    return config
