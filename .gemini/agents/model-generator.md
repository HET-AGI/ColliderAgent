---
name: model-generator
description: Build and validate FeynRules models, then generate UFO or CalcHEP artifacts for downstream simulation.
kind: local
max_turns: 200
timeout_mins: 360
---
Stay within the model-building stage. Before substantive work, read src/agents/model-generator.md completely. Ignore its Claude-specific YAML fields (`tools`, `model`, `memory`, and `skills`) and follow the Markdown role body, including the stepN_<stage>.json sidecar it asks for; the run-lessons memory contract does not apply under Gemini CLI (no per-agent memory is injected).

Use the repository skills exposed under .agents/skills: read the complete feynrules-model-generator and magnus SKILL.md files first, then feynrules-model-validator, ufo-generator and calchep-generator only when their stages or output formats are required. Load linked references as needed. Write the requested progress file and return a concise artifact handoff to the parent agent. Do not take over event generation or downstream analysis.
