from elasticsearch import Elasticsearch
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
        if len(self.max_buffer_size) > 0:
            self._flush_buffer()

    def _flush_buffer(self):
        self.es_client.bulk(index=_get_commit_index(self.config), doc_type='commit', body=self.buffer)
        self.buffer.clear()

    def _map(self, commit):
        return {
            '_source': {
                'repository': self.repo_config['friendlyName'],
                'branch': self.repo_branch_name,
                'message': commit.message,
                'pairs': self._identify_pairs(commit.message),
                'sha': commit.hexsha,
                '_id': commit.hexsha,
                'author': commit.author,
                'authordate': commit.authored_date,
                'committer': commit.committer,
                'commitdate': commit.committed_date
            }
        }

    def _identify_pairs(self, commit_message):
        return [contributor for contributor in self.repo_config['contributors'] if
                contributor.lower() in commit_message.lower()]


if __name__ == '__main__':
    create_index()
