#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

ROOT = Path.cwd()
EXCLUDES = {'.git', '__pycache__', 'data'}
TARGET_PREFIX = Path('src/fair_evaluator')

def find_duplicate_roots():
    duplicates = []
    for p in ROOT.glob('**/*'):
        if p.is_dir() and any(x in str(p) for x in ('A Sviluppo', 'Sviluppo')):
            duplicates.append(p)
    return duplicates

def migrate_one(src_dir: Path, dst: Path):
    if not src_dir.exists():
        return
    if not dst.exists():
        dst.mkdir(parents=True, exist_ok=True)
    for item in src_dir.iterdir():
        if item.name.startswith('.'): continue
        target = dst / item.name
        if item.is_dir():
            migrate_one(item, target)
        else:
            try:
                shutil.move(str(item), str(target))
            except Exception:
                pass

def main():
    duplicates = find_duplicate_roots()
    if not duplicates:
        print("No duplicate root paths found.")
        return
    print("Found duplicate root paths:")
    for d in duplicates:
        print(f" - {d}")
    # Simple heuristic: move contents to src/fair_evaluator if possible
    for d in duplicates:
        for child in d.iterdir():
            if child.name in ('src', 'app', 'tests', 'docs'):
                continue
        # Attempt to merge minimal items under new root
    print("Migration plan ready. Run this script again after reviewing paths to avoid data loss.")

if __name__ == '__main__':
    main()
