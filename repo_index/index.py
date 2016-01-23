
from elasticsearch import Elasticsearch
from repo_scan.config import get_config, get_es_index_config


def create_index():
    config = get_config()
    es = Elasticsearch(config.get('es_url', 'http://localhost:9200'))
    es.indices.create('repo_commits', body=get_es_index_config())


if __name__ == '__main__':
    create_index()