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
| `--interactive` | No | Boolean. Use MG5 `launch -i` mode to run shower/detector on existing events. See [Interactive mode](#interactive-mode-launch--i) below. |

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

The `--commands` string is processed by MG5 as a sequential state machine. Understanding this is critical for correct event generation.

**CRITICAL: `--commands` is ONLY the launch body.** The `madgraph-compile` blueprint already handles `import model`, `define`, `generate`, `add process`, and `output`. NEVER include these commands in `--commands` — they will cause errors. The `--commands` string starts from the point after `launch <dir>` has been issued.

### State 1: Shower/Detector selection

Lines before the **first** `done`:
- `shower=Pythia8` — enable Pythia8 parton shower
- `detector=Delphes` — enable Delphes detector simulation
- `done` — accept selections (or skip if none specified) and advance

### State 2: Card editing (only when shower or detector is enabled)

Lines between the first `done` and the **second** `done`:
- For Delphes: specify the detector card (`CMS`, `ATLAS`, or a full path)
- `done` — accept defaults and move to State 3

**When no shower or detector is selected**, State 1's `done` skips directly to State 3 (parameter setting). State 2 does not appear.

### State 3: Parameter setting

Lines after the preceding `done`:
- `set nevents <N>` — number of events
- `set ebeam1 <GeV>` / `set ebeam2 <GeV>` — beam energies
- `set param_card <BLOCK> <CODE> <VALUE>` — model parameters
- `set param_card MASS <PDG> <VALUE>` — particle masses
- `set param_card DECAY <PDG> <VALUE>` — set decay width (in GeV)
- `set param_card DECAY <PDG> Auto` — auto-calculate decay width (requires UFO embedded in process dir)
- `set use_syst False` — disable systematics (avoids LHAPDF-related failures when Python LHAPDF is unavailable)
- `set run_card pdlabel lhapdf` — use LHAPDF PDF set (required when using `--pdf`)
- `set run_card lhaid <ID>` — LHAPDF set ID (e.g. `82400` for LUXlep-NNPDF31_nlo_as_0118_luxqed)

**CRITICAL: LUXlep PDF LHAID** — When using LUXlep PDF, the correct LHAID is **82400** (for `LUXlep-NNPDF31_nlo_as_0118_luxqed`). Do NOT use 82200 — that is a different, incompatible PDF set.
- `set param_card MASS <PDG> scan:[v1,v2,v3,...]` — mass scan
- `done` — start the run

### Summary: number of `done` commands

| Scenario | States visited | `done` count |
|----------|---------------|-------------|
| No shower, no detector | 1 → 3 | **2** |
| Pythia8 and/or Delphes | 1 → 2 → 3 | **3** |

### CRITICAL: no consecutive `done` before `set` commands

The `done` that ends State 1 (or State 2) transitions into State 3. If you immediately write another `done`, MG5 starts the run **without setting any parameters**. Always place `set` commands before the final `done`:

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

## Interactive mode (`launch -i`)

When `--interactive true` is passed, the blueprint uses MG5's `launch -i` mode instead of the normal `launch`. This mode operates on **existing events** in the process directory — it does NOT re-generate events.

**Use case**: Run Pythia8 shower and/or Delphes detector simulation on an already-generated LHE file. This is essential for the [lepton-from-proton with shower workflow](#lepton-from-proton-with-luxlep-pdf-and-pythia8-shower).

**`--commands` syntax in interactive mode** is different from the state machine above. Use MG5 madevent interactive commands:

```
pythia8 run_01
delphes run_01
```

- `pythia8 run_XX` — run Pythia8 shower on the LHE of run_XX
- `delphes run_XX` — run Delphes detector simulation on the shower output of run_XX

Do NOT use the state machine syntax (`shower=Pythia8`, `detector=Delphes`, `done`) with `--interactive`.

**Example**:
```bash
magnus run madgraph-launch -- \
  --process simulation/pp_ej \
  --interactive true \
  --commands "pythia8 run_01
delphes run_01" \
  --output simulation/pp_ej
```

**Output**: The shower/detector output files get a new tag (e.g., `tag_3_pythia8_events.hepmc`, `tag_3_delphes_events.lhco.gz`) under `Events/run_01/`.

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
CMS
done
set nevents 1000
set ebeam1 7000
set ebeam2 7000
set param_card MASS 6 172.76
set param_card SMINPUTS 1 127.9
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
CMS
done
set nevents 100
set ebeam1 7000
set ebeam2 7000
set param_card SMINPUTS 1 127.9
set param_card MASS 6 172.76
set param_card YQLU 2 3 0.001
set param_card MASS 50001 scan:[20,40,60,80,100,120,140,160]
set param_card DECAY 50001 Auto
done" \
  --output simulation/pp_tS
```

### Lepton-from-proton with LUXlep PDF (parton-level only)

```bash
# Compile: redefine proton to include photon and leptons
magnus run madgraph-compile -- \
  --ufo path/to/MyModel_UFO \
  --process "p p > e- j NP=2" \
  --definitions "p = g u c d s u~ c~ d~ s~ b b~ a e+ e- mu+ mu- ta+ ta-" \
  --output simulation/pp_ej

# Launch: parton-level only (no shower)
magnus run madgraph-launch -- \
  --process simulation/pp_ej \
  --commands "done
set nevents 10000
set ebeam1 6500
set ebeam2 6500
set lpp1 1
set lpp2 1
set run_card pdlabel lhapdf
set run_card lhaid 82400
set run_card bypass_check partonshower
set use_syst False
done" \
  --output simulation/pp_ej
```

Key points:
- The initial state **must** be `p p` (proton-proton), not `e u` or similar. The lepton is extracted from the proton's PDF, not used as an explicit beam particle.
- `--definitions` redefines the proton multiparticle label to include `a e+ e- mu+ mu- ta+ ta-` so MG5 generates lepton-initiated subprocesses.
- `set lpp1 1` and `set lpp2 1` are required. When the proton definition includes leptons, MG5 automatically sets `lpp1=0` (no PDF for beam 1). You must explicitly override both `lpp1` and `lpp2` back to 1 (proton PDF).
- `set run_card bypass_check partonshower` is needed because MG5 by default disables Pythia8 when the proton definition includes leptons; this flag suppresses that check even when generating parton-level only.

### Lepton-from-proton with LUXlep PDF AND Pythia8 shower

Pythia8 **cannot** backward-evolve initial-state leptons from proton PDFs. The workaround is a 3-step process: generate parton-level LHE, locally patch the LHE to replace initial-state leptons with photons, then run shower+detector on the patched LHE via interactive mode.

```bash
# Step 1: Compile (same as parton-level)
magnus run madgraph-compile -- \
  --ufo path/to/MyModel_UFO \
  --process "p p > e- j NP=2" \
  --definitions "p = g u c d s u~ c~ d~ s~ b b~ a e+ e- mu+ mu- ta+ ta-" \
  --output simulation/pp_ej

# Step 2: Launch parton-level only (no shower, no detector)
magnus run madgraph-launch -- \
  --process simulation/pp_ej \
  --commands "done
set nevents 10000
set ebeam1 6500
set ebeam2 6500
set lpp1 1
set lpp2 1
set run_card pdlabel lhapdf
set run_card lhaid 82400
set run_card bypass_check partonshower
set use_syst False
done" \
  --output simulation/pp_ej

# Step 3: Patch LHE — replace initial-state leptons with photons
python3 scripts/patch_lhe_lepton_to_photon.py \
  simulation/pp_ej/Events/run_01/unweighted_events.lhe.gz \
  simulation/pp_ej/Events/run_01/unweighted_events.lhe.gz

# Step 4: Run Pythia8 + Delphes on patched LHE via interactive mode
magnus run madgraph-launch -- \
  --process simulation/pp_ej \
  --interactive true \
  --commands "pythia8 run_01
delphes run_01" \
  --output simulation/pp_ej
```

Key points:
- `set lpp1 1` and `set lpp2 1` are required in Step 2. When the proton definition includes leptons, MG5 automatically sets `lpp1=0` (no PDF for beam 1). You must explicitly override both back to 1.
- Step 2 generates parton-level LHE only — no shower or detector.
- Step 3 uses `scripts/patch_lhe_lepton_to_photon.py` to replace all initial-state lepton PDG codes (status = -1, PDG +-11/+-13/+-15) with photon (PDG 22) in the LHE file. This allows Pythia8 to backward-evolve the initial state correctly. The script can patch in-place (same input and output path).
- Step 4 uses `--interactive true` with `pythia8 run_01` / `delphes run_01` commands to run shower and detector simulation on the patched LHE.
- The `pythia8_card.dat` in the process directory should contain `Check:event = off` and `Check:history = off` to prevent Pythia8 from rejecting the patched events due to charge conservation checks (the initial-state photon replacing a lepton changes the total charge balance seen by Pythia8's validator).
- Without this patching workflow, Pythia8 produces ~67% `partonLevel failed` retries and massive color-tracing errors. With the patch, Pythia8 runs cleanly with zero shower errors.

## Key MG5 Syntax

### Process definition

**RULE: For LHC processes, the initial state MUST always be `p p`.** The LHC is a proton-proton collider — never use quark/gluon-level initial states (e.g. `g g >`, `u u~ >`) for LHC processes.

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
