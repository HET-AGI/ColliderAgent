# Audit: filling the TBD entries of the ColliderAgent paper (sm.pdf Tables S2–S5)

Date: 2026-09-16. Sources: `/home/shiqiu/paper.pdf`, `/home/shiqiu/reply.pdf`, `/home/shiqiu/sm.pdf` (all `[AUTHORS: …]` markers and red TBDs are in the supplemental material; the main text and the reply reference the same four tables).

## Table S2 — software environment (measured today on zhustation)

| Image | Package | Version | Evidence |
|---|---|---|---|
| collider | MadGraph5_aMC@NLO | 3.7.0 | `MGMEVersion.txt` in a downloaded process dir (job 9cda4f3590e9e9cf) |
| collider | Pythia8 | 8.316 | `tag_1_pythia8.log` of job 230c4933a9ab3b75 |
| collider | HepMC | 2.06.09 | header of `tag_1_pythia8_events.hepmc.gz` |
| collider | Delphes | 3.5.x — exact patch level not printed in the run logs; read it from the container (`docker run --rm git.pku.edu.cn/het-agi/collider:latest cat <delphes>/VERSION` or `DelphesHepMC2 --version`) | `tag_1_delphes.log` prints no version |
| collider | MadAnalysis5 | 1.11.0 (2025/04/23) | `Output/HTML/MadAnalysis5job_0/index.html` of job b60762c5e7cebfe5 |
| collider | LHAPDF | 6.5.5 (already in the table) | — |
| agent runtime (local) | uproot / awkward / numpy / scipy / matplotlib / pyhf | 5.7.4 / 2.9.0 / 2.4.4 / 1.15.3 / 3.10.9 / 0.7.6 | `python3 -c "import …; print(__version__)"` on the analysis host, Python 3.13.12 |
| agent runtime | Claude Code | 2.1.273 | `claude --version` |
| agent runtime | LLM | Claude Opus 4.6 (paper's runs); `claude-opus-4-6` is still served — verified with a one-turn `claude -p --model claude-opus-4-6` call today | — |

## Tables S3 / S4 / S5 — how to produce the numbers

The harness on branch `feat/skill-evolution-v2` makes one benchmark run a single command and emits the row:

```bash
scripts/install.sh                                   # this checkout's skills into the sandbox config
scripts/bench/run_benchmark.sh 1701.05379 8 claude-opus-5     # sandbox + result.json + metrics.json
scripts/bench/judge.sh bench_runs/<label> reference_fig8.png  # assistive verdict.yaml (human confirms)
python3 scripts/bench/aggregate.py bench_runs/                # Tables S3, S4, S5 in Markdown
```

`metrics.json` carries exactly the S3 columns: wall-clock from `start.ts`/`end.ts`, sub-agent calls (`Agent` tool uses), Magnus jobs (`magnus run` Bash calls), files written (distinct Write/Edit paths), tokens in/out and cost from the CLI's `result.json` (`usage`, `total_cost_usd`). S4 needs the same benchmark × {Opus 4.6, model B, model C} × 3 attempts; S5 needs 3 attempts per benchmark on the paper's model plus the failure-mode label from `verdict.yaml`.

Benchmark ↔ prompt mapping: Scalar LQ m_ej → `2005.06475/prompt_figure_2.md`; ALP EFT E_T^miss → `1701.05379/prompt_figure_8.md`; U(1)' scan → `1605.02910/prompt_figure_1.md`; U1 LQ mono-τ → `1811.07920/prompt_figure_3.md`; Heavy N → `1308.2209/prompt_figure_3.md`; General Z' → `2103.02708/prompt_figure_4.md`; KK graviton → `9909255/prompt_figure_2.md`; U1 LQ at MuC → `2104.05720/prompt_figure_11.md`, `prompt_figure_12.md`.

Cost expectation per full run (to size the S4 matrix): the paper's Dark-SMEFT campaigns list >100 Magnus jobs and 24–36 h; the eight figure benchmarks are one to two orders smaller. Run the cheapest (ALP EFT, parton level) first with each candidate model, then decide the matrix.

## Findings from the first headless runs (2026-09-16)

- Headless `claude -p` terminates the session 600 s after the orchestrator ends a turn while a stage subagent is still running (`Background tasks still running after 600s; terminating`). Every S3–S5 run must set `CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0`; `scripts/bench/run_benchmark.sh` does. Runs made without it under-report wall-clock and fail at the first stage longer than 10 minutes.
- The quickstart integration run (Sonnet 5, v2 skills) produced 100 000 events with the requested parameters, a correct `step2_madgraph.json` sidecar, and one memory lesson in the collider-simulator store before the ceiling killed the MadAnalysis stage — evidence that the handoff and memory contracts are followed by a current model.

## First cross-model row — ALP EFT, 1701.05379 Fig. 8 (2026-09-16, v2 skills, cold memory, one attempt each)

| Model | Success | Wall-clock [h] | Sub-agent calls | Magnus jobs | Files written | Tokens in [M] | Tokens out [k] | Cost [USD] | Main-session turns |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| claude-opus-5 | yes | 0.87 | 3 | 5 | 17 | 5.72 | 37.5 | 9.06 | 15 |
| claude-opus-4-8 | yes | 1.05 | 3 | 9 | 16 | 10.96 | 43.3 | 12.55 | 7 |
| claude-sonnet-5 | yes | 1.38 | 3 | 14 | 24 | 18.19 | 34.3 | 7.54 | 15 |

Success = the produced normalized E_T^miss distribution matches the paper's c_W̃ curve (peak ≈ 0.18 per 20 GeV bin at 40–80 GeV, tail ≈ 3×10⁻⁴ at 1 TeV), confirmed by side-by-side inspection and by the assistive judge (`scripts/bench/judge.sh`, target-aware prompt). Tokens count the main session plus all stage subagents (the CLI's own `usage` field covers only the main session and would under-report by ~10×). All three runs applied the requested parameters (c_W̃ = 1, f_a = 1 TeV, m_a = 1 MeV, 500 000 events); Opus 5 and Opus 4.8 obtained identical cross sections (0.04135 pb) while Sonnet 5's 0.04909 pb reflects looser generation-level η cuts (5 instead of 2.5), which the normalization removes.

Observations for Tables S3–S5:
- One attempt is not a success rate; the harness makes the remaining two attempts per model one command each (`scripts/bench/run_benchmark.sh 1701.05379 8 <model>`), and `aggregate.py` recomputes the tables from `bench_runs/`.
- The assistive judge is not stable when the reference figure contains curves the task did not ask for; the target-aware prompt fixed one false negative today. Keep the human confirmation step.
- The experience loop produced 11 schema-valid lessons across the three runs (MG5 `cut_decays` semantics, the 10-minute shell timeout on long launches, FeynRules `FeynmanGauge = False` for UFO export, a FeynRules adjoint-index export corruption, and others); support is 1 each, so none is auto-promoted yet. One lesson (long jobs vs the shell timeout) was promoted by hand into the magnus skill.

`aggregate.py` output for the record:

Runs found: 3 (successful 3, failed 0, unjudged 0)

### Table S3: resource usage (successful runs, mean over runs)

| Benchmark | Model | Runs | Wall-clock (h) | Subagent calls | Magnus jobs | Files written | Tokens in (M) | Tokens out (k) | Cost (USD) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1701.05379 Fig. 8 | claude-opus-4-8 | 1 | 1.05 | 3.0 | 9.0 | 16.0 | 10.96 | 43.3 | 12.55 |
| 1701.05379 Fig. 8 | claude-opus-5 | 1 | 0.87 | 3.0 | 5.0 | 17.0 | 5.72 | 37.5 | 9.06 |
| 1701.05379 Fig. 8 | claude-sonnet-5 | 1 | 1.38 | 3.0 | 14.0 | 24.0 | 18.19 | 34.3 | 7.54 |

### Table S4: successful/attempted per benchmark and model (`?` = attempted, not yet judged)

| Benchmark | claude-opus-4-8 | claude-opus-5 | claude-sonnet-5 |
|---|---:|---:|---:|
| 1701.05379 Fig. 8 | 1/1 | 1/1 | 1/1 |

### Table S5: successful/attempted per benchmark with failure modes

| Benchmark | Successful/attempted | Failure modes |
|---|---:|---|
| 1701.05379 Fig. 8 | 3/3 | - |

