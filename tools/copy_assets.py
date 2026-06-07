#!/usr/bin/env python3
"""
Copy background images and audio files from assets/ to content/.

Reads a manifest (tools/asset_manifest.json) that defines which files
to copy and where they should go. This keeps the content/ directory
lean and only includes what the game actually uses.

Usage:
    python tools/copy_assets.py [options]

Options:
    --assets-dir DIR     Source assets directory (default: assets/)
    --content-dir DIR    Destination content directory (default: content/)
    --manifest FILE      JSON manifest file (default: tools/asset_manifest.json)
    --dry-run            Show what would be done without copying
    --clean              Remove existing content images/audio before copying

All paths are relative to the project root (detected automatically).
"""

import argparse
import json
import shutil
import sys
from pathlib import Path


def find_project_root() -> Path:
    """Walk up from this script's location to find the project root."""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / "CMakeLists.txt").exists() and (current / "engine").exists():
            return current
        current = current.parent
    return Path(__file__).resolve().parent.parent


def copy_file(src: Path, dst: Path, dry_run: bool = False) -> bool:
    """Copy a single file, creating parent directories as needed."""
    if not src.exists():
        print(f"  MISSING: {src}")
        return False

    if dry_run:
        print(f"  [DRY-RUN] {src.name} -> {dst}")
        return True

    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Copy game assets from assets/ to content/."
    )
    parser.add_argument("--assets-dir", type=str, default=None,
                        help="Source assets directory")
    parser.add_argument("--content-dir", type=str, default=None,
                        help="Destination content directory")
    parser.add_argument("--manifest", type=str, default=None,
                        help="JSON manifest file")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show actions without copying")
    parser.add_argument("--clean", action="store_true",
                        help="Clean target directories before copying")
    args = parser.parse_args()

    project_root = find_project_root()
    assets_dir = Path(args.assets_dir) if args.assets_dir else project_root / "assets"
    content_dir = Path(args.content_dir) if args.content_dir else project_root / "content"
    manifest_file = Path(args.manifest) if args.manifest else project_root / "tools" / "asset_manifest.json"

    print("=== Asset Copy Tool ===")
    print(f"  Project root: {project_root}")
    print(f"  Assets dir:   {assets_dir}")
    print(f"  Content dir:  {content_dir}")
    print(f"  Manifest:     {manifest_file}")
    if args.dry_run:
        print(f"  Mode:         DRY-RUN")
    print()

    if not manifest_file.exists():
        print(f"Error: Manifest not found: {manifest_file}", file=sys.stderr)
        sys.exit(1)

    with open(manifest_file) as f:
        manifest = json.load(f)

    if args.clean and not args.dry_run:
        for subdir in ["images/bg", "audio/bgm", "audio/sfx"]:
            target = content_dir / subdir
            if target.exists():
                shutil.rmtree(target)
                print(f"  Cleaned: {target}")

    total_ok = 0
    total_missing = 0

    for section_name, entries in manifest.items():
        print(f"[{section_name.upper()}]")
        for entry in entries:
            src_path = assets_dir / entry["src"]
            dst_path = content_dir / entry["dst"]

            if copy_file(src_path, dst_path, args.dry_run):
                total_ok += 1
            else:
                total_missing += 1

    print(f"\n=== Total: {total_ok} copied, {total_missing} missing ===")

    if total_missing > 0:
        print("\nWARNING: Some source files were not found in assets/.")
        print("Make sure you have placed the original DDLC game assets in the assets/ directory.")
        sys.exit(1)


if __name__ == "__main__":
    main()
