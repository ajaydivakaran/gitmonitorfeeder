from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from repo_scan.config import get_config, get_es_index_config


def create_index():
    config = get_config()
    es = _get_es_client(config)
    es.indices.create(_get_commit_index(config), body=get_es_index_config())


def _get_es_client(config):
    es = Elasticsearch(config.get('esUrl', 'http://localhost:9200'))
    return es


def _get_commit_index(config):
    return config.get('indexName', 'repo_commits')


class CommitSyncer():
    def __init__(self, repo_config, repo_branch_name):
        self.config = get_config()
        self.repo_branch_name = repo_branch_name
        self.repo_config = repo_config
        self.max_buffer_size = self.config.get('batchSize', 20)
        self.buffer = []
        self.es_client = _get_es_client(self.config)

    def sync_commit(self, commit):

        self.buffer.append(self._map(commit))

        if len(self.buffer) >= self.max_buffer_size:
            self._flush_buffer()

    def flush(self):
        if len(self.buffer) > 0:
            self._flush_buffer()

    def _flush_buffer(self):
        bulk(self.es_client, self.buffer, stats_only=True)
        self.buffer.clear()

    def _map(self, commit):
        return {
            '_index': _get_commit_index(self.config),
            '_type': 'commit',
            '_source': {
                'repository': self.repo_config['friendlyName'],
                'branch': self.repo_branch_name,
                'message': commit.message,
                'pairs': self._identify_pairs(commit.message),
                'sha': commit.hexsha,
                'author_name': commit.author.name,
                'author_email': commit.author.email,
                'author_date': commit.authored_date,
                'committer_name': commit.committer.name,
                'committer_email': commit.committer.email,
                'commit_date': commit.committed_date
            }
        }

    def _identify_pairs(self, commit_message):
        return [contributor for contributor in self.repo_config['contributors'] if
                contributor.lower() in commit_message.lower()]
