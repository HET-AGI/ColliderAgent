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

## First cross-model row (in progress today)

ALP EFT Fig. 8 with `claude-opus-5`, `claude-opus-4-8`, `claude-sonnet-5`, cold memory, one attempt each, on the v2 skills. Results are appended below by `aggregate.py` when the runs finish.
