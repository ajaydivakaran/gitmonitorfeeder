import sys
from git import Repo

from repo_index.index import CommitSyncer
from repo_scan.cache import CacheManager
from repo_scan.config import get_config

config = get_config()


def _read_commits_from_repository(repo_config):
    repo = Repo(path=repo_config['repoPath'])

    if repo.bare:
        print("'%s' is not a valid Git repository" % repo_config['repoPath'])
        return

    _pull_from_remote(repo, repo_config)

    for branch_name in repo_config['branches']:

        if branch_name not in repo.branches:
            print("branch %s does not exist!" % branch_name)
            continue

        print("Commits in branch: %s" % branch_name)
        cache_manager = CacheManager(config['cachePath'], repo_config, branch_name)
        commit_syncer = CommitSyncer(repo_config, branch_name)
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
            print("-------------------")
            commit_syncer.sync_commit(commit)

        commit_syncer.flush()
        if latest_commit_sha:
            cache_manager.write_commit_sha_for_branch(latest_commit_sha)


def _pull_from_remote(repo, repo_config):
    try:
        repo.remotes.origin.pull()
    except AttributeError:
        print("Repo '%s' has no remote origin" % (repo_config['friendlyName']))


def _scan_repositories():
    for repo_config in config['repos']:
        _read_commits_from_repository(repo_config)
        
def main():
    run_option = sys.argv[1]
    _scan_repositories()

if __name__ == '__main__':    
    main()
