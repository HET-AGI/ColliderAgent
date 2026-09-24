---
name: calchep-generator
description: Export a validated FeynRules .fr model to a CalcHEP model directory (vars1/func1/prtcls1/lgrng1.mdl) on the Magnus cloud for CalcHEP or micrOmegas, and verify the Z2-odd particle naming that micrOmegas needs. Use after a .fr file passes validation when the task needs dark-matter observables or CalcHEP.
---

# CalcHEP Generator

```bash
magnus run generate-calchep -- --model models/MyModel.fr --lagrangian LNP --output models/MyModel_CH
```

(Execution mechanics, upload/download, recovery: magnus skill.)

| Parameter | Required | Meaning |
|---|---|---|
| `--model` | yes | the validated `.fr` file (uploaded) |
| `--lagrangian` | yes | the Lagrangian symbol in the file |
| `--output` | yes | where the CalcHEP directory is downloaded |
| `--restriction` | no | a `.rst` restriction file (uploaded) |

BSM extensions (no `M$GaugeGroups`) are exported on top of SM.fr with its standard restrictions. Result: `success`, `calchep_path`. The directory holds plain-text CalcHEP tables: `vars1.mdl` (independent parameters — the names `assignValW` accepts), `func1.mdl` (derived parameters), `prtcls1.mdl` (particles), `lgrng1.mdl` (vertices), sometimes `extlib1.mdl`.

## The Z₂-odd naming rule (micrOmegas)

micrOmegas finds the dark sector purely by names: every Z₂-odd particle (the DM candidate and all co-annihilation partners) must appear with a leading `~` in the particle-name column of `prtcls1.mdl` (`~x1` in SingletDM, `~H3 ~H+ ~X` in IDM, `~chi0 ~chi1` in RDM). Without it `sortOddParticles` finds no candidate and every observable is zero or NaN, with no error.

The blueprint calls plain `WriteCHOutput[…]` and passes no separate odd-particle list, so the exported file is the only contract. The recipe that works in this pipeline is to put the tilde in the `.fr` itself: `ParticleName -> "~x1"` (and `AntiParticleName` for non-self-conjugate fields). A custom `QuantumNumbers -> {Z2 -> -1}` alone does not produce the prefix. After export, check:

```bash
grep -E '\|~[A-Za-z]' models/MyModel_CH/prtcls1.mdl
```

Every intended odd particle must be listed. If not, fix the `.fr` and re-export; editing `prtcls1.mdl` by hand is lost on the next export and leaves the `.fr` wrong for the reproduction package.
