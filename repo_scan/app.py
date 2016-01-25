from git import Repo

from repo_index.index import CommitSyncer
from repo_scan.cache import CacheManager
from repo_scan.config import get_config
from repo_scan.repo_utils import get_matching_repo_branches

config = get_config()


def _read_commits_from_repository(repo_config):
    repo = Repo(path=repo_config['repoPath'])

    if repo.bare:
        print("'%s' is not a valid Git repository" % repo_config['repoPath'])
        return

    _pull_from_remote(repo, repo_config)
    
    matching_branches_for_repo = get_matching_repo_branches(repo_config['branches'], repo.branches)

    if not matching_branches_for_repo:
        print("No matching branches found in repository '%s'" % repo_config['friendlyName'])

    for branch_name in matching_branches_for_repo:

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
        print("Sync of branch: '%s' in repo: '%s' is complete!" % (branch_name, repo_config['friendlyName']))

        if latest_commit_sha:
            cache_manager.write_commit_sha_for_branch(latest_commit_sha)


def _pull_from_remote(repo, repo_config):
    try:
        repo.remotes.origin.pull()
    except AttributeError:
        print("Repo '%s' has no remote origin" % (repo_config['friendlyName']))


def sync_repositories():
    for repo_config in config['repos']:
        _read_commits_from_repository(repo_config)


if __name__ == '__main__':
    sync_repositories()
