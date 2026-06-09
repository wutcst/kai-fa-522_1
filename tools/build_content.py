#!/usr/bin/env python3
"""
Build all game content from source assets.

This is the main entry point for the content pipeline. It runs:
  1. copy_assets.py  — copies backgrounds and audio from assets/ to content/
  2. compose_sprites.py — composes character sprites from layer images

Usage:
    python tools/build_content.py [options]

Options:
    --clean      Remove existing content (images/audio) before building
    --dry-run    Show what would be done without writing anything
    --all        Compose ALL sprite combinations (not just those in sprites.json)

Prerequisites:
    - Place DDLC game assets in the assets/ directory
    - Install Pillow: pip install Pillow
"""

import argparse
import subprocess
import sys
from pathlib import Path


def find_project_root() -> Path:
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / "CMakeLists.txt").exists() and (current / "engine").exists():
            return current
        current = current.parent
    return Path(__file__).resolve().parent.parent


def run_tool(script: str, args: list, project_root: Path) -> int:
    cmd = [sys.executable, str(project_root / "tools" / "atlas_packer" / script)] + args
    print(f"\n{'='*60}")
    print(f"Running: {' '.join(cmd)}")
    print(f"{'='*60}\n")
    return subprocess.call(cmd, cwd=str(project_root))


def main():
    parser = argparse.ArgumentParser(description="Build all game content from assets.")
    parser.add_argument("--clean", action="store_true", help="Clean before building")
    parser.add_argument("--dry-run", action="store_true", help="Dry run mode")
    parser.add_argument("--all", action="store_true", help="Compose all sprite variants")
    args = parser.parse_args()

    project_root = find_project_root()

    print("=" * 60)
    print(" DDLC: After Story — Content Build Pipeline")
    print("=" * 60)
    print(f" Project: {project_root}")
    print(f" Assets:  {project_root / 'assets'}")
    print(f" Output:  {project_root / 'content'}")
    print("=" * 60)

    # Step 1: Copy backgrounds and audio
    copy_args = []
    if args.clean:
        copy_args.append("--clean")
    if args.dry_run:
        copy_args.append("--dry-run")

    ret = run_tool("copy_assets.py", copy_args, project_root)
    if ret != 0:
        print("\nERROR: Asset copy failed!", file=sys.stderr)
        sys.exit(ret)

    # Step 2: Compose character sprites
    sprite_args = []
    if args.dry_run:
        sprite_args.append("--dry-run")
    if args.all:
        sprite_args.append("--all")

    ret = run_tool("compose_sprites.py", sprite_args, project_root)
    if ret != 0:
        print("\nERROR: Sprite composition failed!", file=sys.stderr)
        sys.exit(ret)

    print("\n" + "=" * 60)
    print(" Content build complete!")
    print(" Run 'cmake --build build' to compile the game.")
    print("=" * 60)


if __name__ == "__main__":
    main()
