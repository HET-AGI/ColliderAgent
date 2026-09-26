#!/usr/bin/env bash
# Run one paper-reproduction prompt with the Codex CLI (skills-only / Codex-agents mode) in a clean sandbox.
#
#   scripts/bench/run_benchmark_codex.sh <arxiv-id> <figure> <model> [--effort low|medium|high|xhigh]
#                                        [--label L] [--codex-checkout DIR] [--no-wait]
#
# The sandbox bench_runs/<label>/ gets prompt.md (+ data files), and the Codex adapter of the codex-com
# branch: AGENTS.md, .codex/ (project config + agents) and .agents/skills/ with the symlinks materialised,
# taken from --codex-checkout (default: ../ColliderAgent-codex, a worktree of branch codex-com).
# Then, from inside the sandbox:
#   codex exec -m <model> -C <sandbox> --skip-git-repo-check --dangerously-bypass-approvals-and-sandbox \
#              --json -o last_message.txt [-c model_reasoning_effort=E] "<prompt>"  < /dev/null
# Produces events.jsonl, last_message.txt, stderr.log, start.ts/end.ts, status.json, run.env, then calls
# collect_metrics_codex.py. --no-wait detaches and returns the sandbox path and PID.
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
BENCH_RUNS_DIR="${BENCH_RUNS_DIR:-$REPO_ROOT/bench_runs}"
PAPER_ROOT="${BENCH_PAPER_ROOT:-$REPO_ROOT/paper-reproduction}"
CODEX_CHECKOUT="${CODEX_CHECKOUT:-$REPO_ROOT/../ColliderAgent-codex}"
EFFORT=""; LABEL=""; NOWAIT=0
[[ $# -ge 3 ]] || { sed -n '2,15p' "$0"; exit 2; }
ARXIV="$1"; FIGURE="$2"; MODEL="$3"; shift 3
while [[ $# -gt 0 ]]; do
  case "$1" in
    --effort) EFFORT="$2"; shift 2 ;;
    --label) LABEL="$2"; shift 2 ;;
    --codex-checkout) CODEX_CHECKOUT="$2"; shift 2 ;;
    --no-wait) NOWAIT=1; shift ;;
    *) echo "unknown option $1" >&2; exit 2 ;;
  esac
done
PROMPT_FILE="$PAPER_ROOT/$ARXIV/prompt_figure_$FIGURE.md"
[[ -f "$PROMPT_FILE" ]] || { echo "no prompt: $PROMPT_FILE" >&2; exit 2; }
for f in AGENTS.md .codex/config.toml; do [[ -f "$CODEX_CHECKOUT/$f" ]] || { echo "codex checkout lacks $f: $CODEX_CHECKOUT" >&2; exit 2; }; done
command -v codex >/dev/null || { echo "codex CLI not on PATH" >&2; exit 2; }

TS="$(date -u +%Y%m%dT%H%M%SZ)"
[[ -n "$LABEL" ]] || LABEL="${TS}_${ARXIV}_fig${FIGURE}_codex-${MODEL}"
SANDBOX="$BENCH_RUNS_DIR/$LABEL"
mkdir -p "$SANDBOX"
[[ -f "$BENCH_RUNS_DIR/.gitignore" ]] || printf '*\n!.gitignore\n' > "$BENCH_RUNS_DIR/.gitignore"
cp "$PROMPT_FILE" "$SANDBOX/prompt.md"
cat "$REPO_ROOT/scripts/bench/benchmark_rules.md" >> "$SANDBOX/prompt.md"
for extra in analysis hepdata; do [[ -d "$PAPER_ROOT/$ARXIV/$extra" ]] && cp -r "$PAPER_ROOT/$ARXIV/$extra" "$SANDBOX/"; done
# Codex adapter: AGENTS.md, .codex/, materialised skills (symlinks -> real directories)
cp "$CODEX_CHECKOUT/AGENTS.md" "$SANDBOX/AGENTS.md"
cp -r "$CODEX_CHECKOUT/.codex" "$SANDBOX/.codex"
mkdir -p "$SANDBOX/.agents/skills"
for s in "$CODEX_CHECKOUT"/.agents/skills/*; do
  [[ -f "$s/SKILL.md" ]] || continue
  cp -rL "$s" "$SANDBOX/.agents/skills/$(basename "$s")"
done
GIT_COMMIT="$(git -C "$CODEX_CHECKOUT" rev-parse HEAD 2>/dev/null || echo unknown)"
cat > "$SANDBOX/run.env" <<ENV
HARNESS=codex
MODEL=$MODEL
EFFORT=$EFFORT
MEMORY=cold
ARXIV=$ARXIV
FIGURE=$FIGURE
LABEL=$LABEL
GIT_COMMIT=$GIT_COMMIT
CODEX_CHECKOUT=$CODEX_CHECKOUT
CODEX_VERSION=$(codex --version 2>/dev/null | head -1)
ENV
cat > "$SANDBOX/run.sh" <<'RUN'
#!/usr/bin/env bash
set -u
cd "$(dirname "$0")"
MODEL=$(grep '^MODEL=' run.env | cut -d= -f2-); EFFORT=$(grep '^EFFORT=' run.env | cut -d= -f2-)
PROMPT="$(cat prompt.md)"
ARGS=(exec -m "$MODEL" -C "$PWD" --skip-git-repo-check --dangerously-bypass-approvals-and-sandbox --json -o last_message.txt)
[[ -n "$EFFORT" ]] && ARGS+=(-c "model_reasoning_effort=\"$EFFORT\"")
date +%s > start.ts
codex "${ARGS[@]}" "$PROMPT" < /dev/null > events.jsonl 2> stderr.log
RC=$?
date +%s > end.ts
python3 - "$RC" <<'PY'
import json,sys
s=int(open("start.ts").read()); e=int(open("end.ts").read())
json.dump({"start_ts":s,"end_ts":e,"exit_code":int(sys.argv[1]),"wall_clock_s":e-s}, open("status.json","w"), indent=1)
PY
python3 "$COLLECT" "$PWD" > collect.log 2>&1 || true
RUN
sed -i "s#python3 \"\$COLLECT\"#python3 '$REPO_ROOT/scripts/bench/collect_metrics_codex.py'#" "$SANDBOX/run.sh"
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
