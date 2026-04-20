#!/usr/bin/env python3
import shutil
import sys
from pathlib import Path


def main(dest_dir):
    repo_root = Path(__file__).resolve().parent.parent
    template_dir = repo_root / 'starter' / 'template'
    dest = Path(dest_dir).resolve()
    if dest.exists():
        print(f"Destination {dest} already exists. Aborting.")
        sys.exit(1)
    shutil.copytree(template_dir, dest)
    print(f"Starter project created at: {dest}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: create_starter.py <destination_path>")
        sys.exit(2)
    main(sys.argv[1])
