#!/usr/bin/env bash
# Run one paper-reproduction benchmark with Gemini CLI (Google's coding agent) in skills-only mode:
# the same prompt, the same `.agents/skills/` as the Codex harness, one clean directory per attempt.
# It is the control for Model C — the same Gemini model inside a coding-agent harness instead of the
# python-agent (ADK) single loop.
#
# usage: scripts/bench/run_benchmark_gemini.sh <arxiv> <figure> <model> [--label L] [--codex-checkout DIR]
#                                              [--wall-limit SECONDS] [--no-wait]
#   <model>   gemini-3.1-pro-preview | gemini-3-pro-preview | gemini-2.5-pro
#   Skills come from the codex-com checkout (default ../ColliderAgent-codex); GEMINI.md and sub-agents from the
#   gemini-com checkout when present, else AGENTS.md is adapted into a skills-only GEMINI.md.
#
# Keys: ~/.config/collideragent/openlux.env (OPENLUX_API_KEY, OPENLUX_BASE_URL) — Gemini CLI reads them as
# GEMINI_API_KEY / GOOGLE_GEMINI_BASE_URL. ~/.gemini/settings.json must select "gemini-api-key" auth and
# disable folder trust (see docs/paper/results-2026-09-24/README.md).
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
BENCH_RUNS_DIR="${BENCH_RUNS_DIR:-$REPO_ROOT/bench_runs}"
PAPER_ROOT="${BENCH_PAPER_ROOT:-$REPO_ROOT/paper-reproduction}"
CODEX_CHECKOUT="${CODEX_CHECKOUT:-$REPO_ROOT/../ColliderAgent-codex}"
GEMINI_CHECKOUT="${GEMINI_CHECKOUT:-$REPO_ROOT/../ColliderAgent-gemini}"   # branch gemini-com: GEMINI.md + .gemini/agents
KEYS_DIR="${ADK_KEYS_DIR:-$HOME/.config/collideragent}"
GEMINI_BIN="${GEMINI_BIN:-$(command -v gemini || echo "$HOME/.npm-global/bin/gemini")}"
LABEL=""; NOWAIT=0; WALL_LIMIT=21600
[[ $# -ge 3 ]] || { sed -n '2,15p' "$0"; exit 2; }
ARXIV="$1"; FIGURE="$2"; MODEL="$3"; shift 3
while [[ $# -gt 0 ]]; do
  case "$1" in
    --label) LABEL="$2"; shift 2 ;;
    --codex-checkout) CODEX_CHECKOUT="$2"; shift 2 ;;
    --gemini-checkout) GEMINI_CHECKOUT="$2"; shift 2 ;;
    --no-subagents) GEMINI_CHECKOUT=""; shift ;;
    --wall-limit) WALL_LIMIT="$2"; shift 2 ;;
    --no-wait) NOWAIT=1; shift ;;
    *) echo "unknown option $1" >&2; exit 2 ;;
  esac
done
PROMPT_FILE="$PAPER_ROOT/$ARXIV/prompt_figure_$FIGURE.md"
[[ -f "$PROMPT_FILE" ]] || { echo "no prompt: $PROMPT_FILE" >&2; exit 2; }
[[ -f "$CODEX_CHECKOUT/AGENTS.md" && -d "$CODEX_CHECKOUT/.agents/skills" ]] || { echo "codex checkout lacks AGENTS.md/.agents/skills: $CODEX_CHECKOUT" >&2; exit 2; }
[[ -x "$GEMINI_BIN" ]] || { echo "gemini CLI not found (set GEMINI_BIN)" >&2; exit 2; }
[[ -f "$KEYS_DIR/openlux.env" ]] || { echo "missing key file $KEYS_DIR/openlux.env" >&2; exit 2; }
magnus config 2>&1 | grep -E "Current:[[:space:]]+zhustation" > /dev/null || echo "warning: magnus current site is not zhustation" >&2

TS="$(date -u +%Y%m%dT%H%M%SZ)"
[[ -n "$LABEL" ]] || LABEL="${TS}_${ARXIV}_fig${FIGURE}_gemini-${MODEL}"
SANDBOX="$BENCH_RUNS_DIR/$LABEL"
mkdir -p "$SANDBOX"
[[ -f "$BENCH_RUNS_DIR/.gitignore" ]] || printf '*\n!.gitignore\n' > "$BENCH_RUNS_DIR/.gitignore"
cp "$PROMPT_FILE" "$SANDBOX/prompt.md"
cat "$REPO_ROOT/scripts/bench/benchmark_rules.md" >> "$SANDBOX/prompt.md"
for extra in analysis hepdata; do [[ -d "$PAPER_ROOT/$ARXIV/$extra" ]] && cp -r "$PAPER_ROOT/$ARXIV/$extra" "$SANDBOX/"; done
if [[ -n "$GEMINI_CHECKOUT" && -f "$GEMINI_CHECKOUT/GEMINI.md" && -d "$GEMINI_CHECKOUT/.gemini/agents" ]]; then
  # full adapter (branch gemini-com): GEMINI.md and the four local sub-agents
  cp "$GEMINI_CHECKOUT/GEMINI.md" "$SANDBOX/GEMINI.md"
  mkdir -p "$SANDBOX/.gemini"
  cp -r "$GEMINI_CHECKOUT/.gemini/agents" "$SANDBOX/.gemini/agents"
  # workspace settings (experimental.enableAgents=true: custom sub-agents are not loaded without it)
  [[ -f "$GEMINI_CHECKOUT/.gemini/settings.json" ]] && cp "$GEMINI_CHECKOUT/.gemini/settings.json" "$SANDBOX/.gemini/settings.json"
  # Project-level agents carry a content hash and are only registered after an interactive acknowledgement
  # (no dialog in headless mode -> "Subagent 'x' not found"); user-level agents register directly, so the
  # four definitions are also installed into ~/.gemini/agents/ (same files, overwritten on every launch).
  mkdir -p "$HOME/.gemini/agents" && cp "$GEMINI_CHECKOUT"/.gemini/agents/*.md "$HOME/.gemini/agents/"
  ADAPTER="gemini-com ($(git -C "$GEMINI_CHECKOUT" rev-parse --short HEAD 2>/dev/null || echo unknown))"
else
  # skills-only fallback: the Codex AGENTS.md adapted, no custom sub-agents (the 2026-09-26 control runs)
  ADAPTER="skills-only (AGENTS.md of $CODEX_CHECKOUT)"
{
  sed 's/^# ColliderAgent Codex adapter/# ColliderAgent Gemini CLI adapter/' "$CODEX_CHECKOUT/AGENTS.md"
  cat <<'NOTE'

## Gemini CLI notes

This harness has no custom sub-agents and no `.codex/` directory: perform the pipeline stages yourself,
in order (model → events → analysis → post-processing), activating the matching skill before each stage,
and keep writing the `progress/<run>/stepN_<stage>.md` and `.json` sidecars the skills describe. Use
`run_shell_command` for the `magnus` CLI and for Python post-processing. Do not stop to wait for a cloud
job: poll it with `magnus job status <id>` (sleep between polls) until it finishes, then continue.
NOTE
} > "$SANDBOX/GEMINI.md"
fi
mkdir -p "$SANDBOX/.agents/skills"
for s in "$CODEX_CHECKOUT"/.agents/skills/*; do
  [[ -f "$s/SKILL.md" ]] || continue
  cp -rL "$s" "$SANDBOX/.agents/skills/$(basename "$s")"
done
GIT_COMMIT="$(git -C "$CODEX_CHECKOUT" rev-parse HEAD 2>/dev/null || echo unknown)"
cat > "$SANDBOX/run.env" <<ENV
HARNESS=gemini
MODEL=$MODEL
EFFORT=
MEMORY=cold
ARXIV=$ARXIV
FIGURE=$FIGURE
LABEL=$LABEL
GIT_COMMIT=$GIT_COMMIT
CODEX_CHECKOUT=$CODEX_CHECKOUT
GEMINI_BIN=$GEMINI_BIN
GEMINI_VERSION=$("$GEMINI_BIN" --version 2>/dev/null | head -1)
ADAPTER=$ADAPTER
KEYS_DIR=$KEYS_DIR
WALL_LIMIT=$WALL_LIMIT
START_UTC=$TS
ENV
cat > "$SANDBOX/run.sh" <<'RUN'
set -u
cd "$(dirname "$0")"
val() { grep "^$1=" run.env | cut -d= -f2-; }
MODEL=$(val MODEL); GEMINI_BIN=$(val GEMINI_BIN); KEYS_DIR=$(val KEYS_DIR); WALL_LIMIT=$(val WALL_LIMIT)
set -a; . "$KEYS_DIR/openlux.env"; set +a
export GEMINI_API_KEY="$OPENLUX_API_KEY" GOOGLE_GEMINI_BASE_URL="${OPENLUX_BASE_URL%/}"
PROMPT="$(cat prompt.md)"
date +%s > start.ts
timeout "$WALL_LIMIT" "$GEMINI_BIN" -m "$MODEL" --yolo --output-format stream-json -p "$PROMPT" < /dev/null > events.jsonl 2> stderr.log
RC=$?
date +%s > end.ts
python3 - "$RC" <<'PY'
import json,sys
s=int(open("start.ts").read()); e=int(open("end.ts").read())
json.dump({"start_ts":s,"end_ts":e,"exit_code":int(sys.argv[1]),"wall_clock_s":e-s}, open("status.json","w"), indent=1)
PY
python3 "$COLLECT" "$PWD" > collect.log 2>&1 || true
RUN
sed -i "s#python3 \"\$COLLECT\"#python3 '$REPO_ROOT/scripts/bench/collect_metrics_gemini.py'#" "$SANDBOX/run.sh"
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
