# ColliderAgent Gemini CLI adapter

## Scope

This branch provides the Gemini CLI adapter for ColliderAgent. Keep the physics
workflows in `src/skills/` and the role definitions in `src/agents/` as the
canonical sources. Treat `.agents/` and `.gemini/` as a thin discovery and
orchestration layer; do not duplicate the domain workflows there.

## Skills

Repository skills are exposed through `.agents/skills/` (Gemini CLI reads this
directory as workspace skills). When a task matches a skill description,
activate that skill and read its complete `SKILL.md` before acting; load only
the references needed for the current stage. Use `pheno-pipeline-orchestrator`
for multi-stage analyses and follow-ups that propagate changes through
downstream stages.

## Subagents

For a multi-stage pipeline, delegate to the project-scoped local subagents in
`.gemini/agents/` in this order when their stages are required:

1. `model-generator`
2. `collider-simulator`
3. `event-analyzer`
4. `pheno-analyzer`

Run dependent stages sequentially and wait for each subagent before starting
its consumer. Do not run write-heavy pipeline stages in parallel. Give every
subagent the relevant task requirements, upstream artifact paths and parameter
mapping, and the exact progress file it must update. The parent agent owns the
run manifest, cross-stage decisions, final execution summary, and user-facing
answer. Every stage writes `progress/<run>/stepN_<stage>.md` and the
`stepN_<stage>.json` sidecar described in the agent role files; pass paths, not
physics, between stages. Subagents cannot call other subagents, so the parent
does all delegation. Use the deterministic helpers that ship with the skills
before submitting cloud jobs: `fr_lint.py` (feynrules-model-generator) and
`ufo_fix.py` (ufo-generator). The `run-lessons` skill and the `memory:` field
of the agent files are Claude Code features and do not apply here.

## Magnus backend

Use only the persisted remote `zhustation` Magnus site. Before the first compute
stage, run `magnus config` and require `Current: zhustation` with an HTTPS
address. Never start local Magnus, select localhost, or fall back to locally
installed HEP tools. Never end a turn to wait for a cloud job: poll
`magnus job status <id>` (with sleeps inside one shell command) until it
finishes, then continue. If the station is unavailable after the retries
specified by the Magnus skill, preserve completed artifacts and report the
remote-service failure. Never print, copy, or commit the Magnus token.

## Headless runs

Benchmarks run `gemini -m <model> --yolo --output-format stream-json -p "<prompt>"`
with `GEMINI_API_KEY` and, for a relay, `GOOGLE_GEMINI_BASE_URL`; the user's
`~/.gemini/settings.json` must select `security.auth.selectedType =
"gemini-api-key"` and set `security.folderTrust.enabled = false`.

## Verification

Keep generated scripts and progress artifacts out of source changes unless the
user explicitly requests them. For adapter changes, validate the agent
frontmatter, skill metadata, symlink targets, and the diff against `codex-com`;
an end-to-end physics run is a separate evaluation step.
