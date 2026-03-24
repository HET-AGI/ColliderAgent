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

## LHE Lepton-to-Photon Patching

**When to use**: Automatically applied when the proton definition includes leptons (e.g., for LUXlep PDF processes) AND Pythia8 shower is requested. This is NOT an optional feature — it is **required** for correct shower behavior.

**Background**: Pythia8 cannot backward-evolve initial-state leptons from the proton PDF. Without patching, Pythia8 produces ~67% `partonLevel failed` retries and thousands of color-tracing errors per run. With patching, Pythia8 runs cleanly with zero shower errors.

**What to do**: After `madgraph-launch` produces the parton-level LHE (without shower), run the patching script:

```bash
python3 scripts/patch_lhe_lepton_to_photon.py \
  <process_dir>/Events/run_XX/unweighted_events.lhe.gz \
  <process_dir>/Events/run_XX/unweighted_events.lhe.gz
```

The script:
- Reads the LHE file (supports `.lhe` and `.lhe.gz`)
- Finds all initial-state particles (status = -1) with lepton PDG codes (±11, ±13, ±15)
- Replaces their PDG code with 22 (photon)
- Preserves all other event data (momenta, colors, final-state particles)
- Supports in-place patching (same input and output path)

**After patching**: Run Pythia8 + Delphes via `--interactive` mode (see SKILL.md for the complete workflow). The `pythia8_card.dat` must contain `Check:event = off` and `Check:history = off`.

**Script location**: `scripts/patch_lhe_lepton_to_photon.py`. If the script does not exist, see below for the implementation.

<details>
<summary>patch_lhe_lepton_to_photon.py implementation</summary>

```python
#!/usr/bin/env python3
"""Patch LHE file: replace initial-state leptons with photons (PDG 22)
so Pythia8 can backward-evolve them from the proton PDF.

Usage:
    python3 patch_lhe_lepton_to_photon.py input.lhe.gz output.lhe.gz
"""

import gzip
import sys

LEPTON_PDGS = {11, -11, 13, -13, 15, -15}


def patch_lhe(input_path: str, output_path: str) -> dict:
    opener = gzip.open if input_path.endswith('.gz') else open
    with opener(input_path, 'rt') as f:
        content = f.read()

    stats = {'events': 0, 'patched_particles': 0}
    lines = content.split('\n')
    output_lines = []
    in_event = False
    event_line_idx = 0

    for line in lines:
        stripped = line.strip()

        if stripped == '<event>':
            in_event = True
            event_line_idx = 0
            stats['events'] += 1
            output_lines.append(line)
            continue

        if stripped == '</event>':
            in_event = False
            output_lines.append(line)
            continue

        if in_event:
            event_line_idx += 1

            if event_line_idx == 1:
                output_lines.append(line)
                continue

            parts = stripped.split()
            if len(parts) >= 7:
                pdg = int(parts[0])
                status = int(parts[1])

                if status == -1 and pdg in LEPTON_PDGS:
                    parts[0] = '22'
                    remaining = stripped.split(None, 6)[6]
                    output_lines.append(
                        f'      {parts[0]:>9s} {parts[1]:>4s} '
                        f'{parts[2]:>4s} {parts[3]:>4s} '
                        f'{parts[4]:>4s} {parts[5]:>4s} {remaining}'
                    )
                    stats['patched_particles'] += 1
                    continue

            output_lines.append(line)
            continue

        output_lines.append(line)

    out_content = '\n'.join(output_lines)
    out_opener = gzip.open if output_path.endswith('.gz') else open
    with out_opener(output_path, 'wt') as f:
        f.write(out_content)

    return stats


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} input.lhe[.gz] output.lhe[.gz]")
        sys.exit(1)
    stats = patch_lhe(sys.argv[1], sys.argv[2])
    print(f"Patched {stats['patched_particles']} initial-state leptons -> photons "
          f"in {stats['events']} events")
```

</details>
