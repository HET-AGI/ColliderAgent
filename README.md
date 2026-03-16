<!-- prettier-ignore -->

<div align="center">

# ⚛ Collider-Agent

**An End-to-end Architecture for Collider Physics and Beyond**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776ab?logo=python&logoColor=white)](https://www.python.org)
[![Claude Code](https://img.shields.io/badge/Claude_Code-compatible-7c3aed)](https://claude.ai/code)
![Status](https://img.shields.io/badge/status-beta-orange)

> From a LaTeX Lagrangian to a publication-ready figure — fully automated.

[Overview](#overview) • [Quickstart](#quickstart) • [Installation](#installation) • [Examples](#example-prompts) • [Citation](#citation)


<img src="images/architecture.svg" alt="Architecture" width="900" />

</div>


## Overview

Collider-Agent enables AI coding agents (Claude Code, Cursor, Windsurf, and more) to autonomously reproduce collider phenomenology results from physics papers. It combines specialized sub-agents and reusable skill modules that interface with standard HEP tools via the [Magnus](https://github.com/Rise-AGI/magnus) cloud platform — no local HEP software installation required.

**Full pipeline, fully automated:**

- Parse a LaTeX Lagrangian and generate a FeynRules model
- Validate the model and produce a UFO output for MadGraph5
- Run parton-level and showered event generation with MadGraph5 + Pythia8
- Apply detector simulation (Delphes) and analysis cuts (MadAnalysis5)
- Generate kinematic distributions, cutflow tables, exclusion contours in parameter space, etc.

## Roadmap

| Status | Feature                                                                       |
|:------:| ----------------------------------------------------------------------------- |
| ✅      | FeynRules model generation from LaTeX Lagrangian                              |
| ✅      | FeynRules model validation (Hermiticity, mass diagonalization, kinetic terms) |
| ✅      | UFO model generation for MadGraph5                                            |
| ✅      | MadGraph5 event generation with Pythia8 parton shower                         |
| ✅      | Delphes detector simulation                                                   |
| ✅      | MadAnalysis5 normal mode analysis                                             |
| ✅      | Multi-agent orchestration for full pipeline                                   |
| ⬜      | MadAnalysis5 expert mode support                                              |
| ⬜      | Fine-grained parameter tuning for Pythia and other packages                   |
| ⬜      | More paper reproduction examples (contributions welcome!)                     |

## Installation

### Prerequisites

- [Claude Code](https://claude.ai/code) — recommended; provides full support for both sub-agents and skills
  
  > Other agents with skills support also work (skills only, no sub-agents): Cursor, Windsurf, Gemini CLI, Cline, Goose, Roo Code, and [more](#supported-agents-and-their-global-skills-paths)

- Python 3.10+ (requires `magnus-sdk>=0.7.0`)

### Setup

**1. Clone the repository:**

```bash
git clone https://github.com/HET-AGI/ColliderAgent.git
cd ColliderAgent
```

**2. Connect to the Magnus platform:**

First, install the Magnus SDK:

```bash
pip install magnus-sdk
```

<details>
<summary>☁️ Option A: Connect to an existing cloud instance</summary>

If you have access to a cloud-hosted Magnus instance, authenticate with:

```bash
magnus login
```

Enter your server URL and API key when prompted. All subsequent commands are routed to the remote backend automatically.

</details>

<details>
<summary>🖥️ Option B: Local deployment</summary>

**Additional prerequisites:** Docker (daemon running), Node.js (optional, enables the Web UI)

Start the local backend:

```bash
magnus local start
```

This fetches the Magnus source, installs backend dependencies, starts the server on port `8017`, and creates a local database and user account. If Node.js is installed, a Web UI is also launched at `http://localhost:3011`.

Verify the setup:

```bash
magnus run hello-world
```

A successful run prints `Hello from Magnus!` after pulling the required container image.

</details>

> For full Magnus documentation and deployment options, see [github.com/Rise-AGI/magnus](https://github.com/Rise-AGI/magnus).

**3. Copy agents and skills to your agent's configuration directory.**

For **Claude Code** (full support: sub-agents + skills):

```bash
cp -r src/agents ~/.claude/agents
cp -r src/skills ~/.claude/skills
```

For **other agents** (skills only):

```bash
# Replace <skills-path> with the global skills path for your agent (see table below)
cp -r src/skills <skills-path>
```

<a id="supported-agents-and-their-global-skills-paths"></a>

**Supported agents and their global skills paths:**

| Agent          | Global skills path            |
| -------------- | ----------------------------- |
| Claude Code    | `~/.claude/skills/`           |
| Cursor         | `~/.cursor/skills/`           |
| Windsurf       | `~/.codeium/windsurf/skills/` |
| GitHub Copilot | `~/.copilot/skills/`          |
| Gemini CLI     | `~/.gemini/skills/`           |
| Cline / Warp   | `~/.agents/skills/`           |
| Goose          | `~/.config/goose/skills/`     |
| Roo Code       | `~/.roo/skills/`              |
| OpenCode       | `~/.config/opencode/skills/`  |
| Codex          | `~/.codex/skills/`            |

> [!TIP]
> Project-scoped installation is also supported. Copy `src/skills/` into `.claude/skills/` (or the equivalent directory for your agent) at the root of your working directory to scope the skills to that project only.

**4. Restart your agent** to load the new agents and skills.

**5. (Optional) Activate the Wolfram Engine license:**

<details>
<summary>🔬 Configure Mathematica / Wolfram Engine license</summary>

The FeynRules-based blueprints (`feynrules-model-validator`, `ufo-generator`) require a Wolfram Engine license. Because the license is tied to the machine identity of the *container* rather than the host, activation must be performed inside the container itself.

1. Register a free Wolfram ID at [wolfram.com/engine/free-license](https://wolfram.com/engine/free-license)

2. Run the activation inside the container:

```bash
mkdir -p ~/.wolfram-container-license
docker run -it --rm \
  -v ~/.wolfram-container-license:/root/.WolframEngine/Licensing \
  git.pku.edu.cn/het-agi/mma-het:latest wolframscript
```

3. Follow the interactive prompts to enter your Wolfram ID and password.

The license file (`mathpass`) is written to `~/.wolfram-container-license/` on the host, which all subsequent FeynRules blueprint runs mount automatically. This step is only needed once.

</details>

## Quickstart

The fastest way to try Collider-Agent is to run a standard-model dilepton invariant mass plot — a classic parton-level check — directly from the command line:

```bash
claude -p "Plot the dilepton invariant mass distribution for parton-level pp -> l+l- process at the 14 TeV LHC in the SM." --dangerously-bypass-permissions
```

This runs the full pipeline non-interactively: MadGraph5 generates the events via [Magnus](https://github.com/rise-agi/magnus), and the agent produces a normalized $m_{\ell\ell}$ histogram in your working directory.

## Usage

### Basic Workflow

1. Prepare a detailed Markdown prompt (for example, `prompt.md`) describing the collider analysis you want to run, including the Lagrangian, collider process, event selection, and parameter scan strategy, much like you would write your own research note or paper draft (see `paper-reproduction/` for examples)

2. Start your agent and provide the prompt:

```bash
claude -p "Execute the analysis following prompt.md"
```

3. The system orchestrates the full pipeline:
   - Parse the Lagrangian and generate a FeynRules model
   - Validate and generate the UFO model
   - Run MadGraph5 simulations with Pythia8 / Delphes
   - Apply analysis cuts with MadAnalysis5
   - Generate the analysis outputs, such as kinematic distribution plots, parameter exclusion regions, and any other results requested in the user prompt

### Example Prompts

The `paper-reproduction/` directory contains example prompts organized by arXiv ID:


| arXiv ID | Topic | Figures |
|----------|-------|---------|
| [hep-ph/9909255](9909255/) | $e^+ e^- \to \mu^+ \mu^- $ affected by KK tower of gravitons| 2 |
| [1308.2209](1308.2209/) | Heavy Neutrinos production at the LHC | 3 |
| [1605.02910](1605.02910/) | Exclusion parameter region from Drell-Yan process at the LHC for a $U(1)'$ model | 1, 10 |
| [1701.05379](1701.05379/) | ALP Effective Field Theory and Collider Signatures | 8 |
| [1811.07920](1811.07920/) | Exclusion parameter region from mono-$\tau$ search at the LHC for the $U_1$ leptoquark model  | 3 |
| [2005.06475](2005.06475/) | Leptoquark production from lepton-Quark collisions at the LHC by using `LUXlep` PDF| 2 |
| [2103.02708](2103.02708/) | $p p \to Z^\prime \to \ell^+ \ell^-$ at the LHC in the SSM and $E_6$ inspired $Z^\prime$ scenario| 4 |
| [2104.05720](2104.05720/) | Searching for Leptoquarks via $\mu^+ \mu^- \to b \bar{b}$ process at Future Muon Colliders | 11, 12 |


## Repository Structure

```
ColliderAgent/
├── src/
│   ├── agents/                        # Sub-agent definitions (Claude Code)
│   │   ├── model-generator.md
│   │   ├── collider-simulator.md
│   │   ├── event-analyzer.md
│   │   └── pheno-analyzer.md
│   └── skills/                        # Agent skill modules (all agents)
│       ├── feynrules-model-generator/
│       ├── feynrules-model-validator/
│       ├── ufo-generator/
│       ├── madgraph-simulator/
│       ├── madanalysis-analyzer/
│       ├── pheno-pipeline-orchestrator/
│       └── magnus/
├── paper-reproduction/                # Example prompts from paper
│   ├── 1308.2209/
│   ├── 1605.02910/
│   └── ...
├── pyproject.toml
└── README.md
```

## Sub-agents

> [!NOTE]
> Sub-agents are currently supported by Claude Code only. Users of other agents can use the skills directly via the agent's built-in skill invocation mechanism.

| Agent                | Description                                       |
| -------------------- | ------------------------------------------------- |
| `model-generator`    | LaTeX → FeynRules → UFO pipeline                  |
| `collider-simulator` | MadGraph5 event generation with Pythia8 / Delphes |
| `event-analyzer`     | MadAnalysis5 cut-flow and histogram analysis      |
| `pheno-analyzer`     | Orchestrates the full phenomenology study         |

## Skills

| Skill                         | Description                                       |
| ----------------------------- | ------------------------------------------------- |
| `feynrules-model-generator`   | Generate `.fr` model files from LaTeX Lagrangians |
| `feynrules-model-validator`   | Validate `.fr` models via Mathematica checks      |
| `ufo-generator`               | Export FeynRules models to UFO format             |
| `madgraph-simulator`          | Run MadGraph5_aMC@NLO event generation            |
| `madanalysis-analyzer`        | Perform cut-flow analysis and produce histograms  |
| `pheno-pipeline-orchestrator` | Coordinate the end-to-end phenomenology pipeline  |
| `magnus`                      | Interface with the Magnus cloud HEP platform      |

## Citation

If you use Collider-Agent in your research, please cite:

```bibtex
@misc{collider-agent,
  author = {Qiu, Shi and Cai, Zeyu and Wei, Jiashen and Li, Zeyu and Yin, Yixuan and Cao, Qing-Hong and Liu, Chang and Luo, Ming-xing and Yuan, Xing-Bo and Zhu, Hua Xing},
  title  = {An End-to-end Architecture for Collider Physics and Beyond},
  year   = {2026},
  howpublished = {\url{https://github.com/HET-AGI/ColliderAgent}},
  note   = {Preprint}
}
```

## Acknowledgments

We thank the developers of [FeynRules](https://arxiv.org/abs/1310.1921), [MadGraph5_aMC@NLO](https://github.com/restrepo/madgraph), [Pythia8](https://pythia.org/), [Delphes](https://github.com/delphes/delphes), and [MadAnalysis5](https://github.com/MadAnalysis/madanalysis5) for their excellent tools that make this work possible.
