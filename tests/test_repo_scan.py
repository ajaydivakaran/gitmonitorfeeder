import unittest
from unittest.mock import Mock

from repo_scan.repo_utils import get_matching_repo_branches


def create_mock_branch(branch_name):
    mock = Mock()
    mock.name = branch_name
    return mock


class TestRepoScan(unittest.TestCase):
    def test_should_return_matching_branch_names(self):
        branch_patterns = ['master', 'rel-*']
        repository_branches = [create_mock_branch('master'), create_mock_branch('spike'),
                               create_mock_branch('release-12'), create_mock_branch('release-13')]

        matching_branch_names = get_matching_repo_branches(branch_patterns, repository_branches)

        self.assertEqual(matching_branch_names, ['master', 'release-12', 'release-13'])
