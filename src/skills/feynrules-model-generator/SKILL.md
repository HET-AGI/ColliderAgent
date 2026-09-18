---
name: feynrules-model-generator
description: Write a FeynRules .fr model file for a BSM Lagrangian given in LaTeX — particle classes, parameters, and the Lagrangian in FeynRules syntax — ready for validation and UFO or CalcHEP export. Use whenever a task provides a Lagrangian and needs a FeynRules model.
---

# FeynRules Model Generator

Turns a LaTeX Lagrangian into a `.fr` file that defines the BSM extension of the Standard Model. This is pure authoring: no Magnus job is involved until validation (feynrules-model-validator skill) and export (ufo-generator / calchep-generator skills).

## Paths (relative to the working directory)

- Model file: `models/<Model>.fr`
- Exported directories later: `models/<Model>_UFO/`, `models/<Model>_CH/`

## Approach

Start from `templates/skeleton.fr` (all required sections with TODO markers) and fill it section by section: `M$ModelName` and `M$Information`, index definitions, `M$ClassesDescription`, `M$Parameters`, the Lagrangian. Working one section at a time keeps each FeynRules construct checkable against `references/feynrules_syntax.md` (section 5: particle-class attributes per spin; 6: external/internal parameters and mixing matrices; 7–8: Lagrangian syntax and a complete BSM example). Write only the BSM part: the SM is loaded automatically at validation and export time.

Before writing, settle the physics-to-FeynRules mapping: new fields with quantum numbers and spin, couplings with their chirality structure, whether `+ h.c.` is present, and which SM symbols appear (`ee`, `gw`, `gs`, `g1`, `sw`/`cw`, `vev`, …). BSM PDG codes go above 9000000 unless the particle has an established reservation (5000039 for a KK graviton, 9900012 for a heavy neutrino in existing UFOs).

## Conventions that decide whether the model validates

- **Class names** have at least two characters (`Zp`, `N1`, `Snew`); one-letter names collide with FeynRules internals.
- **Hermitian conjugate**: when the Lagrangian says `+ h.c.`, write the non-Hermitian part as `LNPtmp := Block[{…}, …]` and `LNP := LNPtmp + HC[LNPtmp]`; when it does not, write the term directly, because adding `HC[]` doubles Hermitian terms and breaks the hermiticity check.
- **Indices**: declare dummy indices with `Block[{…}, …]`; each spinor index appears exactly twice per monomial; each monomial is electrically neutral; use explicit `*` for every product.
- **Projectors and bilinears**: `ProjM` = (1−γ5)/2, `ProjP` = (1+γ5)/2; `psibar.Ga[mu].ProjM.psi` or fully indexed `psibar[sp1].Ga[mu,sp1,sp2].ProjM[sp2,sp3].psi[sp3]`.
- **Chirality flips** (L→R substitutions) replace projectors, fields, and coupling parameters together.
- **Non-self-conjugate fields**: `X` carries the positive charge, `Xbar` the negative one.
- **Parameters**: every new coupling is `External` with `BlockName`, `OrderBlock`, `Value`, and `InteractionOrder -> {NP, 1}` (internal derived parameters keep the same order tag). Masses and widths are set in the particle class, not in `M$Parameters`.
- **Widths of decaying BSM particles** are external parameters (`Width -> {WZp, 0.04}`) or `{WZp, Internal}`; `Width -> 0` marks the particle stable in MG5, which then silently ignores `set param_card DECAY` for it.
- **micrOmegas targets**: Z₂-odd particles need a leading `~` in `ParticleName` (and `AntiParticleName`), because micrOmegas identifies the dark sector by that prefix in the exported CalcHEP files (calchep-generator skill).

## Before submitting

Run the linter that ships with this skill:

```bash
python3 <skill-dir>/scripts/fr_lint.py models/<Model>.fr        # --standalone for a full model with its own gauge groups
```

It catches what cost a cloud round-trip in earlier runs: the literal name of the gauge-group section appearing anywhere in an extension file (the export tools decide standalone-vs-extension by a substring test, comments included), `FSD[` (not a built-in; it leaks Mathematica into the UFO), one-letter class names, unbalanced brackets, `Width -> 0`, and an `h.c.` mention without `HC[]` or vice versa. Fix errors before validating; read warnings.

## Next step

Validate with the feynrules-model-validator skill (`magnus run validate-feynrules -- --model models/<Model>.fr --lagrangian <symbol>`), then export. Also check by eye that every `+ h.c.` decision above matches the Lagrangian; the validator reports hermiticity but not whether you doubled a term that was already Hermitian.

References: `references/feynrules_syntax.md` (full `.fr` syntax, common errors, PDG conventions), `templates/skeleton.fr`.
