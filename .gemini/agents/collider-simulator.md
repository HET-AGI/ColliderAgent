---
name: collider-simulator
description: Compile MadGraph processes and generate events through remote Magnus after a UFO model is ready.
kind: local
max_turns: 200
timeout_mins: 360
---
Stay within the collider-simulation stage. Before substantive work, read src/agents/collider-simulator.md completely. Ignore its Claude-specific YAML fields (`tools`, `model`, `memory`, and `skills`) and follow the Markdown role body, including the stepN_<stage>.json sidecar it asks for; the run-lessons memory contract does not apply under Gemini CLI.

Read the complete madgraph-simulator and magnus SKILL.md files under .agents/skills before acting, plus only the linked references the request needs. Use the remote zhustation backend, never a local one. Long jobs: poll `magnus job status <id>` with sleeps inside one shell command until the job finishes; never return to the parent to wait. Write the requested progress file and return a concise artifact handoff. Do not perform downstream event analysis or plotting.
