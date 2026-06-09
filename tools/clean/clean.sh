#!/usr/bin/env bash
# Clean build artifacts and temporary files (Linux/macOS)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "=== Clean Workspace (bash) ==="
echo "  Project root: $PROJECT_ROOT"
echo

removed=0

remove_dir() {
    local target="$1"
    if [ -d "$target" ]; then
        echo "  Removing DIR: $target"
        rm -rf "$target"
        ((removed++))
    fi
}

remove_dir "$PROJECT_ROOT/build"
remove_dir "$PROJECT_ROOT/bin"
remove_dir "$PROJECT_ROOT/target"
remove_dir "$PROJECT_ROOT/bundle"
remove_dir "$PROJECT_ROOT/.cache"

for d in "$PROJECT_ROOT"/cmake-build-*; do
    [ -d "$d" ] && remove_dir "$d"
done

# Recursive cleanup of __pycache__ and .pyc files (skip third_party)
while IFS= read -r -d '' dir; do
    echo "  Removing DIR: $dir"
    rm -rf "$dir"
    ((removed++))
done < <(find "$PROJECT_ROOT" -name "__pycache__" -type d -not -path "*/third_party/*" -print0 2>/dev/null)

while IFS= read -r -d '' f; do
    echo "  Removing FILE: $f"
    rm -f "$f"
    ((removed++))
done < <(find "$PROJECT_ROOT" \( -name "*.pyc" -o -name "*.pyo" \) -type f -not -path "*/third_party/*" -print0 2>/dev/null)

echo
if [ "$removed" -eq 0 ]; then
    echo "  Nothing to clean — workspace is already tidy."
else
    echo "  Removed $removed item(s)."
fi
