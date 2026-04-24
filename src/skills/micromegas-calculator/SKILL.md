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

micrOmegas identifies dark-matter candidates by **the `~` prefix on particle names** in the `P` column of `prtcls1.mdl` — there is no separate Z₂ quantum number. Every Z₂-odd particle (the DM candidate plus any coannihilation partners) must appear as `~<name>` in that column.

Concrete verification step after `generate-calchep`:

```bash
grep -E '\|~[A-Za-z]' path/to/MyModel_CH/prtcls1.mdl
```

should list every intended Z₂-odd field. Reference examples from shipped micrOmegas projects: SingletDM → `~x1`; IDM → `~H3 ~H+ ~X`; RDM → `~chi0 ~chi1`.

If no `~`-prefixed particles appear, the `.fr` source is wrong — fix it at authoring time, not by hand-editing `.mdl` files (the hand-edit gets lost the next time `generate-calchep` runs). Without the convention, **`sortOddParticles` will fail, `darkOmega` returns `NaN`, and every cross section reads zero — yet the blueprint still returns with exit code 0**. The blueprint detects this failure pattern via stdout markers (`Can not compile`, `Omega=NAN`, `Omega=nan`) and surfaces it as `success: false` in `MAGNUS_RESULT`; the caller should still check `success` before consuming numbers.

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

- **Z₂-odd flag is a model-authoring concern**: fix it in the `.fr` file (so generated `prtcls1.mdl` carries `~`-prefixed names), not by hand-editing generated `.mdl` files
- **results.json is a contract**: `main.c` writes, the blueprint reads; keep the JSON flat and typed (floats, strings, arrays of either) for easy downstream plotting
- **stdout_tail is the fallback physics channel**: if `main.c` does not write `results.json`, the blueprint still surfaces the last 4000 chars of stdout under `stdout_tail` — human-readable, but brittle to parse programmatically. Prefer `results.json` whenever a downstream agent consumes the numbers
- **Compile-once scan-many**: reuse `--project` across parameter points, never re-call `micromegas-compile` per point unless the model itself changes
- **Always check `success` before consuming results**: the blueprint returns `success: false` when `./main` exits non-zero **or** when stdout matches the silent-failure markers `Can not compile` / `Omega=NAN` / `Omega=nan` (needed because micrOmegas sometimes prints NaN with exit 0)

## Timing expectations

Empirically on the Magnus `rise-agi/micromegas:latest` container at blueprint-default resources (compile: 8 CPU / 8 GB; calc: 4 CPU / 4 GB):

| Model | `micromegas-compile` | `micromegas-calc` (per point) | Dominant cost in calc |
|-------|---------------------|------------------------------|-----------------------|
| SingletDM (1 scalar) | ~30 s | ~60 s | dynamic compile of 2–3 annihilation channels |
| RDM (2 fermions + leptoquark mediator, coannihilation) | ~45 s | ~2 min | ~χ0 ~χ0 → LQ LQ̃, plus ~χ0 ~χ1 coannihilation channels |
| IDM (H⁰ + A⁰ + H±, full coannihilation) | ~1 min | **10+ min** | ~30 channels across all scalar pairs, first calc is slowest |

Calc time is dominated by micrOmegas's runtime symbolic compilation of each required subprocess into a `.so` library via CalcHEP. Within one `./main` invocation those `.so` files are cached, but the blueprint re-uploads the pristine compiled project for each scan point, so every `micromegas-calc` run pays the full subprocess-compile cost. The compile-once / scan-many win is in `micromegas-compile` itself — `make main=main.c` plus CalcHEP library linking happens exactly once, not per point.
