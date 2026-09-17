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
  if [[ -d "$target/.git" ]]; then
    echo "Already present: $target"
    continue
  fi
  if [[ -e "$target" ]]; then
    echo "Refusing to overwrite existing non-Git path: $target" >&2
    exit 1
  fi
  git clone "https://github.com/TomiToivio/$repo.git" "$target"
done

echo "Module repositories are available beside $ROOT_DIR"
