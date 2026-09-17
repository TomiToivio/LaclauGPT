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
  if [[ ! -d "$target/.git" ]]; then
    echo "Missing repository: $target" >&2
    echo "Run scripts/bootstrap-modules.sh first." >&2
    exit 1
  fi
  echo "Updating $repo"
  git -C "$target" pull --ff-only
done
