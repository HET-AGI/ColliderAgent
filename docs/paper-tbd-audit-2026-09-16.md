# Audit: filling the TBD entries of the ColliderAgent paper (sm.pdf Tables S2–S5)

Date: 2026-09-16. Sources: `/home/shiqiu/paper.pdf`, `/home/shiqiu/reply.pdf`, `/home/shiqiu/sm.pdf` (all `[AUTHORS: …]` markers and red TBDs are in the supplemental material; the main text and the reply reference the same four tables).

## Table S2 — software environment (probed inside the images on zhustation, 2026-09-16, blueprint `collider-env-probe`)

| Image / runtime | Package | Version | Evidence |
|---|---|---|---|
| collider (`git.pku.edu.cn/het-agi/collider:latest`, Ubuntu 22.04.5) | MadGraph5_aMC@NLO | 3.7.0 | `/opt/MG5_aMC_v3_7_0` |
| collider | Pythia8 | 8.316 | `pythia8-config --version`, `PYTHIA_VERSION 8.316` |
| collider | Delphes | 3.5.1 | `/opt/MG5_aMC_v3_7_0/Delphes/README` (installer tarball Delphes-3.5.1) |
| collider | MadAnalysis5 | 1.11.0 (2025-04-23) | `/opt/madanalysis5/version.txt`, HTML report banner |
| collider | LHAPDF | 6.5.5 | `HEPTools/bin/lhapdf-config --version`; sets NNPDF23_lo_as_0130_qed, NNPDF23_nlo_as_0119_qed preinstalled |
| collider | HepMC | 2.06.09 | event-file header (job 230c4933a9ab3b75) |
| collider | ROOT | 6.28/10 | `root-config --version` |
| collider | Python | 3.10.12: numpy 1.26.4, scipy 1.15.3, awkward 2.9.0, matplotlib 3.10.8, pyhf 0.7.6; no uproot | in-image import |
| mma-het (`het-agi/mma-het:latest`, Ubuntu 22.04.3) | Wolfram Engine | 13.3.0 | `/usr/local/Wolfram/WolframEngine/13.3/.VersionID` |
| mma-het | FeynRules | 2.3.49 (paper's value; package header has no version string, see probe 4) | `/root/.WolframEngine/Applications/FeynRules` |
| micromegas (`rise-agi/micromegas:latest`) | micrOmegas / CalcHEP | 6.3.0 / 3.9.2 | `/opt/micromegas_6.3.0`, `CalcHEP_src/VERSION` |
| agent runtime (this host) | Python analysis stack | 3.13.12: uproot 5.7.4, awkward 2.9.0, numpy 2.4.4, scipy 1.15.3, matplotlib 3.10.9, pyhf 0.7.6 | installed 2026-04-19 … 2026-06-08 |
| agent runtime | Claude Code | 2.1.273 for the 2026-09-16 re-runs; original April–May runs: not recoverable here (earliest local logs are from 2026-08) | `claude --version` |
| agent runtime | LLM | Claude Opus 4.6 (`claude-opus-4-6`, still served; accepts `--effort xhigh` through the CLI) | probe calls |

Corrections to the current table: the `uproot, awkward, numpy, scipy` row belongs to the agent runtime, not the collider image; Delphes is 3.5.1.

## Wall-clock attribution (sm.pdf p.5 claim "LLM inference accounts for a minor fraction")

From transcript timestamps (gap before a model message = inference; gap before a tool result = tool execution; main session + subagents), ALP EFT Fig. 8:

| Model | Wall [s] | Model latency [s] | Tool execution [s] | Inside `magnus` calls [s] | Model share |
|---|---:|---:|---:|---:|---:|
| Opus 5 | 3147 | 1198 | 3151 | 1878 | 0.38 |
| Opus 4.8 | 3779 | 2038 | 1947 | 1684 | 0.54 |
| Sonnet 5 | 4975 | 2527 | 3989 | 2354 | 0.51 |

For this light benchmark the model share is not "a minor fraction"; the sentence should be re-stated with the Opus 4.6 numbers over all eight benchmarks (`metrics.json` carries `llm_share_of_wall`).

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

