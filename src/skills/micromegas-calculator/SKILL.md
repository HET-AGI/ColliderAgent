---
name: micromegas-calculator
description: Compute dark-matter observables with micrOmegas on the Magnus cloud — relic density Ωh², spin-independent and spin-dependent DM–nucleon cross sections, annihilation ⟨σv⟩, indirect-detection spectra — from a CalcHEP model plus a user-supplied main.c. Use when a task asks for these observables or a scan over them.
---

# micrOmegas Calculator

Two blueprints (execution mechanics, upload/download, recovery: magnus skill):

1. `micromegas-compile` — drops the CalcHEP model into a fresh micrOmegas project, installs your `main.c`, compiles `./main`. The symbolic engine is prebuilt in the container; only your code and the generated matrix elements compile here.
2. `micromegas-calc` — runs `./main` once in the compiled project, parses the `results.json` it wrote, uploads the run directory.

## Paths (relative to the working directory)

| Output | Path | Example |
|---|---|---|
| Compiled project | `dm/<project_label>/` | `dm/singlet_scalar/` |
| Run output | `dm/<project_label>/<run_label>/` | `dm/singlet_scalar/mS_700GeV/` |
| Structured result | `dm/<project_label>/<run_label>/results.json` | |

## Prerequisites

- A CalcHEP model whose `prtcls1.mdl` lists every Z₂-odd particle with a leading `~` (calchep-generator skill explains why and how to check). Without it every observable is zero or NaN with no error.
- A `main.c` following the protocol below.

## main.c protocol

`main.c` sets the parameters (`assignValW`/`assignValC`, or `slhaRead(argv[1], 0)` on the SLHA card the calc blueprint passes as `argv[1]`), calls the micrOmegas API it needs (`sortOddParticles`, `darkOmega`, `nucleonAmplitudes`, `calcSpectrum`, …), and writes flat, typed JSON to `results.json` in the working directory. Rules that come from the 6.3.0 API and the container:

- `#include "micromegas.h"` and `"micromegas_aux.h"` with bare names: compile exports `CPATH=<MICROMEGAS_ROOT>/include`, so the same file also compiles locally.
- Read the DM name from `CDM[1]` (a `char**`); the legacy `CDM1`/`CDM2` globals are declared but no longer filled. Treat a null `CDM[1]` after `sortOddParticles` as "no odd particle found" and exit non-zero.
- `assignValW("Name", v)` returns non-zero for an unknown name and leaves the default in place; use the exact names from `vars1.mdl` and check the return value, otherwise a scan silently runs at defaults.
- Anything not in `results.json` is still preserved in the uploaded run directory; the blueprint also returns the last 4000 characters of stdout, which is a fallback, not a parsing target.
- For anything beyond a smoke test, start from the closest micrOmegas reference `main.c` for that model class and trim it; some models need extra setup before heavy calls.

Minimal skeleton and two complete programs (relic only; relic + SI/SD): `references/examples.md`.

## Step 1: compile

```bash
magnus run micromegas-compile -- \
  --calchep models/MyModel_CH --main src/main.c \
  --output dm/my_model --project my_model
```

| Parameter | Required | Meaning |
|---|---|---|
| `--calchep` | yes | CalcHEP directory (uploaded); `vars1/func1/prtcls1/lgrng1.mdl` at the top level or one directory down |
| `--main` | yes | your `main.c` (uploaded) |
| `--output` | yes | where the compiled project (with `./main` and generated matrix-element code) is downloaded |
| `--project` | no | micrOmegas project name (default `dm_project`) |

Result: `success`, `project_dir`, `main_binary`, and on failure `make_log_tail` (last 3000 characters of `make`).

## Step 2: run points

```bash
magnus run micromegas-calc -- --project dm/my_model --output dm/my_model/run1 --slha params.slha
```

| Parameter | Required | Meaning |
|---|---|---|
| `--project` | yes | the compiled project from step 1 (uploaded) |
| `--output` | yes | download path for the run directory (contains `results.json`) |
| `--slha` | no | SLHA card passed as `argv[1]` (only when `main.c` calls `slhaRead`) |
| `--extra_args` | no | extra positional arguments appended to `./main` |

Result: `success`, `output_dir`, `results` (the parsed JSON), `stdout_tail`, and `stderr_tail` on failure. `success` is false when `./main` exits non-zero **or** when stdout matches `Can not compile`, `Omega=NAN`, or `Omega=nan`; check it before reading `results`.

Compile once, run many: a scan is one compile job followed by one calc job per point (different SLHA cards or `--extra_args`), which can be submitted in parallel; the expensive symbolic step is paid once. Recompile only when the model or `main.c` changes.

Timing expectations per model class (compile ~30 s to 1 min; calc from ~1 min for a scalar singlet to 10+ min for a full inert doublet with co-annihilation) are tabulated in `references/examples.md`.
