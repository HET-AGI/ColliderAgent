#!/usr/bin/env bash
# Judge every sandbox under bench_runs/ whose verdict.yaml is still `success: null` and that has a figure,
# using the reference image paper-reproduction/<arxiv>/reference/figure_<fig>.{png,jpeg}.
#   scripts/bench/judge_all.sh [bench_runs_dir]
set -uo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
RUNS="${1:-$REPO_ROOT/bench_runs}"
for d in "$RUNS"/*/; do
  [[ -f "$d/run.env" && -f "$d/status.json" ]] || continue
  if [[ -f "$d/verdict.yaml" ]] && ! grep -q '^success: null' "$d/verdict.yaml"; then continue; fi
  arxiv=$(grep '^ARXIV=' "$d/run.env" | cut -d= -f2); fig=$(grep '^FIGURE=' "$d/run.env" | cut -d= -f2)
  ref=$(ls "$REPO_ROOT/paper-reproduction/$arxiv/reference/figure_$fig".* 2>/dev/null | head -1)
  [[ -n "$ref" ]] || { echo "no reference for $arxiv fig $fig: $(basename "$d")"; continue; }
  echo "== $(basename "$d")"
  "$REPO_ROOT/scripts/bench/judge.sh" "$d" "$ref" 2>&1 | grep -E "^success|^failure_mode|^notes" | cut -c1-160
done
