from git import Repo

from repo_scan.cache import CacheManager
from repo_scan.config import get_config

config = get_config()


def _read_commits_from_repository(repo_config):
    repo = Repo(path=repo_config['repoPath'])

    if repo.bare:
        print("'%s' is not a valid Git repository" % repo_config['repoPath'])
        return

    for branch_name in repo_config['branches']:

        if branch_name not in repo.branches:
            print("branch %s does not exist!" % branch_name)
            continue

        print("Commits in branch: %s" % branch_name)
        cache_manager = CacheManager(config['cachePath'], repo_config, branch_name)
        latest_commit_sha = None
        for index, commit in enumerate(repo.iter_commits(branch_name)):

            if cache_manager.get_commit_sha_for_branch() == commit.hexsha:
                break

            if index == 0:
                latest_commit_sha = commit.hexsha

            print("Commit #: %d" % (index + 1))
            print("Commit message: %s" % commit.message)
            print("SHA: %s" % commit.hexsha)
            print("Author: %s" % commit.author)
            print("Author Date: %s" % commit.authored_date)
            print("Committer: %s" % commit.committer)
            print("Commit Date: %s" % commit.committed_date)
            print("Count: %s" % commit.count())
            print("-------------------")

        if latest_commit_sha:
            cache_manager.write_commit_sha_for_branch(latest_commit_sha)


def _scan_repositories():
    for repo_config in config['repos']:
        _read_commits_from_repository(repo_config)

if __name__ == '__main__':
    _scan_repositories()
