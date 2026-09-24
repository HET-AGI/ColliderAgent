# micrOmegas — worked main.c examples

Compile once with `micromegas-compile`, then run each parameter point with `micromegas-calc`. Every program writes `results.json` (the blueprint parses it) and exits non-zero on failure.


### Relic density only

`main.c`:

```c
#include "micromegas.h"
#include "micromegas_aux.h"
#include <stdio.h>

int main(int argc, char** argv) {
    if (argc > 1 && slhaRead(argv[1], 0)) return 2;
    if (sortOddParticles(NULL)) return 1;
    if (!CDM[1]) return 3;
    double Xf, Omega = darkOmega(&Xf, 1, 1e-4, NULL);
    FILE* out = fopen("results.json", "w");
    if (!out) return 4;
    fprintf(out,
            "{\"cdm\":\"%s\",\"cdm_mass_GeV\":%.6e,\"omega_h2\":%.6e,\"xf\":%.3f}\n",
            CDM[1], McdmN[1], Omega, Xf);
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
    if (argc > 1 && slhaRead(argv[1], 0)) return 2;
    if (sortOddParticles(NULL)) return 1;
    if (!CDM[1]) return 3;

    double Xf, Omega = darkOmega(&Xf, 1, 1e-4, NULL);

    double pA0[2], pA5[2], nA0[2], nA5[2];
    nucleonAmplitudes(CDM[1], pA0, pA5, nA0, nA5);

    double mN = 0.939, Mdm = McdmN[1];
    double mu = Mdm * mN / (Mdm + mN);
    double pref = 4.0 / M_PI * mu * mu * 2.568e9;   // GeV^-2 → pb

    FILE* out = fopen("results.json", "w");
    if (!out) return 4;
    fprintf(out,
        "{\"cdm\":\"%s\",\"mdm\":%.3f,\"omega_h2\":%.6e,"
        "\"sigma_SI_p\":%.6e,\"sigma_SI_n\":%.6e,"
        "\"sigma_SD_p\":%.6e,\"sigma_SD_n\":%.6e}\n",
        CDM[1], Mdm, Omega,
        pref * pA0[0]*pA0[0], pref * nA0[0]*nA0[0],
        3.0 * pref * pA5[0]*pA5[0], 3.0 * pref * nA5[0]*nA5[0]);
    fclose(out);
    return 0;
}
```

## Timing expectations


Empirically on the Magnus `rise-agi/micromegas:latest` container at blueprint-default resources (compile: 8 CPU / 8 GB; calc: 4 CPU / 4 GB):

| Model | `micromegas-compile` | `micromegas-calc` (per point) | Dominant cost in calc |
|-------|---------------------|------------------------------|-----------------------|
| SingletDM (1 scalar) | ~30 s | ~60 s | dynamic compile of 2–3 annihilation channels |
| RDM (2 fermions + leptoquark mediator, coannihilation) | ~45 s | ~2 min | ~χ0 ~χ0 → LQ LQ̃, plus ~χ0 ~χ1 coannihilation channels |
| IDM (H⁰ + A⁰ + H±, full coannihilation) | ~1 min | **10+ min** | ~30 channels across all scalar pairs, first calc is slowest |

Calc time is dominated by micrOmegas's runtime symbolic compilation of each required subprocess into a `.so` library via CalcHEP. Within one `./main` invocation those `.so` files are cached, but the blueprint re-uploads the pristine compiled project for each scan point, so every `micromegas-calc` run pays the full subprocess-compile cost. The compile-once / scan-many win is in `micromegas-compile` itself — `make main=main.c` plus CalcHEP library linking happens exactly once, not per point.
