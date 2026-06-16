#!/usr/bin/env bash
#
# DDLC After Story — Project Toolbox (Linux)
#
# Usage:
#   ./ddlc.sh <command> [args...]
#
# Commands:
#   detect          Check toolchain completeness
#   build-content   Build game content (sprites, backgrounds, audio)
#   build           Configure + compile the game
#   run             Build and launch the game
#   bundle          Full packaging pipeline → bundle/ddlc-<hash>/
#   clean           Remove build artifacts and caches
#   clean-all       Remove everything including content/
#   help            Show this help message

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PYTHON="${PYTHON:-python3}"
BUILD_DIR="${BUILD_DIR:-build}"
BUILD_TYPE="${BUILD_TYPE:-Release}"
JOBS="${JOBS:-$(nproc 2>/dev/null || echo 2)}"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

print_header() {
    echo -e "${CYAN}${BOLD}"
    echo "╔══════════════════════════════════════════════════════╗"
    echo "║        DDLC After Story — Project Toolbox           ║"
    echo "╚══════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_help() {
    print_header
    echo -e "  ${BOLD}Usage:${NC} ./ddlc.sh <command> [args...]"
    echo ""
    echo -e "  ${BOLD}Commands:${NC}"
    echo -e "    ${GREEN}detect${NC}          Check toolchain completeness"
    echo -e "    ${GREEN}build-content${NC}   Build game content (sprites, BG, audio)"
    echo -e "    ${GREEN}build${NC}           Configure + compile the game"
    echo -e "    ${GREEN}run${NC}             Build and launch the game"
    echo -e "    ${GREEN}bundle${NC}          Full packaging pipeline"
    echo -e "    ${GREEN}clean${NC}           Remove build artifacts and caches"
    echo -e "    ${GREEN}clean-all${NC}       Remove everything including content/"
    echo ""
    echo -e "  ${BOLD}Environment:${NC}"
    echo -e "    PYTHON        Python executable  (default: python3)"
    echo -e "    BUILD_DIR     Build directory     (default: build)"
    echo -e "    BUILD_TYPE    CMake build type    (default: Release)"
    echo -e "    JOBS          Parallel jobs       (default: nproc)"
    echo ""
}

cmd_detect() {
    echo -e "${CYAN}Running toolchain detection...${NC}"
    "$PYTHON" tools/compile/detection.py "$@"
}

cmd_build_content() {
    echo -e "${CYAN}Building game content...${NC}"
    "$PYTHON" tools/build_content.py "$@"
}

cmd_build() {
    echo -e "${CYAN}Configuring CMake...${NC}"

    local generator_flag=""
    if command -v ninja &>/dev/null; then
        generator_flag="-G Ninja"
    fi

    cmake -S . -B "$BUILD_DIR" \
        -DCMAKE_BUILD_TYPE="$BUILD_TYPE" \
        -DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
        $generator_flag

    echo -e "${CYAN}Building (${JOBS} jobs)...${NC}"
    cmake --build "$BUILD_DIR" --config "$BUILD_TYPE" --parallel "$JOBS"

    echo -e "${GREEN}Build complete!${NC}"
}

cmd_run() {
    cmd_build "$@"

    local exe="$BUILD_DIR/bin/ddlc_afterstory"
    if [ ! -f "$exe" ]; then
        exe=$(find "$BUILD_DIR" -name "ddlc_afterstory" -type f 2>/dev/null | head -n1)
    fi

    if [ -z "$exe" ] || [ ! -f "$exe" ]; then
        echo -e "${RED}ERROR: Executable not found after build.${NC}"
        exit 1
    fi

    echo -e "${GREEN}Launching: $exe${NC}"
    exec "$exe"
}

cmd_bundle() {
    echo -e "${CYAN}Starting packaging pipeline...${NC}"
    "$PYTHON" tools/bundle/package.py --build-type "$BUILD_TYPE" --jobs "$JOBS" "$@"
}

cmd_clean() {
    echo -e "${CYAN}Cleaning workspace...${NC}"
    "$PYTHON" tools/clean/clean.py "$@"
}

cmd_clean_all() {
    echo -e "${YELLOW}Cleaning workspace (including content/)...${NC}"
    "$PYTHON" tools/clean/clean.py --all "$@"
}

if [ $# -eq 0 ]; then
    print_help
    exit 0
fi

COMMAND="$1"
shift

case "$COMMAND" in
    detect)         cmd_detect "$@" ;;
    build-content)  cmd_build_content "$@" ;;
    build)          cmd_build "$@" ;;
    run)            cmd_run "$@" ;;
    bundle)         cmd_bundle "$@" ;;
    clean)          cmd_clean "$@" ;;
    clean-all)      cmd_clean_all "$@" ;;
    help|--help|-h) print_help ;;
    *)
        echo -e "${RED}Unknown command: $COMMAND${NC}"
        echo "Run './ddlc.sh help' for usage."
        exit 1
        ;;
esac
