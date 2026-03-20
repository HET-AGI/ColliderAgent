<!-- prettier-ignore -->
<div align="center">

# ColliderAgent — Magnus Blueprint Scripts

**Cloud-side execution scripts for the ColliderAgent HEP pipeline**

[![Magnus SDK](https://img.shields.io/badge/Magnus%20SDK-0.5.4%2B-7c3aed)](https://github.com/Rise-AGI/magnus)
[![Wolfram Engine](https://img.shields.io/badge/Wolfram%20Engine-required-dd1100?logo=wolfram&logoColor=white)](https://www.wolfram.com/engine/)

> Entry-point scripts executed remotely on the Magnus cloud platform. They handle FeynRules validation, UFO generation, MadGraph5 event generation, and MadAnalysis5 analysis.

[Blueprints](#blueprints) • [Usage](#usage) • [Script Details](#script-details) • [Environment](#environment)

</div>

---

## Overview

The `scripts/` directory contains Python entry points for [Magnus](https://github.com/Rise-AGI/magnus) blueprint execution. Magnus runs these scripts inside containerized environments on a remote or local server — each script corresponds to a named blueprint invoked by the `python-agent` tools.

> [!NOTE]
> These scripts are not meant to be run directly from the command line. They are executed by Magnus blueprints called from [`python-agent/tools/`](../python-agent/tools/).

## Blueprints

| Script | Blueprint name | Description |
|---|---|---|
| `run_feynrules_validation.py` | `validate-feynrules` | Validate `.fr` models via Mathematica (Hermiticity, mass terms, kinetic normalisation) |
| `run_ufo_generation.py` | `generate-ufo` | Export FeynRules models to UFO format via Wolfram Engine |
| `run_madgraph_compile.py` | `madgraph-compile` | Import UFO model, generate diagrams, compile matrix elements |
| `run_madgraph_launch.py` | `madgraph-launch` | Run event generation with beam energy, shower, and detector settings |
| `run_madanalysis_process.py` | `madanalysis-process` | Execute MadAnalysis5 normal-mode analysis on event files |
| `run_demo.py` | `transfer-file` | Demo: write a file and upload it via Magnus (connectivity test) |

## Usage

Each blueprint is invoked via the `magnus run` command:

```bash
magnus run <blueprint-name> -- [options]
```

### Examples

```bash
# Validate a FeynRules model
magnus run validate-feynrules -- \
  --secret <file-secret> \
  --symbol LSM

# Generate UFO model from a .fr file
magnus run generate-ufo -- \
  --secret <file-secret> \
  --lagrangian LSNP \
  --target_path ./NP_UFO

# Compile a MadGraph5 process
magnus run madgraph-compile -- \
  --ufo <ufo-secret> \
  --process "p p > t t~" \
  --target_path ./pp_ttbar

# Launch event generation
magnus run madgraph-launch -- \
  --process_secret <process-secret> \
  --launch_commands "done\nset nevents 1000\ndone" \
  --target_path ./pp_ttbar

# Run MadAnalysis5 analysis
magnus run madanalysis-process -- \
  --events_secret <events-secret> \
  --script "import {EVENTS_DIR}/Events/run_01/unweighted_events.lhe.gz as sample
set sample.type = signal
plot PT(mu+) 50 0 500" \
  --target_path ./ma5_output \
  --level parton
```

## Script Details

### `validate-feynrules`

Validates a FeynRules `.fr` file using Mathematica on the Magnus cloud. Checks Hermiticity (L = L†), diagonal quadratic/mass terms, and kinetic term normalisation.

| Flag | Required | Description |
|---|---|---|
| `--secret` | Yes | FileSecret for the `.fr` model file |
| `--symbol` | Yes | Lagrangian symbol name defined in the `.fr` file |

Returns JSON with `success`, `verdict`, `feynman_gauge`, `unitary_gauge`, and `model_loading` status. Auto-detects standalone vs BSM extension models.

---

### `generate-ufo`

Exports a validated FeynRules model to UFO format using Wolfram Engine. Produces `particles.py`, `parameters.py`, `vertices.py`, and the rest of the UFO directory.

| Flag | Required | Description |
|---|---|---|
| `--secret` | Yes | FileSecret for the `.fr` model file |
| `--lagrangian` | Yes | Lagrangian symbol (e.g. `LSNP`, `LBSM`) |
| `--target_path` | Yes | Download path for the generated UFO directory |
| `--restriction_secret` | No | FileSecret for an optional `.rst` restriction file |

Returns JSON with `success`, `ufo_path`, and any validation warnings.

---

### `madgraph-compile`

Imports a UFO model into MadGraph5, defines processes, generates Feynman diagrams, and produces a compiled process directory.

| Flag | Required | Description |
|---|---|---|
| `--ufo` | No | FileSecret for UFO model directory (mutually exclusive with `--model`) |
| `--model` | No | MG5 built-in model name (e.g. `sm`, `mssm`) |
| `--process` | Yes | Process definition(s), one per line |
| `--definitions` | No | Multiparticle definitions (without the `define` keyword) |
| `--target_path` | Yes | Download path for the compiled process directory |

Returns JSON with `success`, `process_dir`.

---

### `madgraph-launch`

Runs event generation from a compiled MadGraph5 process directory, with Pythia8 parton shower and optional Delphes detector simulation.

| Flag | Required | Description |
|---|---|---|
| `--process_secret` | Yes | FileSecret for the compiled process directory |
| `--launch_commands` | Yes | MG5 launch body (`set` commands, shower/detector flags, `done`) |
| `--target_path` | Yes | Download path for the output directory |
| `--pdf` | No | LHAPDF PDF set name to install |

Returns JSON with `success`, `output_dir`, `cross_section`, `nevents`, `run_name`, and `param_card_warnings`.

---

### `madanalysis-process`

Runs MadAnalysis5 in normal mode on Monte Carlo event files. Produces histograms, cut tables, and cutflow summaries.

| Flag | Required | Description |
|---|---|---|
| `--events_secret` | Yes | FileSecret for the events directory |
| `--script` | Yes | MA5 commands — do **not** include `submit` |
| `--level` | Yes | Analysis level: `parton`, `hadron`, or `reco` |
| `--target_path` | Yes | Download path for analysis output |

Returns JSON with `success`, `output_dir`.

---

### `run_demo.py` (`transfer-file`)

Writes `"Hello world."` to a file and uploads it via Magnus custody. Use this to verify that Magnus connectivity and authentication are working correctly.

## Reference Templates

The `ref/` subdirectory contains Wolfram Mathematica script templates used by the FeynRules blueprints:

| Template | Used by |
|---|---|
| `feynrules_validation_template()` | `run_feynrules_validation.py` |
| `ufo_generation_template()` | `run_ufo_generation.py` |

Templates are rendered and injected into the cloud container at runtime — they are not executed on the host machine.

## Environment

Magnus sets the following environment variables inside the container at runtime:

| Variable | Description |
|---|---|
| `MAGNUS_ACTION` | Path to write the file download action |
| `MAGNUS_RESULT` | Path to write the JSON result |
| `MAGNUS_ADDRESS` | Magnus server address |
| `MAGNUS_TOKEN` | Magnus API token |

## Structure

```
scripts/
├── ref/
│   ├── __init__.py
│   └── wolfram_script_templates.py    # Mathematica templates for FeynRules & UFO
│
├── run_feynrules_validation.py        # Blueprint: validate-feynrules
├── run_ufo_generation.py              # Blueprint: generate-ufo
├── run_madgraph_compile.py            # Blueprint: madgraph-compile
├── run_madgraph_launch.py             # Blueprint: madgraph-launch
├── run_madanalysis_process.py         # Blueprint: madanalysis-process
└── run_demo.py                        # Blueprint: transfer-file (connectivity demo)
```

## See Also

- [**python-agent/**](../python-agent/) — ADK agent whose tools invoke these blueprints
- [**src/skills/**](../src/skills/) — Claude Code skill modules that call blueprints via `magnus run`
- [Magnus Documentation](https://github.com/Rise-AGI/magnus) — cloud platform for HEP workflows
