import re


def get_matching_repo_branches(branch_patterns, repo_branches):
    matching_branches = []
    for branch_pattern in branch_patterns:
        regex_branch_pattern = re.compile(branch_pattern)
        matching_branches_for_pattern = filter(regex_branch_pattern.match, repo_branches)
        matching_branches.extend(matching_branches_for_pattern)

    return matching_branches
