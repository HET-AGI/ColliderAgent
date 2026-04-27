# Optional Features

This document describes optional features that can be applied between `madgraph-compile` (Step 1) and `madgraph-launch` (Step 2). Only apply these when the user explicitly requests them.

---

## Enable LHCO Output

**When to use**: The user requests LHCO-format event files.

**Prerequisite**: `detector=Delphes` must be set in the launch commands. LHCO output is a Delphes feature.

**What to do**: After `madgraph-compile` downloads the compiled process directory, uncomment the `root2lhco` section (lines 48–58) in `<process_dir>/bin/internal/run_delphes3`. This section is commented out by default; uncommenting it tells Delphes to convert the ROOT output to LHCO format during event generation.

```bash
# Use sed to uncomment lines 48-58 in run_delphes3
sed -i '' '48,58 s/^#//' path/to/pp_ttbar/bin/internal/run_delphes3
```

**Output**: The launch step will produce `tag_1_delphes_events.lhco.gz` in `Events/run_XX/` alongside the ROOT file.

---

## Enable MadSpin Decays

**When to use**: The user wants spin-correlated decays of unstable resonances (top, W, Z, BSM particles) applied **after** the hard event is generated, without baking the decay chain into the `generate` line at compile time. MadSpin preserves angular correlations that a flat narrow-width treatment would lose, and lets you swap or rerun decay topologies without recompiling the process.

Prefer MadSpin over decay-chain syntax in `--process` when:
- You expect to vary or scan the decay final state (e.g. dileptonic vs. semileptonic top decays) on top of one compiled process.
- Spin correlations matter for the analysis (e.g. top polarization, anomalous couplings).
- The decay width is small enough that the narrow-width approximation is reasonable (`onshell` / `none` modes) or you explicitly want off-shell effects via `full`.

**How to enable**: this is configured entirely through `--commands`; no file edits are needed.

1. In **State 1** (before the first `done`), add the switch:
   ```
   madspin=ON
   ```
   This is mandatory. Without it, any `set spinmode` / `decay` lines in State 2 are dispatched to a card that MadSpin never reads, and MadSpin is silently skipped.
2. In **State 2** (between the two `done`s), specify the spin-correlation mode and one `decay` line per unstable particle:
   ```
   set spinmode onshell
   decay t > b l+ vl
   decay t~ > b~ l- vl~
   ```

**Multi-step / cascade decays**: chain them inside a single `decay` line with commas, the same syntax as MG5 process decay chains. For example:
```
decay t > b w+, w+ > l+ vl
decay t~ > b~ w-, w- > l- vl~
```
Each `decay` line targets one mother particle (by PDG label, e.g. `t`, `t~`, `w+`, `z`, `h`); cascades go inside that line.

**`spinmode` options**:

| `spinmode` value | Meaning |
|------------------|---------|
| `none` | No spin correlations. Fastest; equivalent to flat isotropic decay in the rest frame. Use only when correlations are known to be irrelevant. |
| `onshell` | Spin-correlated decays in the narrow-width approximation (resonances strictly on-shell). Default and recommended for narrow resonances like top, W, Z. |
| `full` | Spin-correlated decays including off-shell / finite-width effects. Slower and statistically less efficient; use when off-shell tails matter. |

**CRITICAL: silent failure modes.** MadSpin has two ways to be silently skipped while the job still reports `success=true`:
- **Forgot `madspin=ON` in State 1**: the State 2 `set spinmode` / `decay` lines look syntactically valid and are accepted by the run-card editor, but no MadSpin step runs. You will get the original undecayed `unweighted_events.lhe.gz` only — no `run_XX_decayed_1/` directory.
- **Put `decay` lines after the second `done`**: MG5 has already launched; the `decay` lines fall through to the master prompt and are swallowed as unknown commands. Same symptom: no `run_XX_decayed_1/` directory.

Always verify after the run that `Events/run_XX_decayed_1/` exists. If it does not, MadSpin did not run.

**Output**: when MadSpin runs successfully, decayed events are written to a sibling directory next to the original run:
- `Events/run_XX_decayed_1/unweighted_events.lhe.gz` — MadSpin-decayed LHE events (the file Pythia8 and Delphes consume downstream).
- `Events/run_XX_decayed_1/tag_1_pythia8_events.hepmc.gz` — if Pythia8 is enabled.
- `Events/run_XX_decayed_1/tag_1_delphes_events.root` — if Delphes is enabled.

The original undecayed events remain at `Events/run_XX/unweighted_events.lhe.gz` for reference.
