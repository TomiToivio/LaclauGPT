#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORKSPACE_DIR="$(dirname "$ROOT_DIR")"

repos=(
  "LaclauGPT-Data-Collection"
  "LaclauGPT-Data-Analysis"
  "LaclauGPT-Data-Visualization"
)

for repo in "${repos[@]}"; do
  target="$WORKSPACE_DIR/$repo"
  if [[ ! -d "$target" ]]; then
    echo "Missing module repository: $target" >&2
    echo "Run scripts/bootstrap-modules.sh first." >&2
    exit 1
  fi
  echo "Installing $repo"
  python -m pip install -e "$target"
done
