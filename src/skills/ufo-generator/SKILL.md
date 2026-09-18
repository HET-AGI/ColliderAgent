---
name: ufo-generator
description: Export a validated FeynRules .fr model to a UFO directory for MadGraph5 (also usable by Herwig and Sherpa) on the Magnus cloud, then read particles.py and parameters.py to get the MG5 particle names, PDG codes, and SLHA blocks the simulation stage needs. Use after a .fr file passes validation.
---

# UFO Generator

```bash
magnus run generate-ufo -- --model models/MyModel.fr --lagrangian LNP --output models/MyModel_UFO
```

(Execution mechanics, upload/download, recovery: magnus skill.)

| Parameter | Required | Meaning |
|---|---|---|
| `--model` | yes | the validated `.fr` file (uploaded) |
| `--lagrangian` | yes | the Lagrangian symbol in the file |
| `--output` | yes | where the UFO directory is downloaded |
| `--restriction` | no | a `.rst` restriction file (uploaded) |

A file without `M$GaugeGroups` is exported as a BSM extension: the blueprint loads SM.fr plus `Massless.rst` and `DiagonalCKM.rst` first. Result: `success`, `ufo_path`, and any FeynRules warnings; review warnings before using the model.

## After export, repair and check the directory

Run the fixer that ships with this skill before anything reads the model:

```bash
python3 <skill-dir>/scripts/ufo_fix.py models/MyModel_UFO          # --check to only report
```

It rewrites the Python-2 `raise UFOError, "msg"` that FeynRules 2.3.49 always emits, removes `__pycache__`, byte-compiles every file, and reports defects that a script cannot fix (unevaluated Mathematica such as `CreateObjectParticleName`, `FSD[`, `Slot(`; empty `lorentz.py`/`vertices.py`). Exit 0 means the import test can be submitted; exit 1 means the `.fr` must change first, and the report names the line. Four independent runs re-discovered the `raise` defect by hand before this script existed; do not hand-edit what it fixes.

## After export, read the model

MG5 identifies particles by the `name` field in `particles.py`, not by the `.fr` class name, and parameters by SLHA block and code in `parameters.py`. Extract, for every BSM object:

- `particles.py` → `name`, `antiname`, `pdg_code`, spin, charge, colour (for `generate` lines and `set param_card MASS <pdg>`);
- `parameters.py` → `name`, `lhablock`, `lhacode`, `value` for external parameters (for `set param_card <BLOCK> <code> <value>`);
- `vertices.py` → the vertices containing at least one BSM particle (the production and decay channels the model offers).

These tables go into the step 1 sidecar so the simulation stage does not reopen the files. Then run the MadGraph5 import test (feynrules-model-validator skill) before the model leaves this stage.

Directory layout, field-by-field reading guide, and the mapping to `set param_card` commands: `references/ufo_format.md`.
