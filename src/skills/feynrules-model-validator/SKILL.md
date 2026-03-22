---
name: feynrules-model-validator
description: Validate FeynRules models for correctness. Two capabilities: (1) Mathematica-based physical consistency checks on .fr files (Hermiticity, diagonal mass/quadratic terms, kinetic term normalization), (2) MadGraph5 import test on generated UFO directories to catch Python syntax errors and structural issues.
---

# FeynRules Validator

## Overview

This skill validates FeynRules models at two stages:

1. **Physical consistency checks** (on `.fr` files) — runs four standard checks in both Feynman and Unitary gauge (8 checks total) using remote Mathematica execution via Magnus cloud. Use this between writing a `.fr` model and generating a UFO model.
2. **MadGraph import test** (on UFO directories) — verifies that MadGraph5 can successfully import the generated UFO model. Use this after UFO generation to catch Python syntax errors, corrupted code, and structural issues that Mathematica validation does not detect.

## Workflow

Choose the appropriate workflow based on the task:
- **To validate a `.fr` file** → follow "Physical Consistency Checks" below
- **To test a UFO import** → follow "MadGraph Import Test" below

---

## Physical Consistency Checks

### Step 1: Prepare the Model

Ensure the `.fr` file is complete and saved to disk. Know the exact Lagrangian symbol name (e.g., `LSnew`, `Lag`, `LBSM`).

### Step 2: Run Validation

Execute the `validate-feynrules` blueprint using `magnus run` (see magnus skill):

```bash
magnus run validate-feynrules -- --model path/to/model.fr --lagrangian LSnew
```

**Parameters**:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--model` | Yes | Path to the `.fr` model file |
| `--lagrangian` | Yes | Exact Lagrangian variable name defined in the `.fr` file |

The `.fr` file is automatically uploaded via the FileSecret mechanism.

### Step 3: Interpret Results

The blueprint returns a JSON result (check with `magnus job result <job-id>`) containing:

- **`success`** (bool): `True` iff all 4 Unitary gauge checks pass. Feynman gauge results are informational only.
- **`verdict`** (str): Intelligent human-readable summary explaining the outcome — covers Goldstone mixing, field mixing, etc.
- **`feynman_gauge`** / **`unitary_gauge`**: Per-gauge results with 4 checks each:
  - `hermiticity`
  - `diagonal_quadratic_terms`
  - `diagonal_mass_terms`
  - `kinetic_term_normalisation`
- **`model_loading`**: Whether the model loaded successfully

### Step 4: Fix and Re-validate

If validation fails:
1. Read the `verdict` field for guidance on what to fix
2. Edit the `.fr` file to correct the issues
3. Re-run validation

## Model Type Auto-Detection

The validator auto-detects whether a model is:
- **Standalone**: Contains `M$GaugeGroups` — loaded directly
- **BSM extension**: No `M$GaugeGroups` — the built-in SM.fr is loaded first automatically

## Success Criteria

- **Success = True** when all 4 Unitary gauge checks pass
- Feynman gauge failures are **expected** for models with spontaneous symmetry breaking (Goldstone boson artifacts)
- See [references/validation_checks.md](references/validation_checks.md) for detailed check descriptions and pass criteria

## Reference Documentation

- See [references/validation_checks.md](references/validation_checks.md) for detailed explanation of each check, pass criteria, and gauge-specific behavior

---

## MadGraph Import Test

### Overview

After UFO generation, verify that MadGraph5 can successfully import the model. This catches issues that Mathematica validation cannot detect — Python syntax errors, corrupted Mathematica code in UFO files, and structural problems caused by FeynRules code generation bugs.

### Step 1: Run Import Test

```bash
magnus run madgraph-import-test -- --ufo path/to/MyModel_UFO
```

**Parameters**:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--ufo` | Yes | Path to the UFO model directory |

The UFO directory is automatically uploaded via the FileSecret mechanism.

### Step 2: Interpret Results

The blueprint returns a JSON result containing:

- **`success`** (bool): `True` if MadGraph imported the model without errors
- **`stdout`** (str): MadGraph output (last 4000 chars)
- **`stderr`** (str): Error output (last 4000 chars)
- **`return_code`** (int): MadGraph process exit code

### Step 3: Error Detection

Import failure is determined by `success: false`. When this occurs, check `stdout`/`stderr` for these markers:

- **`UFOError`** — Python error in UFO files (e.g., syntax errors, import failures)
- **`with error:`** — MG5 error during model import
- **`interrupted in sub-command`** combined with **`error`** — subprocess failure during import

### Step 4: Fix and Re-test

If import fails, fix the UFO files directly (not the `.fr` file), because the errors typically originate from FeynRules code generation bugs:

**Common UFO fixes** (known FeynRules 2.3.49 bugs):
1. **`object_library.py`**: Python 2 `raise` syntax — `raise UFOError, "msg"` → `raise UFOError("msg")`
2. **`coupling_orders.py`**: Corrupted Mathematica code — `perturbative_expansion = {{NP, 2}, ...}[[3,2]]` → remove or replace with valid Python
3. **`couplings.py`**: Wrong coupling orders — e.g., `order = {'1':1}` → `order = {'NP':2}` for dimension-6 operators

After fixing, re-run the import test to verify. **Maximum 5 direct UFO fix attempts** — if still failing after 5 attempts, stop and report failure to the caller with diagnostics.
