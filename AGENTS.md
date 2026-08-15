# ColliderAgent Codex adapter

## Scope

This branch provides the Codex-native harness adapter for ColliderAgent. Keep
the physics workflows in `src/skills/` and the role definitions in
`src/agents/` as the canonical sources. Treat `.agents/` and `.codex/` as a
thin discovery and orchestration layer; do not duplicate the domain workflows
there.

## Skills

Repository skills are exposed through `.agents/skills/`. When a task matches a
skill description, read that skill's complete `SKILL.md` before acting and load
only the references needed for the current stage. Use
`pheno-pipeline-orchestrator` for multi-stage analyses and follow-ups that
propagate changes through downstream stages.

## Subagents

For a multi-stage pipeline, delegate to the project-scoped custom agents in
this order when their stages are required:

1. `model-generator`
2. `collider-simulator`
3. `event-analyzer`
4. `pheno-analyzer`

Run dependent stages sequentially and wait for each agent before starting its
consumer. Do not run write-heavy pipeline stages in parallel. Give every agent
the relevant task requirements, upstream artifact paths and parameter mapping,
and the exact progress file it must update. The parent agent owns the run
manifest, cross-stage decisions, final execution summary, and user-facing
answer.

## Magnus backend

Use only the persisted remote `zhustation` Magnus site. Before the first compute
stage, run `magnus config` and require `Current: zhustation` with an HTTPS
address. Never start local Magnus, select localhost, or fall back to locally
installed HEP tools. If the station is unavailable after the retries specified
by the Magnus skill, preserve completed artifacts and report the remote-service
failure. Never print, copy, or commit the Magnus token.

## Verification

Keep generated scripts and progress artifacts out of source changes unless the
user explicitly requests them. For adapter changes, validate TOML syntax,
skill metadata, symlink targets, and the diff against `main`; an end-to-end
physics run is a separate evaluation step.
