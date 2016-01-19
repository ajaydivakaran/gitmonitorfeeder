import os


class CacheManager:
    def __init__(self, cache_path, config, branch_name):
        self.cache_path = cache_path
        self.config = config
        self.branch_name = branch_name

    def get_commit_sha_for_branch(self):
        cache_file_path = self._get_cache_file_path()
        last_read_commit = None
        if os.path.isfile(cache_file_path):
            with open(cache_file_path, 'r') as file:
                last_read_commit = file.read()
        return last_read_commit

    def write_commit_sha_for_branch(self, commit_sha):
        cache_file_path = self._get_cache_file_path()
        with open(cache_file_path, 'w') as file:
            file.write(commit_sha)

    def _get_cache_file_path(self):
        cache_key = "%s-%s" % (self.config['friendlyName'], self.branch_name)
        cache_file_path = os.path.join(self.cache_path, cache_key)
        return cache_file_path
