---
name: micromegas-calculator
description: Compute dark matter observables (relic density, direct detection, indirect detection) via micrOmegas on the Magnus cloud. Triggers when the user wants to calculate Ωh², DM-nucleon cross sections (SI/SD), annihilation ⟨σv⟩ into SM final states, or indirect-detection γ/ν/e⁺/e⁻ spectra. Consumes a CalcHEP model (from the calchep-generator skill) plus a user-supplied main.c.
---

# micrOmegas Calculator

## Overview

This skill runs micrOmegas for dark matter phenomenology using two Magnus blueprints in sequence:

1. **`micromegas-compile`** — drops the CalcHEP model into a fresh micrOmegas project, installs the user-supplied `main.c`, and compiles the executable. The symbolic CalcHEP engine is pre-built in the container, so this step only compiles user code and auto-generated matrix elements.
2. **`micromegas-calc`** — runs the compiled `./main` once, captures its stdout and the structured `results.json` it writes, and uploads any additional output files.

Both steps execute on the Magnus cloud (see magnus skill).

## Prerequisites

### CalcHEP model with Z₂-odd marking

micrOmegas identifies the dark matter candidate via the `aux` column of `prtcls1.mdl`: candidate particles must be marked `odd`. This is **FeynRules territory**, not a micrOmegas concern — either set it at the `.fr` level before calling `generate-calchep`, or post-process the CalcHEP output by hand before `micromegas-compile`. Without this mark, `sortOddParticles` returns a non-zero error code and every downstream function refuses to run.

### main.c protocol

The user-supplied `main.c` is responsible for:

1. Setting parameters (either by `assignValW` / `assignValC` calls, or by calling `slhaRead` on the SLHA file that `micromegas-calc` passes as `argv[1]`)
2. Calling whichever subset of micrOmegas API it needs (`sortOddParticles`, `darkOmega`, `nucleonAmplitudes`, `calcSpectrum`, …)
3. **Writing structured results to `results.json`** in the working directory. The blueprint parses this file and surfaces it in `MAGNUS_RESULT`.

A minimal skeleton:

```c
#include "micromegas.h"
#include "micromegas_aux.h"
#include <stdio.h>

int main(int argc, char** argv) {
    if (argc > 1) slhaRead(argv[1], 0);

    if (sortOddParticles(NULL)) { return 1; }

    double Xf, Omega;
    Omega = darkOmega(&Xf, 1, 1e-4, NULL);

    FILE* out = fopen("results.json", "w");
    fprintf(out, "{\"cdm\": \"%s\", \"omega_h2\": %.6e, \"xf\": %.3f}\n",
            CDM1, Omega, Xf);
    fclose(out);
    return 0;
}
```

Anything not written to `results.json` is still preserved in the uploaded output directory, and stdout is tailed into `MAGNUS_RESULT` for debugging.

## Output Paths

All paths are **relative to the working directory**.

| Output | Path pattern | Example |
|--------|-------------|---------|
| Compiled project | `dm/<project_label>/` | `dm/singlet_scalar/` |
| Run output | `dm/<project_label>/<run_label>/` | `dm/singlet_scalar/mS_700GeV/` |
| Structured result | `dm/<project_label>/<run_label>/results.json` | |

**Naming conventions**:
- `<project_label>`: short model name, e.g. `singlet_scalar`, `IDM`
- `<run_label>`: benchmark-point tag, e.g. `mS_700GeV`, `tanb_10`, `point1`

## Workflow

### Step 1: Compile the project

```bash
magnus run micromegas-compile -- \
  --calchep path/to/MyModel_CH \
  --main path/to/main.c \
  --output dm/my_model \
  --project my_model
```

**Parameters**:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--calchep` | Yes | Path to CalcHEP model directory (from `generate-calchep`). Must contain `vars1.mdl`, `func1.mdl`, `prtcls1.mdl`, `lgrng1.mdl` at top level or one subdirectory down. |
| `--main` | Yes | Path to the user's `main.c` |
| `--output` | Yes | Where to download the compiled project directory |
| `--project` | No | micrOmegas project name (used by `newProject`); defaults to `dm_project` |

The CalcHEP directory and `main.c` are uploaded via FileSecret. On success, the compiled project — including the `./main` binary and the auto-generated matrix-element code — is downloaded to `--output`.

**WARNING**: If `--output` points to an existing directory it will be **deleted and replaced**.

**Result** (`magnus job result <job-id>`):
- `success` (bool)
- `project_dir` (str): path to the compiled project
- `main_binary` (str): path to `./main` inside the container (informational)
- `make_log_tail` (str, only on failure): last 3000 chars of `make` output

### Step 2: Run the calculation

```bash
magnus run micromegas-calc -- \
  --project dm/my_model \
  --output dm/my_model/run1 \
  --slha path/to/params.slha
```

**Parameters**:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--project` | Yes | Path to the compiled project directory (Step 1's output) |
| `--output` | Yes | Where to download the run output (includes `results.json`) |
| `--slha` | No | SLHA parameter card (only if `main.c` calls `slhaRead(argv[1], 0)`) |
| `--extra_args` | No | Extra positional arguments appended to `./main` (space-separated) |

**Result** (`magnus job result <job-id>`):
- `success` (bool)
- `output_dir` (str): path to uploaded run output
- `results` (object, if `results.json` present): the parsed JSON written by `main.c`
- `stdout_tail` (str): last 4000 chars of `./main` stdout
- `stderr_tail` (str, on failure only)

### Parameter scans: compile once, run many

Because the compiled project is returned as a directory and consumed by `--project`, a typical scan looks like:

```bash
# Compile once
magnus run micromegas-compile -- \
  --calchep models/Singlet_CH --main src/main.c \
  --output dm/singlet --project singlet

# Scan points by feeding different SLHA cards (or --extra_args if main.c parses argv)
for m in 200 400 600 800 1000 1200; do
  render_slha $m > params_$m.slha
  magnus run micromegas-calc -- \
    --project dm/singlet \
    --slha params_$m.slha \
    --output dm/singlet/mS_${m}GeV
done
```

Every run reuses the single compiled binary — the expensive symbolic-amplitude step is paid only once.

## Examples

### Relic density only

`main.c`:

```c
#include "micromegas.h"
#include "micromegas_aux.h"
#include <stdio.h>

int main(int argc, char** argv) {
    if (argc > 1) slhaRead(argv[1], 0);
    if (sortOddParticles(NULL)) return 1;
    double Xf, Omega = darkOmega(&Xf, 1, 1e-4, NULL);
    FILE* out = fopen("results.json", "w");
    fprintf(out, "{\"cdm\":\"%s\",\"omega_h2\":%.6e,\"xf\":%.3f}\n",
            CDM1, Omega, Xf);
    fclose(out);
    return 0;
}
```

### Relic + direct detection (SI/SD on p/n)

```c
#include "micromegas.h"
#include "micromegas_aux.h"
#include <stdio.h>

int main(int argc, char** argv) {
    if (argc > 1) slhaRead(argv[1], 0);
    if (sortOddParticles(NULL)) return 1;

    double Xf, Omega = darkOmega(&Xf, 1, 1e-4, NULL);

    double pA0[2], pA5[2], nA0[2], nA5[2];
    nucleonAmplitudes(CDM1, pA0, pA5, nA0, nA5);

    double mN = 0.939, Mdm = MassCDM(CDM1);
    double mu = Mdm * mN / (Mdm + mN);
    double pref = 4.0 / M_PI * mu * mu * 2.568e9;   // GeV^-2 → pb

    FILE* out = fopen("results.json", "w");
    fprintf(out,
        "{\"cdm\":\"%s\",\"mdm\":%.3f,\"omega_h2\":%.6e,"
        "\"sigma_SI_p\":%.6e,\"sigma_SI_n\":%.6e,"
        "\"sigma_SD_p\":%.6e,\"sigma_SD_n\":%.6e}\n",
        CDM1, Mdm, Omega,
        pref * pA0[0]*pA0[0], pref * nA0[0]*nA0[0],
        3.0 * pref * pA5[0]*pA5[0], 3.0 * pref * nA5[0]*nA5[0]);
    fclose(out);
    return 0;
}
```

## Key conventions

- **Z₂-odd flag is a model-authoring concern**: fix it in the `.fr` file, not here
- **results.json is a contract**: `main.c` writes, the blueprint reads; keep the JSON flat and typed (floats, strings, arrays of either) for easy downstream plotting
- **Compile-once scan-many**: reuse `--project` across parameter points, never re-call `micromegas-compile` per point unless the model itself changes
- **micrOmegas prints heavily to stdout**: the last 4000 chars are captured in `stdout_tail`, but authoritative results should always go through `results.json`
