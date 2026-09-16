---
name: madgraph-simulator
description: Generate Monte Carlo events with MadGraph5_aMC@NLO on the Magnus cloud, from process compilation through event generation, with optional Pythia8 shower, Delphes detector simulation, MadSpin decays, LHAPDF sets, parameter scans, and LHCO output. Use whenever a task needs collider events or cross sections from MadGraph5.
---

# MadGraph Simulator

Two blueprints, run in order (execution mechanics, upload/download, recovery: magnus skill):

1. `madgraph-compile` — imports the model, defines the process, generates diagrams and matrix elements, returns the compiled process directory.
2. `madgraph-launch` — runs event generation in that directory with your run/param settings and optional Pythia8, Delphes, MadSpin.

## Paths (relative to the working directory)

| Output | Path | Example |
|---|---|---|
| MG5 script (one per launch, the reproducible record) | `scripts/mg5_<label>.mg5` | `scripts/mg5_7TeV.mg5` |
| Process directory + events | `events/<process_label>/` | `events/pp_muN_7TeV/` |
| Event files | `events/<process_label>/Events/<run_name>/` | `events/pp_muN_7TeV/Events/run_01/` |

The script mirrors what the two blueprints did (`import model`, `define`, `generate`, `output events/…`, `launch events/…`, the launch body) with relative paths, so it can be replayed locally or copied into a reproduction package.

## Step 1: compile

```bash
magnus run madgraph-compile -- \
  --ufo models/MyModel_UFO \
  --process "p p > t t~" \
  --output events/pp_ttbar \
  --definitions "l+ = e+ mu+
l- = e- mu-"
```

| Parameter | Required | Meaning |
|---|---|---|
| `--ufo` | one of the two | UFO directory (uploaded); `--model` names an MG5 built-in model (`sm`, `mssm`, …) instead; neither → `sm` |
| `--process` | yes | one process per line; the first becomes `generate`, the rest `add process` (decay chains `p p > t t~, t > b l+ vl` are allowed) |
| `--output` | yes | where the compiled directory is downloaded |
| `--definitions` | no | multiparticle lines `label = p1 p2 …` **without** the `define` keyword — the blueprint prepends it, so writing it yourself produces `define define …` and an MG5 error |

Result: `success`, `process_dir`. The downloaded directory has `Cards/` (`param_card.dat`, `run_card.dat`, `pythia8_card.dat`, `delphes_card_*.dat`), `bin/`, `SubProcesses/`, `Source/`.

Omitting `--process` only imports the model (the UFO import test in the feynrules-model-validator skill).

## Step 2: launch

```bash
magnus run madgraph-launch -- \
  --process events/pp_ttbar \
  --commands "done
set nevents 10000
set ebeam1 6500
set ebeam2 6500
done" \
  --output events/pp_ttbar
```

| Parameter | Required | Meaning |
|---|---|---|
| `--process` | yes | compiled directory from step 1 (uploaded) |
| `--commands` | yes | the launch body: everything MG5 reads after `launch <dir>` (state machine below). Never include `import`, `define`, `generate`, `output`, or `launch` here; compile already did them and they error in this context |
| `--output` | yes | download path; using the process directory itself puts `Events/` where the scripts expect it |
| `--pdf` | no | LHAPDF set to install first (e.g. `LUXlep-NNPDF31_nlo_as_0118_luxqed`); pair it with `set run_card pdlabel lhapdf` and `set run_card lhaid <id>` in the commands |

Result: `success`, `output_dir`, `cross_section` (e.g. `"0.1234 +- 0.005 pb"`), `nevents`, `run_name`, and `param_card_warnings` when the MASS/DECAY blocks contain duplicate PDG entries (a UFO defect: fix the `.fr`, regenerate).

Files per run, in `Events/<run_name>/`: `unweighted_events.lhe.gz` always; `tag_1_pythia8_events.hepmc.gz` with Pythia8; `tag_1_delphes_events.root` with Delphes; `tag_1_delphes_events.lhco.gz` only after enabling LHCO (below); `run_XX_decayed_1/` with the decayed events when MadSpin ran. `run_name` increments (`run_02`, …) when the directory already holds runs.

### The launch body has exactly two states

MG5 v3.7.0 reads the body as two prompts separated by `done`, whatever features you enable:

1. **Switches** (before the first `done`): `shower=Pythia8`, `detector=Delphes`, `madspin=ON`, `reweight=ON`. With no switches the first line is just `done`.
2. **Cards** (between the first and the second `done`): every `set …` line, the Delphes card choice, and MadSpin `set spinmode` / `decay` lines. The second `done` starts the run.

So the body always has exactly two `done` lines and every setting sits between them. Lines after the second `done` reach a prompt where they are unknown commands and are dropped without error: the job still returns `success: true` with the MG5 defaults (10000 events, default masses). Two consecutive `done` lines have the same effect. The check is cheap: compare the result's `nevents` and `cross_section` with the request.

Settings available in the cards state:

```
set nevents <N>
set ebeam1 <GeV>                          set ebeam2 <GeV>
set param_card MASS <pdg> <value>         set param_card <BLOCK> <code> <value>
set param_card DECAY <pdg> <GeV|Auto>     # Auto needs the UFO embedded in the process dir
set param_card MASS <pdg> scan:[v1,v2,…]  # one job, one run per point (run_01, run_02, …)
set use_syst False                        # skip systematics; avoids LHAPDF-python failures
set run_card pdlabel lhapdf               set run_card lhaid <id>
set delphes_card cms | atlas | default    # bare card names on their own line are ignored
set spinmode none|onshell|full            decay t > b l+ vl        # only with madspin=ON
```

PDG codes and `BLOCK`/`code` pairs come from the UFO's `particles.py` and `parameters.py` (or the step 1 sidecar). MG5 built-in models use the SLHA blocks in `Cards/param_card.dat`.

### Optional features

| Feature | How | Where documented |
|---|---|---|
| Pythia8 shower, Delphes | switches in state 1, card in state 2 | above; card behaviour in `references/madgraph_reference.md` |
| MadSpin spin-correlated decays | `madspin=ON` + `set spinmode` + `decay` lines; verify `run_XX_decayed_1/` exists afterwards | `references/optional_features.md` |
| LHCO output | edit `bin/internal/run_delphes3` in the compiled directory between compile and launch (needs Delphes) | `references/optional_features.md` |
| Lepton-initiated processes | `--pdf LUXlep-…` + `pdlabel lhapdf` + `lhaid 82400`; Pythia8 cannot shower lepton beams — see the lepton→photon workaround | `references/madgraph_reference.md` |

Worked examples for each configuration: `references/examples.md`. Full MG5 syntax (decay chains, cuts, PDF settings, Pythia8/Delphes cards, troubleshooting): `references/madgraph_reference.md`.
