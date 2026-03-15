# Paper Reproduction Examples

A curated collection of prompts for reproducing collider phenomenology figures from published high-energy physics papers using Collider-Agent.

Each entry in this directory is a self-contained benchmark: it provides the agent with a LaTeX Lagrangian, model parameters, collider process definition, and analysis instructions — and asks it to reproduce a specific figure from the corresponding paper.

> [!NOTE]
> For a general overview of Collider-Agent, installation instructions, and quickstart examples, see the [root README](../README.md).

## Papers

| arXiv ID | Title | Figures |
|----------|-------|---------|
| [hep-ph/9909255](9909255/) | Warped Phenomenology | 2 |
| [1308.2209](1308.2209/) | New Production Mechanism for Heavy Neutrinos at the LHC | 3 |
| [1605.02910](1605.02910/) | Z', Higgses and Heavy Neutrinos in U(1)' Models: From the LHC to the GUT Scale | 1, 10 |
| [1701.05379](1701.05379/) | ALPs Effective Field Theory and Collider Signatures | 8 |
| [1811.07920](1811.07920/) | The Mono-Tau Menace: From B Decays to High-pT Tails | 3 |
| [2005.06475](2005.06475/) | Lepton-Quark Collisions at the Large Hadron Collider | 2 |
| [2103.02708](2103.02708/) | Search for Resonant and Nonresonant New Phenomena in High-Mass Dilepton Final States at √s = 13 TeV | 4 |
| [2104.05720](2104.05720/) | Searching for Leptoquarks at Future Muon Colliders | 11, 12 |

## How to Use

**1. Choose a paper** from the table above and open its directory.

**2. Read the prompt file** — use `prompt_figure_N.md` (not the `_with_comments` variant, which contains hints and is intended for developers only).

**3. Start your agent** and paste the prompt:

```bash
claude
```

**4. The agent runs the full pipeline** — model generation, simulation, analysis, and plotting — and outputs the reproduced figure in your working directory.

> [!TIP]
> Run prompts from a clean working directory to avoid mixing outputs from different runs. Each paper directory also has a `README.md` with a difficulty ranking when multiple figures are available — start with the simpler one.

## Prompt Format

Every prompt follows a standard four-section structure:

| Section | Contents |
|---------|----------|
| **1. Target** | The figure to reproduce and the physical quantity to plot |
| **2. Model** | BSM Lagrangian in LaTeX, particle content, quantum numbers, and parameter definitions |
| **3. Collider Process** | Process string (e.g. `pp > l+ l-`), beam energy, PDF set, and generation-level cuts |
| **4. Numerical Setup / Analysis** | Parameter scan values, event counts, analysis cuts, and instructions for producing the final plot |

The `_with_comments` version of each prompt annotates the same sections with implementation notes and known pitfalls. Use these as a reference when debugging a reproduction or writing new prompts.

## Directory Structure

```
paper-reproduction/
├── <arXiv-ID>/
│   ├── README.md                        # Difficulty ranking and file index
│   ├── paper/                           # PDF and LaTeX source of the paper
│   ├── prompt_figure_N.md               # Clean prompt — give this to the agent
│   └── prompt_figure_N_with_comments.md # Annotated version — for developers only
└── README.md                            # This file
```

## Adding New Examples

To contribute a new paper reproduction:

1. Create a directory named after the arXiv ID (e.g. `2312.01234/`)
2. Add a `prompt_figure_N.md` following the four-section structure above
3. Optionally add a `prompt_figure_N_with_comments.md` with implementation notes
4. Add a `README.md` with difficulty ranking and file index
5. Place the paper PDF in `paper/`
