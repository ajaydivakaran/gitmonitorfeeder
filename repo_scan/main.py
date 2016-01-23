import sys

from repo_index.index import create_index
from repo_scan.app import sync_repositories

actions = {
    'setup': lambda: create_index(),
    'sync': lambda: sync_repositories()
}

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] not in ['setup', 'sync']:
        print("Usage python main.py [setup|sync]")
        sys.exit(1)

    actions[sys.argv[1]]()
