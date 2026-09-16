# Benchmark harness (`scripts/bench/`)

Runs a paper-reproduction prompt in a clean sandbox with a chosen model and emits the
numbers Tables S3/S4/S5 need. Design: `docs/superpowers/specs/2026-09-16-skill-evolution-design.md`, section 4.
All scripts print `--help`; the Python ones need only the standard library.

| Script | What it does |
|---|---|
| `run_benchmark.sh <arxiv> <figure> <model> [--effort E] [--memory cold\|warm] [--label L] [--extra-args "..."] [--no-wait]` | Creates `bench_runs/<label>/` with `prompt.md` (from `paper-reproduction/<arxiv>/prompt_figure_<figure>.md`, plus `analysis/`, `hepdata/`, `*.yaml` inputs), a private `CLAUDE_CONFIG_DIR` (`.claude-config/`: this checkout's skills/agents via `scripts/install.sh`, your `.credentials.json` + `settings.json`, agent-memory empty for `cold` or a copy of the central store for `warm`), writes `run.env`, then runs `claude -p "<prompt>" --model <model> [--effort E] --output-format json --dangerously-skip-permissions` detached (`setsid nohup`) from inside the sandbox. Produces `result.json`, `stderr.log`, `start.ts`/`end.ts`, `status.json`, then calls `collect_metrics.py`. `--no-wait` returns immediately with the sandbox path and PID. |
| `collect_metrics.py <sandbox>` | Reads `result.json` (authoritative for tokens/cost/turns), `status.json`, `run.env`; copies the session transcript (`<config>/projects/<slug>/<session_id>.jsonl`, slug = sandbox path with non-alphanumerics replaced by `-`, glob fallback) to `transcript.jsonl` and its subagent transcripts to `transcript_subagents/`; counts `Agent`/`Task` tool uses (subagent calls), `Bash` commands matching `magnus (run\|launch\|blueprint run)` (Magnus jobs, counted over the main and subagent transcripts), distinct `Write`/`Edit`/`NotebookEdit` paths (files written); writes `metrics.json` with a `table_s3_row` and creates an empty `verdict.yaml` template. |
| `judge.sh <sandbox> <reference.png>` | Finds the newest `output/figures/*.png\|pdf` (PDF rasterised with `pdftoppm`), asks `claude -p` (model `JUDGE_MODEL`, default `claude-opus-5`, `--allowedTools Read`) for a strict JSON verdict and writes `verdict.yaml` (`success`, `failure_mode` in model/generation/analysis/infrastructure, `notes`, `judged_by: "... (assistive; human confirm required)"`). Unparseable output goes into `notes` with `success: null`. A human edits `verdict.yaml` to confirm. |
| `aggregate.py bench_runs/` | Reads every sandbox's `metrics.json` + `verdict.yaml` + `run.env` and prints Table S3 (mean resource usage per benchmark x model, successful runs only), S4 (successful/attempted per benchmark x model; unjudged runs shown as `?`) and S5 (successful/attempted per benchmark with failure-mode counts). Warm-memory runs appear as `<model> (warm)`. |
| `smoke.sh [--quick] [--dry-run]` | The 5-blueprint smoke gate against zhustation: `magnus config` must show `Current:  zhustation`, then `madgraph-compile` (p p > e+ e-), `madgraph-launch` (500 events, 7+7 TeV), `madanalysis-process` (parton level) and `validate-feynrules` (`python-agent/tests/assets/minimal_Zp.fr`, first `L...` symbol). Logs in `$SMOKE_DIR/<step>.log`; a step passes iff its log contains `"success": true`. Prints a PASS/FAIL table, exits non-zero on any failure. `--quick` runs config, compile and validate only. |

## Typical flow

```bash
scripts/install.sh --check                                  # installed skills match this checkout?
scripts/bench/run_benchmark.sh 1701.05379 8 claude-opus-5 --effort high --memory cold
scripts/bench/judge.sh bench_runs/<label> paper-reproduction/1701.05379/paper/fig8.png
$EDITOR bench_runs/<label>/verdict.yaml                     # confirm or fix the assistive verdict
scripts/memory/distill.py import --from bench_runs/<label>/.claude-config/agent-memory
scripts/bench/aggregate.py bench_runs/
```

## Sandbox layout

```
bench_runs/<label>/
  prompt.md  run.env  run.sh  run.log  pid  start.ts  end.ts  status.json
  result.json  stderr.log  metrics.json  verdict.yaml  transcript.jsonl  transcript_subagents/
  .claude-config/   private CLAUDE_CONFIG_DIR (skills, agents, credentials, agent-memory, projects/)
  output/           whatever the run produced (figures under output/figures/)
```

`bench_runs/.gitignore` (written on first use) keeps sandboxes, including the copied
credentials, out of git. The `warm` mode only copies memory in; harvesting is explicit via
`distill.py import`, which never lowers a central lesson's support.
