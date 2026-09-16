---
name: madanalysis-analyzer
description: Analyze Monte Carlo event files with MadAnalysis5 on the Magnus cloud — kinematic distributions, event selections, and cut-flow tables at parton (LHE), hadron (HepMC), or reconstruction (LHCO/ROOT) level. Use whenever a task asks for MadAnalysis5 histograms or cut flows on generated events.
---

# MadAnalysis Analyzer

Runs MadAnalysis5 in normal mode through the `madanalysis-process` blueprint (execution mechanics, upload/download, recovery: magnus skill).

## Paths (relative to the working directory)

| Output | Path | Example |
|---|---|---|
| MA5 script (one per analysis, the reproducible record) | `scripts/ma5_<label>.ma5` | `scripts/ma5_dilepton.ma5` |
| Analysis output | `analysis/<label>/` | `analysis/dilepton_mass/` |

## Running an analysis

```bash
magnus run madanalysis-process -- \
  --events events/pp_ttbar \
  --script "import {EVENTS_DIR}/Events/run_01/unweighted_events.lhe.gz as sample
set sample.type = signal
plot PT(mu+) 50 0 500
plot M(mu+ mu-) 100 0 200
select N(mu+) >= 1" \
  --output analysis/dilepton \
  --level parton
```

| Parameter | Required | Meaning |
|---|---|---|
| `--events` | yes | the process directory from `madgraph-launch` (the one containing `Events/`); it is uploaded whole |
| `--script` | yes | MA5 commands; `{EVENTS_DIR}` is replaced on the cloud by the upload location, so import paths are `{EVENTS_DIR}/Events/<run>/<file>` |
| `--output` | yes | download path for the analysis output |
| `--level` | yes | `parton` (LHE), `hadron` (HepMC, FastJet available), `reco` (LHCO or Delphes ROOT); it must match the file format or MA5 rejects the import |

Leave `submit` out of the script: the runner appends `submit analysis_output` itself and strips any `submit` you write, so a hand-written one only changes the output name expectations. Result: `success`, `output_dir`.

Downloaded tree (`--output analysis/dilepton`):

```
analysis/dilepton/
├── Output/
│   ├── HTML/MadAnalysis5job_0/index.html, selection_N.png   # one selection_N per plot/cut
│   ├── PDF/  DVI/                                          # the same report
│   ├── Histos/                                             # histogram data
│   └── SAF/…/Cutflows/*.saf, Histograms/histos.saf         # machine-readable cut flow + histograms
├── Build/                                                  # generated C++ (Log/ holds the run log)
└── Input/
```

`Output/SAF` is what downstream scripts should read; `HTML` is for humans.

## Choosing the input file

Per run directory the formats are `unweighted_events.lhe.gz` (parton), `tag_1_pythia8_events.hepmc.gz` (hadron), `tag_1_delphes_events.lhco.gz` and `tag_1_delphes_events.root` (reco). Use the highest level the task's analysis needs and that exists; a parton-level analysis of showered events is a different measurement, not a fallback.

## Script essentials

```
import {EVENTS_DIR}/Events/run_01/tag_1_delphes_events.lhco.gz as signal
set signal.type = signal          # or background
set signal.xsection = 0.123       # pb, when MA5 should normalise
set main.lumi = 100               # fb^-1
set main.normalize = lumi

plot PT(mu[1]) 50 0 500           # leading muon pT; mu[2] is sub-leading
plot MET 50 0 500
plot M(mu+ mu-) 100 0 200
plot N(j) 15 0 15

select N(mu) >= 2                 # cuts apply in order (AND); the order defines the cut flow
select PT(mu[1]) > 25
reject MET < 50
select 80 < M(mu+ mu-) < 100
```

Multiple datasets (signal vs background, several mass points) can share one script; separate analyses (different runs or levels) are separate jobs and can be submitted in parallel.

Full command reference (observables, `define` labels, selection syntax, SAF cut-flow format, more examples, troubleshooting): `references/madanalysis_reference.md`.
