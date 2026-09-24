# Example FeynRules models

Validated `.fr` files to start from when the task's model resembles one of them. Copy the closest example,
rename it, and edit; run `scripts/fr_lint.py` before validating.

| File | Kind | What it shows |
|---|---|---|
| `Wprime.fr` | BSM extension | a new charged vector with chiral couplings to SM fermions, external width, `+ h.c.` via `HC[]` |
| `top-philic_Zprime.fr` | BSM extension | a neutral vector coupling to one quark flavour, `InteractionOrder -> {NP,1}` on couplings |
| `HillModel.fr` | BSM extension (scalar sector) | extra scalars mixing with the Higgs, internal parameters and mixing angles |
| `SM.fr` | standalone | the full Standard Model with its gauge-group section — the reference for standalone models only |

Provenance: `python-agent/tests/assets/`, used by that package's tests. Two assets are deliberately not
listed here: `minimal_Zp.fr` (the minimal B-L Z' of arXiv:1605.02910) and `KK_graviton.fr` (arXiv:hep-ph/9909255)
are benchmark models of `paper-reproduction/`; giving the agent their solution would contaminate the
benchmark. Add examples from non-benchmark models only.
