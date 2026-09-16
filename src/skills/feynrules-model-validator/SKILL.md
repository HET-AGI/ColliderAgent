---
name: feynrules-model-validator
description: Validate a FeynRules model at two points — Mathematica consistency checks of the .fr file (hermiticity, diagonal mass and quadratic terms, kinetic normalisation) on the Magnus cloud, and a MadGraph5 import test of the generated UFO directory with fixes for known FeynRules export bugs. Use after writing or editing a .fr file and again after UFO generation.
---

# FeynRules Model Validator

Two checks, two blueprints (execution mechanics, upload/download, recovery: magnus skill).

## 1. Consistency checks on the `.fr` file

```bash
magnus run validate-feynrules -- --model models/MyModel.fr --lagrangian LNP
```

| Parameter | Required | Meaning |
|---|---|---|
| `--model` | yes | the `.fr` file (uploaded) |
| `--lagrangian` | yes | the exact Lagrangian symbol defined in the file |

The blueprint loads the SM first when the file has no `M$GaugeGroups` (a BSM extension) and loads a standalone model directly otherwise. It runs four checks in Feynman and in unitary gauge:

| Result field | Meaning |
|---|---|
| `success` | true iff all four **unitary-gauge** checks pass |
| `verdict` | human-readable explanation (Goldstone mixing, field mixing, …) — read this first when `success` is false |
| `unitary_gauge.{hermiticity, diagonal_quadratic_terms, diagonal_mass_terms, kinetic_term_normalisation}` | per-check `passed` plus offending terms |
| `feynman_gauge.*` | informational; failures there are expected for models with spontaneous symmetry breaking |
| `model_loading` | whether the file parsed at all |

Fix the `.fr` from the verdict and re-run until `success` is true. What each check tests and how to read failures: `references/validation_checks.md`.

## 2. MadGraph5 import test on the UFO directory

```bash
magnus run madgraph-compile -- --ufo models/MyModel_UFO
```

Without `--process`, `madgraph-compile` only imports the model. Result: `success`, `stdout`, `stderr` (last 4000 characters each), `return_code`. On failure look for `UFOError` (Python error inside the UFO), `with error:` (MG5 import error), or `interrupted in sub-command` with `error`.

Import failures usually come from FeynRules 2.3.49 code generation, so fix the UFO files directly rather than the `.fr`:

| File | Defect | Fix |
|---|---|---|
| `object_library.py` | Python 2 `raise UFOError, "msg"` | `raise UFOError("msg")` |
| `coupling_orders.py` | leaked Mathematica such as `perturbative_expansion = {{NP, 2}, …}[[3,2]]` | delete the expression or replace with the intended integer |
| `couplings.py` | wrong order dictionaries (`order = {'1': 1}` for a dimension-6 operator) | `order = {'NP': 2}` (or the correct QCD/QED count) |

Re-test after each fix. Give up on direct UFO fixes after 5 attempts and return to the `.fr` (revalidate, regenerate, re-test); the model-generator agent stops the whole loop after 10 import attempts so a structural defect is reported instead of hidden.

Every model that later fails at `madgraph-compile` with a real process most often failed one of these two checks silently; run both before handing the model on.
