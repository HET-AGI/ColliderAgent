---
name: madgraph-simulator
description: Run MadGraph5_aMC@NLO event generation for particle physics simulations via Magnus cloud. Triggers when the user wants to generate Monte Carlo events, simulate collider processes, or run MadGraph5. Supports Pythia8 parton shower and Delphes detector simulation.
---

# MadGraph Simulator

## Overview

This skill runs MadGraph5_aMC@NLO for Monte Carlo event generation using two Magnus blueprints executed in sequence:

1. **`madgraph-compile`** — imports the UFO model, defines processes, generates Feynman diagrams, computes matrix elements, and produces a compiled process directory
2. **`madgraph-launch`** — takes the compiled process directory and runs event generation with specified physics parameters, optional Pythia8 shower, and optional Delphes detector simulation

Both steps execute on the Magnus cloud (see magnus skill).

## Output Paths

All paths are **relative to the working directory**. Scripts use relative paths so they can be directly `cp`'d into the reproduction package.

| Output | Path pattern | Example |
|--------|-------------|---------|
| MG5 scripts | `scripts/mg5_<label>.mg5` | `scripts/mg5_7TeV.mg5` |
| Process + events | `events/<process_label>/` | `events/pp_muN_7TeV/` |
| Event files | `events/<process_label>/Events/run_XX/` | `events/pp_muN_7TeV/Events/run_01/` |

**Naming conventions**:
- `<label>`: a short, descriptive tag (typically beam energy or scan label), e.g. `7TeV`, `8TeV`, `14TeV`
- `<process_label>`: MG5 process name + label, e.g. `pp_muN_7TeV`, `pp_ttbar`

When writing MG5 scripts (for local fallback), use relative paths in `output` and `launch` commands:
```
import model SM_HeavyN_UFO
generate p p > mu- n1
output events/pp_muN_7TeV
launch events/pp_muN_7TeV
```

## Workflow

### Step 1: Compile the Process

```bash
magnus run madgraph-compile -- \
  --ufo path/to/MyModel_UFO \
  --process "p p > t t~" \
  --output path/to/pp_ttbar \
  --definitions "l+ = e+ mu+
l- = e- mu-
vl = ve vm
vl~ = ve~ vm~"
```

**Parameters**:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--ufo` | No | Path to UFO model directory (for custom BSM models; mutually exclusive with `--model`) |
| `--model` | No | MG5 built-in model name, e.g. `sm`, `mssm` (mutually exclusive with `--ufo`) |
| `--process` | Yes | Process definition(s), one per line. First line becomes `generate`, rest become `add process` |
| `--output` | Yes | Where to download the compiled process directory |
| `--definitions` | No | Multiparticle definitions, one per line (without the `define` keyword) |

**`--definitions` format**: each line is `label = particle1 particle2 ...`. Do **NOT** include the `define` keyword — the blueprint adds it automatically.

```
# CORRECT:
l+ = e+ mu+

# WRONG (will cause errors):
define l+ = e+ mu+
```

The UFO directory (if provided) is uploaded via FileSecret. When using `--model`, no file upload is needed — MG5 uses its built-in model. You must provide either `--ufo` or `--model` (defaults to `sm` if neither is given).

**WARNING**: If `--output` points to an existing directory, it will be **deleted and replaced** by the download.

**Downloaded directory structure** (example: `--output simulation/pp_ttbar`):
```
simulation/pp_ttbar/
├── Cards/
│   ├── param_card.dat
│   ├── run_card.dat
│   └── ...
├── SubProcesses/
├── Source/
├── bin/
└── ...
```

**Result** (`magnus job result <job-id>`):
- `success` (bool)
- `process_dir` (str): path to compiled process directory

### Between Step 1 and Step 2: Optional Features

Apply these **after** compile and **before** launch, only when the user explicitly requests them. See [references/optional_features.md](references/optional_features.md) for details.

| Feature | Trigger | Effect |
|---------|---------|--------|
| LHCO output | User requests LHCO format | Uncomment `root2lhco` in `bin/internal/run_delphes3` (requires Delphes) |

### Step 2: Launch Event Generation

```bash
magnus run madgraph-launch -- \
  --process path/to/pp_ttbar \
  --commands "done
set nevents 1000
set ebeam1 7000
set ebeam2 7000
done" \
  --output path/to/pp_ttbar
```

**Parameters**:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--process` | Yes | Path to compiled process directory (from Step 1) |
| `--commands` | Yes | MG5 launch body — everything after `launch <dir>` (see state machine below) |
| `--output` | Yes | Where to download the output directory (with Events/) |
| `--pdf` | No | LHAPDF PDF set name to install before running (e.g. `LUXlep-NNPDF31_nlo_as_0118_luxqed`). Downloaded from CERN if not already present. |

The process directory is uploaded via FileSecret. On success, the full output directory (including `Events/run_XX/`) is downloaded to `--output`.

**WARNING**: If `--output` points to an existing directory (e.g. the same path used for compile), it will be **deleted and replaced** by the download. The downloaded directory includes the compiled process plus the generated events.

**Downloaded directory structure** (example: `--output simulation/pp_ttbar`):
```
simulation/pp_ttbar/
├── Cards/
├── Events/
│   └── run_01/
│       ├── unweighted_events.lhe.gz              # always present
│       ├── run_01_tag_1_banner.txt
│       ├── tag_1_pythia8_events.hepmc.gz         # if Pythia8
│       ├── tag_1_delphes_events.lhco.gz          # if Delphes + LHCO enabled (see optional_features.md)
│       └── tag_1_delphes_events.root             # if Delphes
├── SubProcesses/
└── ...
```

**Result** (`magnus job result <job-id>`):
- `success` (bool)
- `output_dir` (str): path to output directory
- `cross_section` (str): e.g. "0.1234 +- 0.005 pb"
- `nevents` (int)
- `run_name` (str): e.g. "run_01"
- `param_card_warnings` (list, if any): duplicate PDG entries in param_card.dat

## launch_commands State Machine

The `--commands` string is processed by MG5 as a sequential state machine with **exactly two states**, regardless of which optional features (Pythia8, Delphes, MadSpin, Reweight) are enabled. Understanding this is critical for correct event generation.

**CRITICAL: `--commands` is ONLY the launch body.** The `madgraph-compile` blueprint already handles `import model`, `define`, `generate`, `add process`, and `output`. NEVER include these commands in `--commands` — they will cause errors. The `--commands` string starts from the point after `launch <dir>` has been issued.

### State 1: Feature switches

Lines before the **first** `done`:
- `shower=Pythia8` — enable Pythia8 parton shower
- `detector=Delphes` — enable Delphes detector simulation
- `madspin=ON` — enable MadSpin spin-correlated decays (see [references/optional_features.md](references/optional_features.md))
- `reweight=ON` — enable matrix-element reweighting
- `done` — accept selections (or skip if none specified) and advance to State 2

### State 2: Card editing (run / param / pythia / delphes / madspin)

Lines between the first `done` and the **second** `done`. MG5 funnels every enabled card through this single editor stage:
- `set nevents <N>` — number of events
- `set ebeam1 <GeV>` / `set ebeam2 <GeV>` — beam energies
- `set param_card <BLOCK> <CODE> <VALUE>` — model parameters
- `set param_card MASS <PDG> <VALUE>` — particle masses
- `set param_card DECAY <PDG> <VALUE>` — set decay width (in GeV)
- `set param_card DECAY <PDG> Auto` — auto-calculate decay width (requires UFO embedded in process dir)
- `set param_card MASS <PDG> scan:[v1,v2,v3,...]` — mass scan
- `set use_syst False` — disable systematics (avoids LHAPDF-related failures when Python LHAPDF is unavailable)
- `set run_card pdlabel lhapdf` — use LHAPDF PDF set (required when using `--pdf`)
- `set run_card lhaid <ID>` — LHAPDF set ID (e.g. `82400` for LUXlep-NNPDF31_nlo_as_0118_luxqed)
- For Delphes: select a built-in card with `set delphes_card cms | atlas | default`, or supply a full path on its own line. Bare card names (`CMS`, `ATLAS`) on their own line are silently swallowed by the v3.7.0 `AskforEditCard` default handler — no card is copied and Delphes runs against whatever `delphes_card.dat` is currently in `Cards/`.
- For MadSpin: `set spinmode none|onshell|full` and `decay <pdg> > <fs>` (MadSpin must be turned on in State 1 with `madspin=ON`; setting `spinmode`/`decay` here without that switch is a silent no-op)
- `done` — start the run

### Summary: number of `done` commands

| Scenario | States visited | `done` count |
|----------|---------------|-------------|
| Any combination (bare / +Pythia8 / +Delphes / +MadSpin / +Reweight) | 1 → 2 | **2** |

### CRITICAL: exactly two `done` commands, no consecutive `done` before `set` commands

There are only two states, so there must be exactly two `done` lines: one to leave State 1, one to launch the run. If you write a second `done` immediately after the first (before any `set` lines), MG5 launches the run **without setting any parameters** and uses defaults.

```
done
set nevents 1000
set ebeam1 7000
set ebeam2 7000
done
```

**NOT**:
```
done
done
set nevents 1000    <-- TOO LATE, run already started
```

**CRITICAL: silent-failure mode after the second `done`.** Once the second `done` is issued, MG5 launches the run and any further `set ...` lines are dispatched to the master prompt (where they are unknown commands and silently swallowed). The job will still report `success=true` because the Results Summary is parsed from the completed run — but the parameters from those late `set` lines were **never applied**. Symptoms: cross-section / nevents / mass values that look like defaults instead of what you requested. Always keep every `set`, every detector card line, and every `decay ...` line **above** the final `done`.

### Reproducibility note

Prompts run against the pre-2026-04 version of this skill silently produced `nevents=10000` (MG5 default) regardless of `set nevents N` because of the old 3-done table. Re-running with this guide produces the requested value. For most analyses (cross-sections, kinematic shapes, exclusion limits) this is purely a statistics improvement — central values do not move, error bars shrink as 1/√N. The only place it changes results is if a downstream script normalizes by the **requested** nevents instead of the file's actual event count.

## Examples

### Parton-level (no shower, no detector)

```bash
# Compile
magnus run madgraph-compile -- \
  --ufo path/to/UFO \
  --process "p p > t t~" \
  --output simulation/pp_ttbar

# Launch
magnus run madgraph-launch -- \
  --process simulation/pp_ttbar \
  --commands "done
set nevents 1000
set ebeam1 7000
set ebeam2 7000
done" \
  --output simulation/pp_ttbar
```

Output events: `simulation/pp_ttbar/Events/run_01/unweighted_events.lhe.gz`

### With Pythia8 + Delphes (CMS detector card)

```bash
magnus run madgraph-launch -- \
  --process simulation/pp_ttbar \
  --commands "shower=Pythia8
detector=Delphes
done
set nevents 1000
set ebeam1 7000
set ebeam2 7000
set param_card MASS 6 172.76
set param_card SMINPUTS 1 127.9
set delphes_card cms
done" \
  --output simulation/pp_ttbar
```

Output events:
- `Events/run_01/tag_1_pythia8_events.hepmc.gz` (hadron-level)
- `Events/run_01/tag_1_delphes_events.root` (reco-level, ROOT)
- `Events/run_01/tag_1_delphes_events.lhco.gz` (reco-level, LHCO; only if enabled — see optional_features.md)

### BSM signal with mass scan and auto-width

```bash
magnus run madgraph-compile -- \
  --ufo path/to/ScalarModel_UFO \
  --process "p p > t h0, t > b l+ vl, h0 > mu+ mu-
p p > t~ h0, t~ > b~ l- vl~, h0 > mu+ mu-" \
  --output simulation/pp_tS \
  --definitions "l+ = e+ mu+
l- = e- mu-
vl = ve vm
vl~ = ve~ vm~"

magnus run madgraph-launch -- \
  --process simulation/pp_tS \
  --commands "shower=Pythia8
detector=Delphes
done
set nevents 100
set ebeam1 7000
set ebeam2 7000
set param_card SMINPUTS 1 127.9
set param_card MASS 6 172.76
set param_card YQLU 2 3 0.001
set param_card MASS 50001 scan:[20,40,60,80,100,120,140,160]
set param_card DECAY 50001 Auto
set delphes_card cms
done" \
  --output simulation/pp_tS
```

### Lepton-initiated process with LUXlep PDF

```bash
# Compile (using SM model with lepton beams)
magnus run madgraph-compile -- \
  --model sm \
  --process "e+ u > e+ u" \
  --output simulation/ep_u

# Launch with LUXlep PDF set
magnus run madgraph-launch -- \
  --process simulation/ep_u \
  --pdf LUXlep-NNPDF31_nlo_as_0118_luxqed \
  --commands "done
set run_card pdlabel lhapdf
set run_card lhaid 82400
set nevents 1000
set ebeam1 7000
set ebeam2 7000
done" \
  --output simulation/ep_u
```

The `--pdf` flag downloads the specified LHAPDF PDF set into the cloud container before MG5 runs. You must also set `pdlabel` and `lhaid` in `--commands` to tell MG5 to use it.

### MadSpin decays + Pythia8 + Delphes (top-pair, dilepton final state)

Use MadSpin when you want spin-correlated decays applied **after** the hard event is generated (instead of writing the decays into the `--process` string at compile time). MadSpin needs to be switched on in State 1 (`madspin=ON`) **and** configured in State 2 (`set spinmode ...` plus one `decay <pdg> > <fs>` line per unstable particle to decay).

```bash
# Compile the undecayed process
magnus run madgraph-compile -- \
  --model sm \
  --process "p p > t t~" \
  --output simulation/pp_ttbar_madspin \
  --definitions "l+ = e+ mu+
l- = e- mu-
vl = ve vm
vl~ = ve~ vm~"

# Launch with MadSpin + Pythia8 + Delphes
magnus run madgraph-launch -- \
  --process simulation/pp_ttbar_madspin \
  --commands "shower=Pythia8
detector=Delphes
madspin=ON
done
set nevents 1000
set ebeam1 6500
set ebeam2 6500
set param_card MASS 6 172.76
set delphes_card cms
set spinmode onshell
decay t > b l+ vl
decay t~ > b~ l- vl~
done" \
  --output simulation/pp_ttbar_madspin
```

Output events (in addition to the usual files):
- `Events/run_01/unweighted_events.lhe.gz` — original undecayed events
- `Events/run_01_decayed_1/unweighted_events.lhe.gz` — MadSpin-decayed events fed to Pythia8/Delphes
- `Events/run_01_decayed_1/tag_1_pythia8_events.hepmc.gz`
- `Events/run_01_decayed_1/tag_1_delphes_events.root`

## Key MG5 Syntax

### Process definition

```
p p > t t~                                    # Simple
p p > t t~, t > b l+ vl, t~ > b~ l- vl~      # With decay chains
```

Use `add process` (second line onward in `--process`) for charge-conjugate states.

### Multiparticle definitions

```
l+ = e+ mu+ ta+
l- = e- mu- ta-
vl = ve vm vt
vl~ = ve~ vm~ vt~
j = g u c d s u~ c~ d~ s~
```

### Setting parameters (in launch_commands)

```
set param_card MASS <pdg> <value>              # Set mass
set param_card <BLOCK> <code> <value>          # Set coupling
set param_card DECAY <pdg> <value>             # Set width (GeV)
set param_card DECAY <pdg> Auto                # Auto-calculate width
set param_card MASS <pdg> scan:[v1,v2,...]     # Mass scan
```

If the caller provides PDG codes and block/code values, use them directly. Otherwise, read the UFO model's `particles.py` and `parameters.py` to find the correct PDG codes and block/code values.

### param_card duplicate PDG warning

The launch blueprint checks `param_card.dat` for duplicate PDG entries in the MASS block and DECAY declarations. If found, the result includes `param_card_warnings`. This typically indicates duplicate external/dependent mass entries in the UFO model's `parameters.py` — fix the `.fr` model and regenerate UFO.

## Reference Documentation

- See [references/madgraph_reference.md](references/madgraph_reference.md) for the complete MG5 command reference, including decay chain syntax, common processes, Pythia8/Delphes integration, parameter settings, and troubleshooting
- See [references/optional_features.md](references/optional_features.md) for optional features (LHCO output, etc.) applied between compile and launch
