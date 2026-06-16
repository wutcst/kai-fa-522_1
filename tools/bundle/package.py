#!/usr/bin/env python3
"""
Package the DDLC After Story game into a distributable bundle.

Complete pipeline:
  1. Run toolchain detection (optional, --skip-check to bypass)
  2. Build game content (sprites, backgrounds, audio)
  3. Configure CMake
  4. Build the game binary
  5. Assemble bundle at bundle/ddlc-<hash>/

Usage:
    python tools/bundle/package.py [options]

Options:
    --skip-check        Skip toolchain detection
    --skip-content      Skip content building (use existing content/)
    --build-type TYPE   CMake build type: Release|Debug|RelWithDebInfo (default: Release)
    --generator GEN     CMake generator (default: auto-detect)
    --jobs N            Parallel build jobs (default: auto)
    --output-dir DIR    Override output directory (default: bundle/)
    --dry-run           Show steps without executing
"""

import argparse
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


def find_project_root() -> Path:
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / "CMakeLists.txt").exists() and (current / "engine").exists():
            return current
        current = current.parent
    return Path(__file__).resolve().parent.parent.parent


def get_short_hash(project_root: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short=8", "HEAD"],
            capture_output=True, text=True, cwd=str(project_root)
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except FileNotFoundError:
        pass
    return "unknown"


def detect_generator():
    system = platform.system()
    if system == "Windows":
        if shutil.which("ninja"):
            return "Ninja"
        return None
    else:
        if shutil.which("ninja"):
            return "Ninja"
        if shutil.which("make"):
            return "Unix Makefiles"
    return None


def detect_jobs() -> int:
    try:
        return os.cpu_count() or 2
    except Exception:
        return 2


def run_step(name: str, cmd: list, cwd: str, dry_run: bool = False) -> int:
    print(f"\n{'─'*60}")
    print(f"  Step: {name}")
    print(f"  Command: {' '.join(cmd)}")
    print(f"{'─'*60}\n")
    if dry_run:
        print("  [DRY-RUN] Skipped.")
        return 0
    result = subprocess.run(cmd, cwd=cwd)
    if result.returncode != 0:
        print(f"\n  ERROR: '{name}' failed with exit code {result.returncode}")
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description="Package the game into a bundle.")
    parser.add_argument("--skip-check", action="store_true", help="Skip toolchain check")
    parser.add_argument("--skip-content", action="store_true", help="Skip content build")
    parser.add_argument("--build-type", default="Release",
                        choices=["Release", "Debug", "RelWithDebInfo", "MinSizeRel"])
    parser.add_argument("--generator", default=None, help="CMake generator")
    parser.add_argument("--jobs", type=int, default=None, help="Parallel jobs")
    parser.add_argument("--output-dir", default=None, help="Bundle output directory")
    parser.add_argument("--dry-run", action="store_true", help="Preview without executing")
    args = parser.parse_args()

    project_root = find_project_root()
    build_dir = project_root / "build"
    jobs = args.jobs or detect_jobs()
    git_hash = get_short_hash(project_root)
    bundle_name = f"ddlc-{git_hash}"
    output_base = Path(args.output_dir) if args.output_dir else project_root / "bundle"
    bundle_dir = output_base / bundle_name

    print("╔══════════════════════════════════════════════════════════╗")
    print("║       DDLC After Story — Game Packaging Pipeline       ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"  Project:    {project_root}")
    print(f"  Build type: {args.build_type}")
    print(f"  Jobs:       {jobs}")
    print(f"  Git hash:   {git_hash}")
    print(f"  Bundle:     {bundle_dir}")
    if args.dry_run:
        print(f"  Mode:       DRY-RUN")

    # Step 1: Toolchain check
    if not args.skip_check:
        ret = run_step(
            "Toolchain Detection",
            [sys.executable, str(project_root / "tools" / "compile" / "detection.py")],
            str(project_root),
            dry_run=args.dry_run,
        )
        if ret != 0 and not args.dry_run:
            print("\nToolchain check failed. Fix issues or use --skip-check.")
            sys.exit(1)

    # Step 2: Build content
    if not args.skip_content:
        ret = run_step(
            "Build Content",
            [sys.executable, str(project_root / "tools" / "build_content.py")],
            str(project_root),
            dry_run=args.dry_run,
        )
        if ret != 0 and not args.dry_run:
            print("\nContent build failed.")
            sys.exit(1)

    # Step 3: CMake configure
    generator = args.generator or detect_generator()
    cmake_cmd = [
        "cmake", "-S", str(project_root), "-B", str(build_dir),
        f"-DCMAKE_BUILD_TYPE={args.build_type}",
        "-DCMAKE_POLICY_VERSION_MINIMUM=3.5",
    ]
    if generator:
        cmake_cmd += ["-G", generator]

    ret = run_step(
        "CMake Configure",
        cmake_cmd,
        str(project_root),
        dry_run=args.dry_run,
    )
    if ret != 0 and not args.dry_run:
        print("\nCMake configuration failed.")
        sys.exit(1)

    # Step 4: CMake build
    build_cmd = [
        "cmake", "--build", str(build_dir),
        "--config", args.build_type,
        "--parallel", str(jobs),
    ]

    ret = run_step(
        "CMake Build",
        build_cmd,
        str(project_root),
        dry_run=args.dry_run,
    )
    if ret != 0 and not args.dry_run:
        print("\nBuild failed.")
        sys.exit(1)

    # Step 5: Assemble bundle
    print(f"\n{'─'*60}")
    print(f"  Step: Assemble Bundle")
    print(f"{'─'*60}\n")

    if args.dry_run:
        print("  [DRY-RUN] Would assemble bundle to:")
        print(f"    {bundle_dir}/")
        print(f"    ├── ddlc_afterstory[.exe]")
        print(f"    └── content/")
    else:
        if bundle_dir.exists():
            shutil.rmtree(bundle_dir)
        bundle_dir.mkdir(parents=True, exist_ok=True)

        bin_dir = build_dir / "bin"
        if not bin_dir.exists():
            bin_dir = build_dir / "game" / args.build_type
        if not bin_dir.exists():
            bin_dir = build_dir / "game"

        exe_name = "ddlc_afterstory.exe" if platform.system() == "Windows" else "ddlc_afterstory"
        exe_src = None
        for candidate_dir in [build_dir / "bin", build_dir / "game" / args.build_type, build_dir / "game", build_dir]:
            candidate = candidate_dir / exe_name
            if candidate.exists():
                exe_src = candidate
                break

        if not exe_src:
            for match in build_dir.rglob(exe_name):
                exe_src = match
                break

        if exe_src:
            shutil.copy2(exe_src, bundle_dir / exe_name)
            print(f"  Copied: {exe_src.name}")
        else:
            print(f"  WARNING: Executable '{exe_name}' not found in build output.")
            print(f"  Searched in: {build_dir}")

        content_src = project_root / "content"
        content_dst = bundle_dir / "content"
        if content_src.exists():
            shutil.copytree(content_src, content_dst)
            print(f"  Copied: content/")
        else:
            print(f"  WARNING: content/ directory not found.")

        # Copy any required shared libraries on Linux
        if platform.system() != "Windows":
            for lib_pattern in ["*.so", "*.so.*"]:
                for lib in (build_dir / "bin").glob(lib_pattern) if (build_dir / "bin").exists() else []:
                    shutil.copy2(lib, bundle_dir / lib.name)
                    print(f"  Copied: {lib.name}")

    print(f"\n{'═'*60}")
    print(f"  Bundle ready: {bundle_dir}")
    print(f"{'═'*60}")


if __name__ == "__main__":
    main()
