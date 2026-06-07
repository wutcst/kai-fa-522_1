#!/usr/bin/env python3
"""
Compose DDLC character sprites from individual layers into single images.

DDLC sprites are composite images assembled from three layers:
  - Left arm/body pose (e.g., 1l.png, 2l.png)
  - Right arm/body pose (e.g., 1r.png, 2r.png)
  - Face expression (e.g., a.png, b.png, ...)

This tool reads raw layers from the project's assets/ directory and outputs
composed sprites to content/images/characters/.

Usage:
    python tools/compose_sprites.py [options]

Options:
    --assets-dir DIR    Source assets directory (default: assets/images)
    --output-dir DIR    Output directory (default: content/images/characters)
    --characters CHARS  Comma-separated list of characters to process
                        (default: sayori,natsuki,yuri,monika)
    --sprites FILE      JSON file specifying which sprites to compose
                        (default: tools/sprites.json)
    --all               Compose ALL possible combinations (ignore sprites list)
    --dry-run           Print what would be done without writing files

All paths are relative to the project root (detected automatically).
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Error: Pillow is required. Install with: pip install Pillow", file=sys.stderr)
    sys.exit(1)


def find_project_root() -> Path:
    """Walk up from this script's location to find the project root (contains CMakeLists.txt)."""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / "CMakeLists.txt").exists() and (current / "engine").exists():
            return current
        current = current.parent
    return Path(__file__).resolve().parent.parent


POSE_DEFINITIONS = {
    "sayori": {
        "1": ("1l.png", "1r.png"),
        "2": ("1l.png", "2r.png"),
        "3": ("2l.png", "1r.png"),
        "4": ("2l.png", "2r.png"),
    },
    "natsuki": {
        "1": ("1l.png", "1r.png"),
        "2": ("1l.png", "2r.png"),
        "3": ("2l.png", "1r.png"),
        "4": ("2l.png", "2r.png"),
    },
    "yuri": {
        "1": ("1l.png", "1r.png"),
        "2": ("1l.png", "2r.png"),
        "3": ("2l.png", "1r.png"),
        "4": ("2l.png", "2r.png"),
    },
    "monika": {
        "1": ("1l.png", "1r.png"),
        "2": ("1l.png", "2r.png"),
        "3": ("2l.png", "1r.png"),
        "4": ("2l.png", "2r.png"),
    },
}


def compose_sprite(char_dir: Path, left_file: str, right_file: str,
                   face_file: str, output_path: Path, dry_run: bool = False) -> bool:
    """Compose a single sprite from three layers. Returns True on success."""
    left_path = char_dir / left_file
    right_path = char_dir / right_file
    face_path = char_dir / face_file

    for p in [left_path, right_path, face_path]:
        if not p.exists():
            return False

    if dry_run:
        print(f"  [DRY-RUN] Would compose: {output_path.name}")
        return True

    left = Image.open(left_path).convert("RGBA")
    right = Image.open(right_path).convert("RGBA")
    face = Image.open(face_path).convert("RGBA")

    result = Image.new("RGBA", left.size, (0, 0, 0, 0))
    result = Image.alpha_composite(result, left)
    result = Image.alpha_composite(result, right)
    result = Image.alpha_composite(result, face)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.save(output_path, "PNG")
    return True


def load_sprite_list(sprites_file: Path) -> dict:
    """Load the sprite specification from a JSON file."""
    if not sprites_file.exists():
        return {}
    with open(sprites_file) as f:
        return json.load(f)


def discover_all_sprites(char_dir: Path, character: str) -> list:
    """Discover all valid sprite combinations for a character."""
    poses = POSE_DEFINITIONS.get(character, {})
    if not poses:
        return []

    faces = sorted(
        p.stem for p in char_dir.iterdir()
        if p.suffix == ".png" and len(p.stem) <= 2 and p.stem.isalpha()
    )

    sprites = []
    for pose_num in sorted(poses.keys()):
        for face in faces:
            sprites.append(f"{pose_num}{face}")
    return sprites


def compose_character(character: str, sprites: list, assets_dir: Path,
                      output_dir: Path, dry_run: bool = False) -> tuple:
    """Compose all requested sprites for a character. Returns (ok_count, skip_count)."""
    char_dir = assets_dir / character
    out_dir = output_dir / character
    poses = POSE_DEFINITIONS.get(character, {})

    if not char_dir.exists():
        print(f"  WARNING: Asset directory not found: {char_dir}")
        return (0, len(sprites))

    ok = 0
    skipped = 0

    for sprite_id in sprites:
        pose_num = sprite_id[0]
        face_letter = sprite_id[1:]

        if pose_num not in poses:
            skipped += 1
            continue

        left_file, right_file = poses[pose_num]
        face_file = f"{face_letter}.png"
        output_path = out_dir / f"{sprite_id}.png"

        success = compose_sprite(char_dir, left_file, right_file, face_file, output_path, dry_run)
        if success:
            ok += 1
        else:
            skipped += 1

    return (ok, skipped)


def main():
    parser = argparse.ArgumentParser(
        description="Compose DDLC character sprites from layer images."
    )
    parser.add_argument("--assets-dir", type=str, default=None,
                        help="Source assets/images directory (default: <project>/assets/images)")
    parser.add_argument("--output-dir", type=str, default=None,
                        help="Output directory (default: <project>/content/images/characters)")
    parser.add_argument("--characters", type=str, default="sayori,natsuki,yuri,monika",
                        help="Comma-separated character list")
    parser.add_argument("--sprites", type=str, default=None,
                        help="JSON file with sprite specifications (default: tools/sprites.json)")
    parser.add_argument("--all", action="store_true",
                        help="Compose ALL possible combinations")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be done without writing files")
    args = parser.parse_args()

    project_root = find_project_root()
    assets_dir = Path(args.assets_dir) if args.assets_dir else project_root / "assets" / "images"
    output_dir = Path(args.output_dir) if args.output_dir else project_root / "content" / "images" / "characters"
    sprites_file = Path(args.sprites) if args.sprites else project_root / "tools" / "sprites.json"

    characters = [c.strip() for c in args.characters.split(",")]

    print(f"=== DDLC Sprite Composer ===")
    print(f"  Project root: {project_root}")
    print(f"  Assets dir:   {assets_dir}")
    print(f"  Output dir:   {output_dir}")
    print(f"  Characters:   {', '.join(characters)}")
    if args.dry_run:
        print(f"  Mode:         DRY-RUN")
    print()

    sprite_spec = {}
    if not args.all:
        sprite_spec = load_sprite_list(sprites_file)
        if not sprite_spec:
            print(f"  No sprites.json found at {sprites_file}, using --all mode.")
            args.all = True

    total_ok = 0
    total_skip = 0

    for character in characters:
        print(f"[{character.upper()}]")

        if args.all:
            sprites = discover_all_sprites(assets_dir / character, character)
        else:
            sprites = sprite_spec.get(character, [])

        if not sprites:
            print(f"  No sprites to compose.")
            continue

        ok, skip = compose_character(character, sprites, assets_dir, output_dir, args.dry_run)
        total_ok += ok
        total_skip += skip
        print(f"  Done: {ok} composed, {skip} skipped")

    print(f"\n=== Total: {total_ok} sprites composed, {total_skip} skipped ===")


if __name__ == "__main__":
    main()
