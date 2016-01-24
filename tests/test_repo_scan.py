import unittest

from repo_scan.repo_utils import get_matching_repo_branches


class TestRepoScan(unittest.TestCase):

    def test_should_return_matching_branch_names(self):
        branch_patterns = ['master', 'rel-*']
        repository_branches = ['master', 'spike', 'release-12', 'release-13']

        matching_branch_names = get_matching_repo_branches(branch_patterns, repository_branches)

        self.assertEqual(matching_branch_names, ['master', 'release-12', 'release-13'])
