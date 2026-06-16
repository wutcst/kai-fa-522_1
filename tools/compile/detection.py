#!/usr/bin/env python3
"""
Toolchain completeness detection for the DDLC After Story project.

Checks:
  - CMake availability and version
  - Platform build tools (Make / Ninja on Linux, MSVC / MinGW on Windows)
  - Python availability and version
  - Git submodule initialization status
  - Whether the current branch is up-to-date with remote

Usage:
    python tools/compile/detection.py [--json] [--fix]

Options:
    --json    Output results as machine-readable JSON
    --fix     Attempt to auto-fix issues (e.g. run git submodule update)
"""

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

REQUIRED_CMAKE_VERSION = (3, 14)
REQUIRED_PYTHON_VERSION = (3, 8)

SUBMODULES = [
    "third_party/SDL",
    "third_party/SDL_image",
    "third_party/SDL_ttf",
    "third_party/SDL_mixer",
]


class Colors:
    OK = "\033[92m"
    WARN = "\033[93m"
    FAIL = "\033[91m"
    BOLD = "\033[1m"
    END = "\033[0m"

    @classmethod
    def disable(cls):
        cls.OK = cls.WARN = cls.FAIL = cls.BOLD = cls.END = ""


if os.name == "nt" or not sys.stdout.isatty():
    Colors.disable()


def find_project_root() -> Path:
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / "CMakeLists.txt").exists() and (current / "engine").exists():
            return current
        current = current.parent
    return Path(__file__).resolve().parent.parent.parent


def run_cmd(cmd: list, cwd: str = None) -> tuple:
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=15, cwd=cwd
        )
        return result.returncode, (result.stdout + result.stderr).strip()
    except FileNotFoundError:
        return -1, ""
    except subprocess.TimeoutExpired:
        return -2, "command timed out"


def parse_version(version_str: str) -> tuple:
    import re
    match = re.search(r"(\d+)\.(\d+)(?:\.(\d+))?", version_str)
    if match:
        parts = [int(x) for x in match.groups() if x is not None]
        return tuple(parts)
    return (0,)


def check_cmake() -> dict:
    result = {"name": "CMake", "found": False, "version": None, "ok": False, "detail": ""}
    path = shutil.which("cmake")
    if not path:
        result["detail"] = "cmake not found in PATH"
        return result

    result["found"] = True
    ret, output = run_cmd(["cmake", "--version"])
    if ret == 0:
        ver = parse_version(output.splitlines()[0])
        result["version"] = ".".join(str(v) for v in ver)
        result["ok"] = ver >= REQUIRED_CMAKE_VERSION
        if not result["ok"]:
            result["detail"] = (
                f"version {result['version']} < required "
                f"{'.'.join(str(v) for v in REQUIRED_CMAKE_VERSION)}"
            )
        else:
            result["detail"] = f"version {result['version']} at {path}"
    return result


def check_build_tools() -> dict:
    result = {"name": "Build Tools", "found": False, "version": None, "ok": False, "detail": ""}
    system = platform.system()

    if system == "Windows":
        for tool_name, cmd in [
            ("MSVC (cl.exe)", ["cl"]),
            ("MinGW (gcc)", ["gcc", "--version"]),
            ("Ninja", ["ninja", "--version"]),
        ]:
            path = shutil.which(cmd[0])
            if path:
                result["found"] = True
                result["ok"] = True
                ret, output = run_cmd(cmd)
                ver = parse_version(output) if ret == 0 else (0,)
                result["version"] = ".".join(str(v) for v in ver) if ver != (0,) else None
                result["detail"] = f"{tool_name} found at {path}"
                return result

        vswhere = (
            Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"))
            / "Microsoft Visual Studio" / "Installer" / "vswhere.exe"
        )
        if vswhere.exists():
            ret, output = run_cmd([
                str(vswhere), "-latest", "-property", "installationPath"
            ])
            if ret == 0 and output:
                result["found"] = True
                result["ok"] = True
                result["detail"] = f"Visual Studio found at {output}"
                return result

        result["detail"] = (
            "No build tool found. Install Visual Studio with C++ workload, "
            "MinGW, or Ninja."
        )
    else:
        for tool_name, cmd in [
            ("Make", ["make", "--version"]),
            ("Ninja", ["ninja", "--version"]),
        ]:
            path = shutil.which(cmd[0])
            if path:
                result["found"] = True
                result["ok"] = True
                ret, output = run_cmd(cmd)
                ver = parse_version(output) if ret == 0 else (0,)
                result["version"] = ".".join(str(v) for v in ver) if ver != (0,) else None
                result["detail"] = f"{tool_name} found at {path}"
                return result

        result["detail"] = "No build tool found. Install make or ninja."

    return result


def check_compiler() -> dict:
    result = {"name": "C++ Compiler", "found": False, "version": None, "ok": False, "detail": ""}
    system = platform.system()

    candidates = (
        [("cl", ["cl"]), ("g++", ["g++", "--version"]), ("clang++", ["clang++", "--version"])]
        if system == "Windows"
        else [("g++", ["g++", "--version"]), ("clang++", ["clang++", "--version"])]
    )

    for name, cmd in candidates:
        path = shutil.which(cmd[0])
        if path:
            result["found"] = True
            result["ok"] = True
            ret, output = run_cmd(cmd)
            ver = parse_version(output) if ret == 0 else (0,)
            result["version"] = ".".join(str(v) for v in ver) if ver != (0,) else None
            result["detail"] = f"{name} found at {path}"
            return result

    result["detail"] = "No C++ compiler found. Install g++, clang++, or MSVC."
    return result


def check_python() -> dict:
    result = {"name": "Python", "found": True, "version": None, "ok": False, "detail": ""}
    ver = sys.version_info[:3]
    result["version"] = ".".join(str(v) for v in ver)
    result["ok"] = ver >= REQUIRED_PYTHON_VERSION
    if result["ok"]:
        result["detail"] = f"version {result['version']} at {sys.executable}"
    else:
        result["detail"] = (
            f"version {result['version']} < required "
            f"{'.'.join(str(v) for v in REQUIRED_PYTHON_VERSION)}"
        )
    return result


def check_pillow() -> dict:
    result = {"name": "Pillow (Python)", "found": False, "version": None, "ok": False, "detail": ""}
    try:
        from PIL import Image
        import PIL
        result["found"] = True
        result["ok"] = True
        result["version"] = getattr(PIL, "__version__", "unknown")
        result["detail"] = f"version {result['version']}"
    except ImportError:
        result["detail"] = "Not installed. Run: pip install Pillow"
    return result


def check_submodules(project_root: Path, fix: bool = False) -> dict:
    result = {
        "name": "Git Submodules",
        "found": False,
        "ok": False,
        "detail": "",
        "submodules": {},
    }

    git_path = shutil.which("git")
    if not git_path:
        result["detail"] = "git not found in PATH"
        return result

    result["found"] = True
    all_ok = True

    for submod in SUBMODULES:
        submod_path = project_root / submod
        submod_ok = submod_path.exists() and any(submod_path.iterdir())
        result["submodules"][submod] = submod_ok
        if not submod_ok:
            all_ok = False

    if all_ok:
        result["ok"] = True
        result["detail"] = f"All {len(SUBMODULES)} submodules initialized"
    else:
        missing = [s for s, ok in result["submodules"].items() if not ok]
        result["detail"] = f"Missing/empty: {', '.join(missing)}"

        if fix:
            print(f"  {Colors.WARN}Attempting: git submodule update --init --recursive{Colors.END}")
            ret, output = run_cmd(
                ["git", "submodule", "update", "--init", "--recursive"],
                cwd=str(project_root),
            )
            if ret == 0:
                result["ok"] = True
                result["detail"] += " (fixed by auto-init)"
            else:
                result["detail"] += f" (auto-fix failed: {output})"

    return result


def check_branch_status(project_root: Path) -> dict:
    result = {
        "name": "Branch Status",
        "found": False,
        "ok": False,
        "detail": "",
        "branch": None,
        "ahead": 0,
        "behind": 0,
    }

    git_path = shutil.which("git")
    if not git_path:
        result["detail"] = "git not found in PATH"
        return result

    ret, branch = run_cmd(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=str(project_root)
    )
    if ret != 0:
        result["detail"] = "Not a git repository or git error"
        return result

    result["found"] = True
    result["branch"] = branch.strip()

    ret, _ = run_cmd(["git", "fetch", "--dry-run"], cwd=str(project_root))
    fetch_available = ret == 0

    ret, status = run_cmd(
        ["git", "status", "--porcelain", "-b"], cwd=str(project_root)
    )
    if ret != 0:
        result["detail"] = "Unable to get git status"
        return result

    import re
    first_line = status.splitlines()[0] if status else ""
    ahead_match = re.search(r"ahead (\d+)", first_line)
    behind_match = re.search(r"behind (\d+)", first_line)
    result["ahead"] = int(ahead_match.group(1)) if ahead_match else 0
    result["behind"] = int(behind_match.group(1)) if behind_match else 0

    if result["behind"] > 0:
        result["detail"] = (
            f"Branch '{result['branch']}' is {result['behind']} commit(s) behind remote"
        )
        if result["ahead"] > 0:
            result["detail"] += f" and {result['ahead']} ahead"
    elif result["ahead"] > 0:
        result["ok"] = True
        result["detail"] = (
            f"Branch '{result['branch']}' is {result['ahead']} commit(s) ahead of remote"
        )
    else:
        result["ok"] = True
        if not fetch_available:
            result["detail"] = (
                f"Branch '{result['branch']}' — no remote available to compare"
            )
        else:
            result["detail"] = f"Branch '{result['branch']}' is up-to-date with remote"

    return result


def print_result(r: dict):
    if r["ok"]:
        icon = f"{Colors.OK}✓{Colors.END}"
    elif r["found"]:
        icon = f"{Colors.WARN}⚠{Colors.END}"
    else:
        icon = f"{Colors.FAIL}✗{Colors.END}"

    ver = f" v{r['version']}" if r.get("version") else ""
    print(f"  {icon} {Colors.BOLD}{r['name']}{Colors.END}{ver}")
    if r["detail"]:
        print(f"    {r['detail']}")


def main():
    parser = argparse.ArgumentParser(description="Check toolchain completeness.")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--fix", action="store_true", help="Auto-fix issues")
    args = parser.parse_args()

    project_root = find_project_root()

    checks = [
        check_cmake(),
        check_compiler(),
        check_build_tools(),
        check_python(),
        check_pillow(),
        check_submodules(project_root, fix=args.fix),
        check_branch_status(project_root),
    ]

    if args.json:
        print(json.dumps({"project_root": str(project_root), "checks": checks}, indent=2))
        return

    print()
    print(f"{Colors.BOLD}═══ DDLC After Story — Toolchain Detection ═══{Colors.END}")
    print(f"  Project: {project_root}")
    print(f"  System:  {platform.system()} {platform.machine()}")
    print()

    for check in checks:
        print_result(check)
    print()

    all_ok = all(c["ok"] for c in checks)
    if all_ok:
        print(f"  {Colors.OK}{Colors.BOLD}All checks passed!{Colors.END} Ready to build.")
    else:
        failed = [c["name"] for c in checks if not c["ok"]]
        print(f"  {Colors.FAIL}{Colors.BOLD}Issues found:{Colors.END} {', '.join(failed)}")
        if not args.fix:
            print(f"  Run with --fix to attempt automatic fixes.")

    print()
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
