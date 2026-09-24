#!/usr/bin/env bash
# Five-blueprint smoke run against Magnus (zhustation) with the inputs used on 2026-09-16:
# config check, madgraph-compile, madgraph-launch, madanalysis-process, validate-feynrules.
# Exit non-zero on any step that does not report "success": true.
set -uo pipefail

usage() {
  cat <<'USAGE'
Usage: scripts/bench/smoke.sh [--quick] [--dry-run]

Steps (each log goes to $SMOKE_DIR/<step>.log; a step passes iff the log contains
"success": true):
  config     magnus config must show `Current:  zhustation` (exit 1 otherwise)
  compile    magnus run madgraph-compile   (p p > e+ e-)
  launch     magnus run madgraph-launch    (500 events, 7+7 TeV, no systematics)
  ma5        magnus run madanalysis-process (parton level, M(e+ e-) histogram)
  validate   magnus run validate-feynrules (python-agent/tests/assets/minimal_Zp.fr)

  --quick     run only config, compile and validate
  --dry-run   print the commands without calling magnus
  -h, --help  show this help

Environment: SMOKE_DIR (default /tmp/collider-smoke-<pid>), SMOKE_TIMEOUT seconds per
job (default 1800). The magnus token is never printed.
USAGE
}

QUICK=0; DRY=0
for arg in "$@"; do
  case "$arg" in
    --quick) QUICK=1 ;;
    --dry-run) DRY=1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "smoke.sh: unknown argument: $arg" >&2; usage >&2; exit 2 ;;
  esac
done

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SMOKE_DIR="${SMOKE_DIR:-/tmp/collider-smoke-$$}"
TIMEOUT="${SMOKE_TIMEOUT:-1800}"
# `magnus run` takes no leading options before the blueprint id (a leading --timeout is parsed as the id),
# so bound each step with coreutils timeout instead.
if command -v timeout >/dev/null 2>&1; then TIMEOUT_CMD=(timeout "$TIMEOUT"); else TIMEOUT_CMD=(); fi

FR="$REPO_ROOT/python-agent/tests/assets/minimal_Zp.fr"
[[ -f "$FR" ]] || { echo "smoke.sh: model file not found: $FR" >&2; exit 2; }
# Prefer the total Lagrangian: the L* symbol whose definition sums the most other L* symbols
# (LmZp := LGauge + LHiggs + LFermions + LYukawa + LGhost in minimal_Zp.fr); fall back to the first L* assignment.
SYMBOL="${SMOKE_LAGRANGIAN:-}"
if [[ -z "$SYMBOL" ]]; then
  SYMBOL="$(awk '/^L[A-Za-z0-9]+[[:space:]]*:?=/ { sym=$1; sub(/:?=.*/, "", sym); n=gsub(/\+[[:space:]]*L[A-Za-z0-9]+/, "&"); if (n>best) {best=n; bestsym=sym} } END { if (best>0) print bestsym }' "$FR" || true)"
fi
[[ -z "$SYMBOL" ]] && SYMBOL="$(grep -m1 -oE '^L[A-Za-z0-9]+' "$FR" || true)"
[[ -n "$SYMBOL" ]] || { echo "smoke.sh: no Lagrangian symbol (^L[A-Za-z0-9]+) found in $FR" >&2; exit 2; }
mkdir -p "$SMOKE_DIR"

# Exactly two `done` lines: the first accepts the default run mode, the second confirms the cards.
LAUNCH_CMDS=$'done\nset nevents 500\nset ebeam1 7000\nset ebeam2 7000\nset use_syst False\ndone'
MA5_SCRIPT=$'import {EVENTS_DIR}/Events/run_01/unweighted_events.lhe.gz as sample\nset sample.type = signal\nplot M(e+ e-) 50 0 500\nselect N(e+) >= 1'

redact() { sed 's/sk-[A-Za-z0-9_-]*/sk-***/g'; }

NAMES=(); RESULTS=()
record() { NAMES+=("$1"); RESULTS+=("$2"); }

print_table() {
  echo
  echo "| step | result | log |"
  echo "|---|---|---|"
  local i
  for i in "${!NAMES[@]}"; do
    echo "| ${NAMES[$i]} | ${RESULTS[$i]} | $SMOKE_DIR/${NAMES[$i]}.log |"
  done
}

run_step() {  # <name> <command...>
  local name="$1"; shift
  local log="$SMOKE_DIR/$name.log"
  printf '== %s:' "$name"; printf ' %q' "$@" | redact; echo
  if [[ $DRY -eq 1 ]]; then record "$name" DRY; return 0; fi
  "$@" 2>&1 | redact > "$log"
  if grep -q '"success": true' "$log"; then
    record "$name" PASS; return 0
  fi
  record "$name" FAIL
  echo "smoke.sh: $name failed; tail of $log:" >&2
  tail -n 20 "$log" >&2
  return 1
}

echo "smoke dir: $SMOKE_DIR   (lagrangian symbol: $SYMBOL)"

# 1. config
echo "== config: magnus config"
if [[ $DRY -eq 1 ]]; then
  record config DRY
else
  magnus config 2>&1 | redact > "$SMOKE_DIR/config.log"
  if grep -qE '^[[:space:]]*Current:[[:space:]]+zhustation[[:space:]]*$' "$SMOKE_DIR/config.log"; then
    record config PASS
  else
    record config FAIL
    cat "$SMOKE_DIR/config.log"
    echo "smoke.sh: magnus current site is not zhustation; run 'magnus login zhustation' first" >&2
    print_table
    exit 1
  fi
fi

# 2. compile
COMPILE_OK=0
if run_step compile ${TIMEOUT_CMD[@]} magnus run madgraph-compile -- \
     --process "p p > e+ e-" --output "$SMOKE_DIR/pp_ee"; then COMPILE_OK=1; fi

# 3./4. launch + ma5 (skipped with --quick)
if [[ $QUICK -eq 0 ]]; then
  if [[ $COMPILE_OK -eq 1 || $DRY -eq 1 ]]; then
    LAUNCH_OK=0
    if run_step launch ${TIMEOUT_CMD[@]} magnus run madgraph-launch -- \
         --process "$SMOKE_DIR/pp_ee" --commands "$LAUNCH_CMDS" --output "$SMOKE_DIR/pp_ee"; then LAUNCH_OK=1; fi
    if [[ $LAUNCH_OK -eq 1 || $DRY -eq 1 ]]; then
      run_step ma5 ${TIMEOUT_CMD[@]} magnus run madanalysis-process -- \
        --events "$SMOKE_DIR/pp_ee" --script "$MA5_SCRIPT" --output "$SMOKE_DIR/ma5_out" --level parton || true
    else
      record ma5 "FAIL (skipped: launch failed)"
    fi
  else
    record launch "FAIL (skipped: compile failed)"
    record ma5 "FAIL (skipped: compile failed)"
  fi
fi

# 5. validate
run_step validate ${TIMEOUT_CMD[@]} magnus run validate-feynrules -- \
  --model "$FR" --lagrangian "$SYMBOL" || true

print_table
FAILED=0
for r in "${RESULTS[@]}"; do
  case "$r" in PASS|DRY) ;; *) FAILED=1 ;; esac
done
if [[ $FAILED -eq 0 ]]; then echo "smoke: all steps passed"; else echo "smoke: FAILED" >&2; fi
exit $FAILED
