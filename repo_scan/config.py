import json
import os


def get_config():
    return _get_config('configs/config.json')


def get_es_index_config():
    return _get_config('es_config/index_configuration.json')


def _get_config(config_file):
    with open(_get_full_path(config_file)) as json_data_file:
        config = json.load(json_data_file)
    return config


def _get_full_path(config_file):
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), config_file)
