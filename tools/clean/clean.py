#!/usr/bin/env python3
"""
Clean build artifacts and temporary files from the project workspace.

Removes:
  - build/          CMake build directory
  - bin/            Binary output directory
  - cmake-build-*/  CLion / CMake IDE build directories
  - target/         Misc build output
  - bundle/         Packaged game bundles
  - __pycache__     Python bytecode caches (recursive)
  - *.pyc           Python compiled files (recursive)
  - .cache/         Generic tool cache

Usage:
    python tools/clean/clean.py [--dry-run] [--all]

Options:
    --dry-run   Show what would be deleted without removing anything
    --all       Also remove content/ (generated game content)
"""

import argparse
import shutil
import sys
from pathlib import Path


def find_project_root() -> Path:
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / "CMakeLists.txt").exists() and (current / "engine").exists():
            return current
        current = current.parent
    return Path(__file__).resolve().parent.parent.parent


TOP_LEVEL_DIRS = [
    "build",
    "bin",
    "target",
    "bundle",
    ".cache",
]

TOP_LEVEL_GLOBS = [
    "cmake-build-*",
]

EXTRA_DIRS = [
    "content",
]

RECURSIVE_PATTERNS = [
    "__pycache__",
]

RECURSIVE_FILE_PATTERNS = [
    "*.pyc",
    "*.pyo",
]


def remove_path(path: Path, dry_run: bool = False) -> bool:
    if not path.exists():
        return False
    label = "DIR " if path.is_dir() else "FILE"
    action = "[DRY-RUN] Would remove" if dry_run else "Removing"
    print(f"  {action} {label}: {path}")
    if not dry_run:
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
    return True


def main():
    parser = argparse.ArgumentParser(description="Clean project workspace.")
    parser.add_argument("--dry-run", action="store_true", help="Preview without deleting")
    parser.add_argument("--all", action="store_true", help="Also remove content/")
    args = parser.parse_args()

    root = find_project_root()
    print(f"=== Clean Workspace ===")
    print(f"  Project root: {root}")
    if args.dry_run:
        print(f"  Mode: DRY-RUN")
    print()

    removed = 0

    for name in TOP_LEVEL_DIRS:
        if remove_path(root / name, args.dry_run):
            removed += 1

    for pattern in TOP_LEVEL_GLOBS:
        for match in root.glob(pattern):
            if remove_path(match, args.dry_run):
                removed += 1

    if args.all:
        for name in EXTRA_DIRS:
            if remove_path(root / name, args.dry_run):
                removed += 1

    for pattern in RECURSIVE_PATTERNS:
        for match in root.rglob(pattern):
            if "third_party" in match.parts:
                continue
            if remove_path(match, args.dry_run):
                removed += 1

    for pattern in RECURSIVE_FILE_PATTERNS:
        for match in root.rglob(pattern):
            if "third_party" in match.parts:
                continue
            if remove_path(match, args.dry_run):
                removed += 1

    print()
    if removed == 0:
        print("  Nothing to clean — workspace is already tidy.")
    else:
        verb = "Would remove" if args.dry_run else "Removed"
        print(f"  {verb} {removed} item(s).")

    return 0


if __name__ == "__main__":
    sys.exit(main())
