<!-- prettier-ignore -->
<div align="center">

# ColliderAgent — Python Agent

**Google ADK-based LLM Agent for Particle Physics Simulations**

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776ab?logo=python&logoColor=white)](https://www.python.org)
[![Google ADK](https://img.shields.io/badge/Google%20ADK-compatible-4285f4?logo=google&logoColor=white)](https://google.github.io/adk-docs/)
[![Magnus SDK](https://img.shields.io/badge/Magnus%20SDK-0.5.4%2B-7c3aed)](https://github.com/Rise-AGI/magnus)
[![uv](https://img.shields.io/badge/uv-recommended-de5fe9)](https://github.com/astral-sh/uv)

> Standalone ADK agent that converts LaTeX Lagrangians into validated FeynRules models, runs Monte Carlo event generation with MadGraph5, and analyzes results with MadAnalysis5.

[Installation](#installation) • [Quick Start](#quick-start) • [Tools](#tools-reference) • [Structure](#project-structure) • [See Also](#see-also)

</div>

---

## Overview

The `python-agent` module is a **self-contained ADK agent** for the full HEP simulation pipeline. It can be used independently of the Claude Code / Magnus skill infrastructure — ideal for direct API integration, scripting, or custom workflows.

```
LaTeX Lagrangian → FeynRules .fr → UFO Model → MadGraph5 Events → MadAnalysis5 Analysis
```

## Installation

### With uv (recommended)

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install all dependencies
uv sync
```

> [!TIP]
> Run `python CLI.py` for an interactive guided setup that installs uv, syncs dependencies, and walks you through configuring `.env`.

### With pip

```bash
pip install -r requirements.txt
```

### Environment variables

Copy `.env.example` to `.env` and fill in the required values:

```bash
cp .env.example .env
```

| Variable | Required | Description |
|---|---|---|
| `COLLIDER_AGENT_MODEL` | Yes | LiteLLM model string, e.g. `openai/gpt-4o` |
| `OPENAI_API_KEY` | Yes | API key for your LLM provider |
| `OPENAI_BASE_URL` | No | Custom base URL (for proxy or alternative providers) |
| `MAGNUS_ADDRESS` | Yes | Magnus server URL for remote Mathematica execution |
| `MAGNUS_TOKEN` | Yes | Magnus API token |
| `MG5_PATH` | No | Path to `MG5_aMC` binary directory |
| `MA5_PATH` | No | Path to MadAnalysis5 binary directory |

## Quick Start

### Command line

```bash
# Full pipeline: Lagrangian → .fr → UFO → Events → Analysis
python agent.py "Generate a FeynRules model for L = -y_S S \bar{l}_i P_L l_j + h.c., then simulate pp→SS at 13 TeV"

# Generate .fr file only, skip simulation
python agent.py "Generate FeynRules code for ..." --skip-madgraph

# Write output to a specific file
python agent.py "..." --output-file outputs/MyModel.fr

# Set maximum agent turns
python agent.py "..." --max-turns 30
```

### Programmatic usage

```python
from agent import FeynRulesAgent

agent = FeynRulesAgent(output_dir="outputs")

result = agent.run(
    task="Generate FeynRules model for: L = -y_S S \\bar{l}_i P_L l_j + h.c.",
    max_turns=30,
)

if result["success"]:
    print(result["response"])
    agent.save_session("session.json")
```

### Input format

The agent accepts free-form physics descriptions. For best results, include a Lagrangian and symbol definitions:

```markdown
## Lagrangian
$$\mathcal{L} = -\frac{1}{\sqrt{2}} S \left( y_{L,ij} \bar{l}_i P_L l_j + y_{R,ij} \bar{l}_i P_R l_j \right) + \text{h.c.}$$

## Symbol Definitions
- S: real scalar, electrically neutral, color singlet
- y_L, y_R: left/right-handed Yukawa couplings (3×3 complex matrices)
- l_i: charged lepton field (i = flavor index)
- P_L, P_R: chiral projection operators
```

## Tools Reference

The agent has access to three categories of tools:

### File operations

| Function | Description |
|---|---|
| `read(file_path)` | Read file contents, with optional line offset/limit |
| `write(file_path, content)` | Write content to file |
| `edit(file_path, old_string, new_string)` | Replace a unique string in a file |

### FeynRules & UFO

| Function | Description |
|---|---|
| `validate_feynrules(model_path, symbol)` | Validate a `.fr` file via Magnus cloud (Hermiticity, mass diagonalization, kinetic terms) |
| `generate_ufo_model(fr_path, lagrangian, ufo_path)` | Export a FeynRules model to UFO format via Wolfram Engine |

`validate_feynrules` returns `{success, verdict, feynman_gauge, unitary_gauge}` and auto-detects standalone vs BSM extension models.

### MadGraph5 & MadAnalysis5

| Function | Description |
|---|---|
| `madgraph_compile(ufo_path, process, target_path)` | Import UFO model, generate diagrams, compile matrix elements |
| `madgraph_launch(process_dir, launch_commands, target_path)` | Run event generation with beam energy, cuts, shower/detector settings |
| `generate_simulation_yaml(yaml_path, process_name, ...)` | Write a YAML-based simulation config |
| `run_from_yaml(yaml_path, process_name)` | Execute a simulation defined in YAML |
| `read_event_index(yaml_path, process_name, event_set)` | Locate event files from a YAML config |
| `madanalysis_process(events_path, script, target_path, level)` | Run MA5 normal-mode analysis (histograms, cuts, cutflow) |

> [!NOTE]
> MadGraph5 uses a two-step workflow: **compile** first (enumerate diagrams, build matrix elements), then **launch** (generate events). This separation allows reusing compiled processes across multiple run configurations.

## Project Structure

```
python-agent/
├── agent.py                          # FeynRulesAgent — ADK InMemoryRunner loop
│
├── CLI.py                            # Interactive setup: uv, venv, .env config
├── conftest.py                       # Pytest root config
│
├── tools/                            # Tool implementations
│   ├── __init__.py                   # Re-exports all tools
│   ├── file_tools.py                 # read / write / edit
│   ├── feynrules_validation.py       # validate_feynrules()
│   ├── feynrules_to_ufo.py           # generate_ufo_model()
│   ├── madgraph_tools.py             # madgraph_compile() / madgraph_launch()
│   ├── madanalysis_tools.py          # read_event_index() / madanalysis_process()
│   └── simulation_yaml_to_madgraph.py  # generate_simulation_yaml() / run_from_yaml()
│
├── utils/                            # Utilities (not used by agent directly)
│   ├── build_default_mappings.py     # Build symbol DB from reference models
│   ├── build_symbol_database.py      # Alternative symbol database builder
│   ├── download_feynrules_models.py  # Download 100+ reference .fr models
│   └── madgraph_setup.py            # MadGraph environment setup helpers
│
├── prompts/                          # Reference documentation for the agent
│   ├── feynrules_reference.md
│   ├── madgraph_reference.md
│   └── madanalysis_reference.md
│
├── templates/                        # FeynRules file templates
│   ├── lagrangian_template.txt
│   ├── parameters_template.txt
│   ├── classes_template.txt
│   └── model_info_template.txt
│
└── tests/                            # Test suite
    ├── conftest.py
    ├── test_e2e_pipeline.py
    ├── test_madgraph_tools.py
    ├── test_simulation_workflow.py
    └── assets/                       # Reference .fr models and scripts
```

### Output structure

```
outputs/
├── MyModel.fr                         # FeynRules model file
├── MyModel_UFO/                       # UFO model directory
│   ├── particles.py
│   ├── parameters.py
│   └── vertices.py
├── simulation.yaml                    # Simulation configuration
└── pp_XX/                            # MadGraph project directory
    ├── Cards/
    │   ├── param_card.dat
    │   └── run_card.dat
    └── Events/run_01/
        ├── unweighted_events.lhe.gz       # Parton-level
        ├── tag_1_pythia8_events.hepmc.gz  # Hadron-level
        └── tag_1_delphes_events.lhco.gz   # Reco-level
```

## See Also

- [**scripts/**](../scripts/) — Magnus cloud blueprint execution scripts called by the tools above
- [**src/skills/**](../src/skills/) — Claude Code skill modules for the same HEP tools
- [**paper-reproduction/**](../paper-reproduction/) — Example prompts reproducing figures from physics papers
