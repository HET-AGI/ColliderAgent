# ColliderAgent — Blueprints

**Magnus blueprint definitions, synced from the active Magnus station.**

Each `.yaml` file is a self-contained blueprint that can be registered with Magnus via:

```bash
magnus blueprint save <id> --file src/blueprints/<id>.yaml
```

## Blueprints

| File | Blueprint ID | Description |
|------|-------------|-------------|
| `validate-feynrules.yaml` | `validate-feynrules` | Validate `.fr` model via Mathematica |
| `generate-ufo.yaml` | `generate-ufo` | Export FeynRules model to UFO format |
| `generate-calchep.yaml` | `generate-calchep` | Export FeynRules model to CalcHEP format |
| `madgraph-compile.yaml` | `madgraph-compile` | Import UFO model, compile MadGraph5 process |
| `madgraph-launch.yaml` | `madgraph-launch` | Run Monte Carlo event generation |
| `madanalysis-process.yaml` | `madanalysis-process` | MadAnalysis5 event analysis |
| `micromegas-compile.yaml` | `micromegas-compile` | Build a micrOmegas project from CalcHEP model + user `main.c` |
| `micromegas-calc.yaml` | `micromegas-calc` | Execute the compiled `./main`, capture `results.json` |

## Syncing

To pull the latest blueprint from a Magnus station:

```bash
magnus blueprint get <id> > src/blueprints/<id>.yaml
```

To push a local blueprint to the station:

```bash
magnus blueprint save <id> --file src/blueprints/<id>.yaml
```

## Entry-Point Scripts

Blueprint entry commands reference Python scripts in `scripts/` that run inside the Magnus container. See [`scripts/README.md`](../../scripts/README.md) for details.
