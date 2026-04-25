---
name: calchep-generator
description: Generate CalcHEP model directories from FeynRules .fr files via Magnus cloud. Triggers when the user has a validated .fr model and needs a CalcHEP model for micrOmegas or CalcHEP.
---

# CalcHEP Generator

## Overview

This skill generates CalcHEP model directories from FeynRules `.fr` files using remote Mathematica execution via the Magnus cloud platform. CalcHEP models are the standard interchange format between model-building tools (FeynRules) and dark matter calculation packages (micrOmegas, CalcHEP).

## Workflow

### Step 1: Prepare the .fr File

Ensure the `.fr` file is validated (via feynrules-model-validator skill) and saved to disk. Know the Lagrangian symbol name (e.g., `LSnew`, `LBSM`).

### Step 2: Generate the CalcHEP Model

Execute the `generate-calchep` blueprint using `magnus run` (see magnus skill):

```bash
magnus run generate-calchep -- --model path/to/model.fr --lagrangian LSnew --output path/to/MyModel_CH
```

**Parameters**:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--model` | Yes | Path to the `.fr` model file |
| `--lagrangian` | Yes | Lagrangian symbol from the `.fr` file |
| `--output` | Yes | Output path for the generated CalcHEP directory |
| `--restriction` | No | Path to `.rst` restriction file |

The `.fr` file (and `.rst` if provided) is automatically uploaded via the FileSecret mechanism. On success, the CalcHEP directory is automatically downloaded to `--output`.

**WARNING**: If `--output` points to an existing directory, it will be **deleted and replaced** by the download.

Model type is auto-detected:
- With `M$GaugeGroups`: loaded directly as standalone model
- Without `M$GaugeGroups`: BSM extension — SM.fr and SM restrictions (Massless.rst, DiagonalCKM.rst) are loaded automatically

### Step 3: Verify CalcHEP Output

Check the result JSON (`magnus job result <job-id>`):
- `success` (bool): Whether generation succeeded
- `calchep_path` (str): Path to the downloaded CalcHEP directory

### Step 4: Read CalcHEP Output Files

After successful generation, the CalcHEP directory contains `.mdl` files used by CalcHEP and micrOmegas:

- `vars1.mdl` — independent variables and parameters
- `func1.mdl` — dependent parameters (functions of independent variables)
- `prtcls1.mdl` — particle definitions (name, spin, mass, width, color, charge)
- `lgrng1.mdl` — interaction vertices (Lagrangian terms)
- `extlib1.mdl` — external library references (if any)

These files are plain text in CalcHEP's proprietary format — they are **not** Python files like UFO.

## Z₂-Odd Convention (for micrOmegas consumption)

**If this model will be passed to micrOmegas for dark-matter calculations**, every Z₂-odd particle (the DM candidate plus any coannihilation partners) **must appear with a leading `~` in the particle-name (`P`) column of `prtcls1.mdl`**. micrOmegas identifies the DM sector purely by this naming convention — it does not read a separate Z₂ quantum number.

Examples from shipped micrOmegas models:

| Model | Particle-name column entry | Role |
|-------|---------------------------|------|
| SingletDM | `~x1` | scalar singlet DM |
| IDM | `~H3`, `~H+`, `~X` | inert doublet components (CP-odd, charged, second Higgs) |
| RDM | `~chi0`, `~chi1` | fermion DM + fermion coannihilator |

**After `generate-calchep` succeeds, verify** `prtcls1.mdl` lists `~`-prefixed names for every particle that should be Z₂-odd. Hand-editing `prtcls1.mdl` after the fact is not a fix: the edit is lost the next time `generate-calchep` runs.

Current repo limitation: this blueprint calls plain `WriteCHOutput[...]` and does **not** inject a separate odd-particle list. So the only reliable contract is the generated CalcHEP output itself. A FeynRules-side recipe that is verified to work in the current pipeline is to place the tilde directly in `ParticleName` (and `AntiParticleName` for non-self-conjugate fields). Still, treat the generated `prtcls1.mdl` as the final authority, because export behavior is model-dependent. Likewise, do **not** assume `QuantumNumbers -> {Z2 -> -1}` alone is sufficient: custom quantum numbers require explicit model-level declarations, and even then the CalcHEP exporter may not map them to micrOmegas odd-particle names.

Practical rule: iterate on the `.fr`, rerun `generate-calchep`, and re-check `prtcls1.mdl` until the exported names are right. If you need a starting point, copy the naming strategy from a known-good dark-matter FeynRules model rather than inventing a new convention.

Without this convention, `sortOddParticles` in the downstream micrOmegas run will fail to locate a DM candidate and every dark-matter observable will silently be zero or `NaN`.
