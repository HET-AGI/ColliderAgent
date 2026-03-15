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
