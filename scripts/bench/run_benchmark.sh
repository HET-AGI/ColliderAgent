#!/usr/bin/env bash
# Run one paper-reproduction prompt in a clean sandbox with a chosen model, record timing,
# and collect metrics (design spec 2026-09-16-skill-evolution-design.md, section 4).
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: scripts/bench/run_benchmark.sh <arxiv-id> <figure> <model> [options]

Creates bench_runs/<label>/ containing prompt.md (from paper-reproduction/<arxiv>/
prompt_figure_<figure>.md, plus analysis/, hepdata/ and *.yaml inputs when present) and a
private CLAUDE_CONFIG_DIR (.claude-config/) with this checkout's skills and agents, your
credentials and settings, and an agent-memory that is empty (cold) or a copy of the central
store (warm). Then runs, detached from the caller:

  CLAUDE_CONFIG_DIR=<sandbox>/.claude-config claude -p "<prompt>" --model <model>
      [--effort E] --output-format json --dangerously-skip-permissions [extra]

writing result.json, stderr.log, start.ts/end.ts, status.json, and finally metrics.json via
collect_metrics.py. Import the harvested memory afterwards with
  scripts/memory/distill.py import --from <sandbox>/.claude-config/agent-memory

Options:
  --effort <E>          pass --effort E to claude (low|medium|high|max)
  --memory cold|warm    cold (default): empty agent-memory; warm: copy of the central store
  --label <L>           sandbox name (default: <UTC-ts>_<arxiv>_fig<figure>_<model>)
  --extra-args "..."    extra claude flags, split on whitespace (repeatable)
  --no-wait             launch in the background, print the sandbox path and PID, return
  -h, --help            show this help

Environment: BENCH_RUNS_DIR (default <repo>/bench_runs), BENCH_PAPER_ROOT (default
<repo>/paper-reproduction), BENCH_POLL_S (wait poll interval, default 10), CLAUDE_CONFIG_DIR
(where credentials, settings and the central agent-memory are read from).
USAGE
}

if [[ $# -ge 1 ]]; then
  case "$1" in -h|--help) usage; exit 0 ;; esac
fi
[[ $# -ge 3 ]] || { usage >&2; exit 2; }
ARXIV="$1"; FIGURE="$2"; MODEL="$3"; shift 3
EFFORT=""; MEMORY="cold"; LABEL=""; NOWAIT=0
EXTRA=()

need_value() { [[ $# -ge 2 ]] || { echo "run_benchmark.sh: $1 needs a value" >&2; exit 2; }; }
while [[ $# -gt 0 ]]; do
  case "$1" in
    --effort) need_value "$@"; EFFORT="$2"; shift 2 ;;
    --memory) need_value "$@"; MEMORY="$2"; shift 2 ;;
    --label) need_value "$@"; LABEL="$2"; shift 2 ;;
    --extra-args)
      need_value "$@"
      if [[ -n "$2" ]]; then
        read -r -a words <<< "$2"
        EXTRA+=("${words[@]}")
      fi
      shift 2 ;;
    --no-wait) NOWAIT=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "run_benchmark.sh: unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done
case "$MEMORY" in cold|warm) ;; *) echo "run_benchmark.sh: --memory must be cold or warm" >&2; exit 2 ;; esac

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PAPER_DIR="${BENCH_PAPER_ROOT:-$REPO_ROOT/paper-reproduction}/$ARXIV"
PROMPT_SRC="$PAPER_DIR/prompt_figure_$FIGURE.md"
[[ -f "$PROMPT_SRC" ]] || { echo "run_benchmark.sh: prompt not found: $PROMPT_SRC" >&2; exit 2; }
command -v claude >/dev/null 2>&1 || { echo "run_benchmark.sh: claude CLI not found in PATH" >&2; exit 2; }

SRC_CFG="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
TS="$(date -u +%Y%m%dT%H%M%SZ)"
MODEL_SLUG="$(printf '%s' "$MODEL" | tr -c 'A-Za-z0-9._-' '-')"
[[ -n "$LABEL" ]] || LABEL="${TS}_${ARXIV}_fig${FIGURE}_${MODEL_SLUG}"
RUNS_DIR="${BENCH_RUNS_DIR:-$REPO_ROOT/bench_runs}"
SANDBOX="$RUNS_DIR/$LABEL"
[[ ! -e "$SANDBOX" ]] || { echo "run_benchmark.sh: sandbox already exists: $SANDBOX (choose another --label)" >&2; exit 2; }

# --- sandbox contents -------------------------------------------------------------------
mkdir -p "$RUNS_DIR"
# Sandboxes hold copied credentials and large outputs: never let git see them.
[[ -f "$RUNS_DIR/.gitignore" ]] || printf '*\n!.gitignore\n' > "$RUNS_DIR/.gitignore"
mkdir -p "$SANDBOX"
cp "$PROMPT_SRC" "$SANDBOX/prompt.md"
cat "$REPO_ROOT/scripts/bench/benchmark_rules.md" >> "$SANDBOX/prompt.md"
for d in analysis hepdata; do
  if [[ -d "$PAPER_DIR/$d" ]]; then cp -R "$PAPER_DIR/$d" "$SANDBOX/$d"; fi
done
while IFS= read -r -d '' f; do
  rel="${f#"$PAPER_DIR"/}"
  mkdir -p "$SANDBOX/$(dirname "$rel")"
  cp "$f" "$SANDBOX/$rel"
done < <(find "$PAPER_DIR" -type f \( -name '*.yaml' -o -name '*.yml' \) -print0)

# --- private CLAUDE_CONFIG_DIR ---------------------------------------------------------
CFG="$SANDBOX/.claude-config"
mkdir -p "$CFG"
# settings are copied; credentials are SHARED by symlink so that every sandbox session sees the token the
# main ~/.claude keeps refreshing (a copied token stops working as soon as any other session refreshes:
# "OAuth session expired and could not be refreshed", observed 2026-09-17 and 2026-09-24).
[[ -f "$SRC_CFG/settings.json" ]] && cp "$SRC_CFG/settings.json" "$CFG/settings.json"
[[ -f "$SRC_CFG/.credentials.json" ]] && ln -sfn "$SRC_CFG/.credentials.json" "$CFG/.credentials.json"
python3 "$REPO_ROOT/scripts/check_env.py" --quiet || echo "run_benchmark.sh: warning: environment incomplete (python3 scripts/check_env.py)" >&2
"$REPO_ROOT/scripts/install.sh" --target "$CFG" >/dev/null
if [[ "$MEMORY" == "warm" ]]; then
  if [[ -d "$SRC_CFG/agent-memory" ]]; then
    cp -R "$SRC_CFG/agent-memory" "$CFG/agent-memory"
  else
    echo "run_benchmark.sh: note: no central agent-memory at $SRC_CFG/agent-memory; warm run starts empty" >&2
    mkdir -p "$CFG/agent-memory"
  fi
else
  mkdir -p "$CFG/agent-memory"
fi

# --- run.env -----------------------------------------------------------------------------
GIT_COMMIT="$(git -C "$REPO_ROOT" rev-parse HEAD 2>/dev/null || echo unknown)"
GIT_BRANCH="$(git -C "$REPO_ROOT" rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"
CLAUDE_VERSION="$(claude --version 2>/dev/null | head -n 1 || echo unknown)"
{
  echo "LABEL=$LABEL"
  echo "ARXIV=$ARXIV"
  echo "FIGURE=$FIGURE"
  echo "MODEL=$MODEL"
  echo "EFFORT=$EFFORT"
  echo "MEMORY=$MEMORY"
  echo "GIT_COMMIT=$GIT_COMMIT"
  echo "GIT_BRANCH=$GIT_BRANCH"
  echo "START_UTC=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "CLAUDE_VERSION=$CLAUDE_VERSION"
  echo "CONFIG_DIR=$CFG"
  echo "SANDBOX=$SANDBOX"
  echo "EXTRA_ARGS=${EXTRA[*]:-}"
} > "$SANDBOX/run.env"

# --- generated runner (the prompt is read into a variable at run time; never eval'd) -----
CLAUDE_REST=(--model "$MODEL" --output-format json --dangerously-skip-permissions)
[[ -n "$EFFORT" ]] && CLAUDE_REST+=(--effort "$EFFORT")
if [[ ${#EXTRA[@]} -gt 0 ]]; then CLAUDE_REST+=("${EXTRA[@]}"); fi
{
  printf '#!/usr/bin/env bash\n# generated by run_benchmark.sh; runs the benchmark inside the sandbox\nset -uo pipefail\n'
  printf 'SANDBOX=%q\nCOLLECT=%q\n' "$SANDBOX" "$REPO_ROOT/scripts/bench/collect_metrics.py"
  printf 'CLAUDE_ARGS=('
  for a in "${CLAUDE_REST[@]}"; do printf ' %q' "$a"; done
  printf ' )\n'
  cat <<'BODY'
cd "$SANDBOX"
export CLAUDE_CONFIG_DIR="$SANDBOX/.claude-config"
# Headless claude -p exits ~600 s after the main agent ends a turn while background subagents
# (the pipeline stages) are still running; 0 = wait for them indefinitely.
export CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS="${CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS:-0}"
PROMPT="$(cat prompt.md)"
START=$(date +%s)
echo "$START" > start.ts
claude -p "$PROMPT" "${CLAUDE_ARGS[@]}" > result.json 2> stderr.log
RC=$?
END=$(date +%s)
echo "$END" > end.ts
printf '{"start_ts": %s, "end_ts": %s, "exit_code": %s, "wall_clock_s": %s}\n' \
  "$START" "$END" "$RC" "$((END - START))" > status.json
python3 "$COLLECT" "$SANDBOX" > collect.log 2>&1 || true
exit "$RC"
BODY
} > "$SANDBOX/run.sh"
chmod +x "$SANDBOX/run.sh"

# --- launch, detached from this shell ----------------------------------------------------
cd "$SANDBOX"
if command -v setsid >/dev/null 2>&1; then
  setsid nohup bash "$SANDBOX/run.sh" > "$SANDBOX/run.log" 2>&1 < /dev/null &
else
  nohup bash "$SANDBOX/run.sh" > "$SANDBOX/run.log" 2>&1 < /dev/null &
fi
PID=$!
echo "$PID" > "$SANDBOX/pid"
echo "sandbox: $SANDBOX"
echo "pid: $PID"
if [[ $NOWAIT -eq 1 ]]; then
  echo "running in the background; status.json and metrics.json appear when it finishes"
  exit 0
fi
while kill -0 "$PID" 2>/dev/null; do sleep "${BENCH_POLL_S:-10}"; done

RC=1
if [[ -f "$SANDBOX/status.json" ]]; then
  cat "$SANDBOX/status.json"
  RC="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("exit_code", 1))' "$SANDBOX/status.json")"
else
  echo "run_benchmark.sh: status.json missing; see $SANDBOX/run.log" >&2
fi
if [[ -f "$SANDBOX/metrics.json" ]]; then
  python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["table_s3_row"])' "$SANDBOX/metrics.json"
else
  echo "run_benchmark.sh: metrics.json missing; see $SANDBOX/collect.log" >&2
fi
exit "$RC"
