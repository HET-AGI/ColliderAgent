#!/usr/bin/env bash
# Run one paper-reproduction benchmark with the python-agent (Google ADK + LiteLLM) harness —
# the "traditional" single-agent, flat-tool baseline (Model C in the paper's Table S4).
#
# usage: scripts/bench/run_benchmark_adk.sh <arxiv> <figure> <model> [--max-turns N] [--label L]
#                                           [--provider openlux|openai] [--wall-limit SECONDS] [--no-wait]
#   <model>      gemini-3.1-pro-preview | gemini-3-pro-preview | gemini-2.5-pro | gpt-5.5 | ... (LiteLLM openai/<model>)
#   --provider   which key/base URL to use; default: openlux for gemini-* (relay), openai for gpt-*
#   --max-turns  ADK max_llm_calls (default 150; the stock agent default is 20)
#   --wall-limit kill the run after this many seconds (default 21600 = 6 h)
#
# Keys are read from ~/.config/collideragent/openlux.env (OPENLUX_API_KEY, OPENLUX_BASE_URL) and
# ~/.config/collideragent/openai.env (OPENAI_API_KEY_REAL); override the directory with ADK_KEYS_DIR.
# Magnus is taken from ~/.magnus/config.json (current site) exactly as the magnus CLI does.
#
# The sandbox (BENCH_RUNS_DIR/<label>/) gets prompt.md, task.md (prompt + working-directory note),
# run.env, run.sh, events.jsonl (one record per ADK event), agent_stdout.log, status.json and, after
# collect_metrics_adk.py, metrics.json — the same files aggregate.py / judge_all.sh expect.
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
BENCH_RUNS_DIR="${BENCH_RUNS_DIR:-$REPO_ROOT/bench_runs}"
PAPER_ROOT="${BENCH_PAPER_ROOT:-$REPO_ROOT/paper-reproduction}"
AGENT_DIR="${ADK_AGENT_DIR:-$REPO_ROOT/python-agent}"
KEYS_DIR="${ADK_KEYS_DIR:-$HOME/.config/collideragent}"
MAX_TURNS=150; LABEL=""; NOWAIT=0; PROVIDER=""; WALL_LIMIT=21600
[[ $# -ge 3 ]] || { sed -n '2,16p' "$0"; exit 2; }
ARXIV="$1"; FIGURE="$2"; MODEL="$3"; shift 3
while [[ $# -gt 0 ]]; do
  case "$1" in
    --max-turns) MAX_TURNS="$2"; shift 2 ;;
    --label) LABEL="$2"; shift 2 ;;
    --provider) PROVIDER="$2"; shift 2 ;;
    --wall-limit) WALL_LIMIT="$2"; shift 2 ;;
    --no-wait) NOWAIT=1; shift ;;
    *) echo "unknown option $1" >&2; exit 2 ;;
  esac
done
if [[ -z "$PROVIDER" ]]; then
  case "$MODEL" in gemini*) PROVIDER=openlux ;; *) PROVIDER=openai ;; esac
fi
PROMPT_FILE="$PAPER_ROOT/$ARXIV/prompt_figure_$FIGURE.md"
[[ -f "$PROMPT_FILE" ]] || { echo "no prompt: $PROMPT_FILE" >&2; exit 2; }
PY="$AGENT_DIR/.venv/bin/python"
[[ -x "$PY" ]] || { echo "python-agent venv missing: run 'uv sync --extra analysis' in $AGENT_DIR" >&2; exit 2; }
[[ -f "$KEYS_DIR/$PROVIDER.env" ]] || { echo "missing key file $KEYS_DIR/$PROVIDER.env" >&2; exit 2; }
"$PY" -c "import google.adk, litellm, magnus" || { echo "python-agent venv lacks google-adk/litellm/magnus" >&2; exit 2; }
magnus config 2>&1 | grep -qE "Current:[[:space:]]+zhustation" || echo "warning: magnus current site is not zhustation" >&2

TS="$(date -u +%Y%m%dT%H%M%SZ)"
[[ -n "$LABEL" ]] || LABEL="${TS}_${ARXIV}_fig${FIGURE}_adk-${MODEL}"
SANDBOX="$BENCH_RUNS_DIR/$LABEL"
mkdir -p "$SANDBOX"
[[ -f "$BENCH_RUNS_DIR/.gitignore" ]] || printf '*\n!.gitignore\n' > "$BENCH_RUNS_DIR/.gitignore"
cp "$PROMPT_FILE" "$SANDBOX/prompt.md"
for extra in analysis hepdata; do [[ -d "$PAPER_ROOT/$ARXIV/$extra" ]] && cp -r "$PAPER_ROOT/$ARXIV/$extra" "$SANDBOX/"; done
{
  cat "$PROMPT_FILE"
  cat <<NOTE

## Execution environment
- Working directory: $SANDBOX (absolute). Create every file under this directory and pass absolute paths to the tools.
- The Magnus cloud (FeynRules, MadGraph5, MadAnalysis5) is configured; the tools upload your inputs and download results into the paths you give.
- Use run_python / run_shell for post-processing, statistics and plotting; save the final figure as a PNG under $SANDBOX/output/figures/ and state its absolute path in your final answer.
NOTE
} > "$SANDBOX/task.md"
GIT_COMMIT="$(git -C "$REPO_ROOT" rev-parse HEAD 2>/dev/null || echo unknown)"
ADK_VERSION="$("$PY" -c 'import google.adk, litellm; print(google.adk.__version__, "litellm", getattr(litellm, "__version__", "?"))' 2>/dev/null || echo unknown)"
cat > "$SANDBOX/run.env" <<ENV
HARNESS=adk
MODEL=$MODEL
EFFORT=
MEMORY=cold
ARXIV=$ARXIV
FIGURE=$FIGURE
LABEL=$LABEL
GIT_COMMIT=$GIT_COMMIT
PROVIDER=$PROVIDER
MAX_TURNS=$MAX_TURNS
WALL_LIMIT=$WALL_LIMIT
ADK_VERSION=$ADK_VERSION
AGENT_DIR=$AGENT_DIR
KEYS_DIR=$KEYS_DIR
START_UTC=$TS
ENV
cat > "$SANDBOX/run.sh" <<'RUN'
set -u
cd "$(dirname "$0")"
val() { grep "^$1=" run.env | cut -d= -f2-; }
MODEL=$(val MODEL); PROVIDER=$(val PROVIDER); MAX_TURNS=$(val MAX_TURNS); WALL_LIMIT=$(val WALL_LIMIT)
AGENT_DIR=$(val AGENT_DIR); KEYS_DIR=$(val KEYS_DIR)
set -a; . "$KEYS_DIR/$PROVIDER.env"; set +a
if [[ "$PROVIDER" == "openlux" ]]; then
  export OPENAI_API_KEY="$OPENLUX_API_KEY" OPENAI_BASE_URL="${OPENLUX_BASE_URL%/}/v1"
else
  export OPENAI_API_KEY="$OPENAI_API_KEY_REAL"; unset OPENAI_BASE_URL
fi
export COLLIDER_AGENT_MODEL="openai/$MODEL" COLLIDER_AGENT_EVENTS="$PWD/events.jsonl" COLLIDER_AGENT_MAX_TURNS="$MAX_TURNS"
export MPLBACKEND=Agg
date +%s > start.ts
timeout "$WALL_LIMIT" "$AGENT_DIR/.venv/bin/python" "$AGENT_DIR/agent.py" task.md --max-turns "$MAX_TURNS" --save-session --output-dir outputs > agent_stdout.log 2> agent_stderr.log
RC=$?
date +%s > end.ts
python3 - "$RC" <<'PY'
import json,sys
s=int(open("start.ts").read()); e=int(open("end.ts").read())
json.dump({"start_ts":s,"end_ts":e,"exit_code":int(sys.argv[1]),"wall_clock_s":e-s}, open("status.json","w"), indent=1)
PY
python3 "$COLLECT" "$PWD" > collect.log 2>&1 || true
RUN
sed -i "s#python3 \"\$COLLECT\"#python3 '$REPO_ROOT/scripts/bench/collect_metrics_adk.py'#" "$SANDBOX/run.sh"
chmod +x "$SANDBOX/run.sh"
if [[ $NOWAIT -eq 1 ]]; then
  if command -v setsid >/dev/null 2>&1; then
    setsid nohup bash "$SANDBOX/run.sh" > "$SANDBOX/run.log" 2>&1 < /dev/null &
  else
    nohup bash "$SANDBOX/run.sh" > "$SANDBOX/run.log" 2>&1 < /dev/null &
  fi
  PID=$!
  echo "$PID" > "$SANDBOX/pid"
  echo "sandbox: $SANDBOX"; echo "pid: $PID"; echo "running in the background; status.json and metrics.json appear when it finishes"
else
  bash "$SANDBOX/run.sh"
  cat "$SANDBOX/collect.log"
fi
