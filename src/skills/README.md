# ColliderAgent — Skills

**Reusable skill modules loaded by coding agents (Claude Code, Cursor, Codex, ...) to execute collider-physics tasks.**

Each skill is a directory containing a `SKILL.md` (frontmatter + workflow) plus optional `references/` and `templates/`. Skills are the portable unit of domain knowledge — the same directory can be consumed by any agent that understands the Agent Skills format, or registered on a Magnus station for cloud-side invocation.

## Skills

| Skill | Description |
|---|---|
| [`pheno-pipeline-orchestrator`](pheno-pipeline-orchestrator/) | 编排从拉氏量到图表的完整唯象流水线：run label、progress 记录、stepN.json 交接、增量任务 |
| [`feynrules-model-generator`](feynrules-model-generator/) | 从 LaTeX 拉氏量生成 FeynRules `.fr` 模型文件 |
| [`feynrules-model-validator`](feynrules-model-validator/) | 校验 `.fr` 的物理自洽性，并验证 UFO 能否被 MadGraph5 正确导入 |
| [`ufo-generator`](ufo-generator/) | 将 `.fr` 模型转换为 UFO 格式，供 MadGraph5 / Herwig / Sherpa 使用 |
| [`calchep-generator`](calchep-generator/) | 将 `.fr` 模型转换为 CalcHEP 格式，供 CalcHEP / micrOmegas 使用 |
| [`madgraph-simulator`](madgraph-simulator/) | 用 MadGraph5 生成蒙特卡洛事件，支持 Pythia8 簇射、Delphes 探测器模拟、MadSpin、LHAPDF |
| [`madanalysis-analyzer`](madanalysis-analyzer/) | 用 MadAnalysis5 分析蒙卡事件，产出运动学分布与 cutflow 表 |
| [`micromegas-calculator`](micromegas-calculator/) | 用 micrOmegas 计算暗物质遗迹丰度、直接探测与间接探测观测量 |
| [`magnus`](magnus/) | 通过 `magnus` CLI 在 zhustation 上调度蓝图任务：上传、下载、结果检查、断线恢复 |
| [`run-lessons`](run-lessons/) | 子 agent 跨 run 记忆的契约：何时读、何时写、lesson 文件格式（由子 agent 预加载） |
| [`skill-evolve`](skill-evolve/) | `/skill-evolve`：把反复出现的 lesson 提升为 skill 文本，跑 smoke 门禁后留在审阅分支 |
| [`execution-summarizer`](execution-summarizer/) | 流水线结束后生成从 prompt 到代码的映射摘要报告（forked context） |
| [`reproduction-guide-generator`](reproduction-guide-generator/) | 为已完成的分析生成可复现的实验包（含 `run_all.sh` 与 README，forked context） |

## Layout conventions (v2, 2026-09)

- One owner per fact: Magnus mechanics live in `magnus`, workspace layout and handoff in `pheno-pipeline-orchestrator`, each blueprint's contract in its stage skill. Other files point to the owner in one line.
- `SKILL.md` = contract (parameters, result fields, paths, failure modes) + the few fragile rules with their reasons + pointers. Worked examples and long syntax live in `references/`. Keep each `SKILL.md` under roughly 5 k tokens: Claude Code re-attaches at most the last 5 k tokens of a skill after context compaction.
- Stage subagents (`src/agents/`) are thin role contracts; the skills they list under `skills:` are preloaded into their context, so the agent file never restates a skill body.
- Every stage writes `progress/<run>/stepN_<stage>.json` next to the `.md` record; the orchestrator passes paths, not physics.
- `memory: user` on the four stage agents turns on per-agent cross-run memory (`~/.claude/agent-memory/<agent>/`). `scripts/memory/distill.py` maintains the index; `/skill-evolve` promotes recurring lessons into skill text behind a smoke gate and a human review.

Install or check the installed copies with `scripts/install.sh` / `scripts/install.sh --check`.

## Syncing with Magnus

Skills are also registered on the active Magnus station so that agents running in the cloud can discover them. The descriptions above are the canonical copy — keep them in sync with the station.

Push a skill to the station:

```bash
magnus skill save <id> ./<id>/ -t "<id>" -d "<Chinese description>"
```

Pull a skill from the station (for inspection):

```bash
magnus skill get <id>
```

Note: `SKILL.md` frontmatter `description:` is the agent-facing **trigger description** (natural-language conditions for when the skill should fire), whereas the Magnus station `-d` field is the **human-facing catalogue description** (what the skill does, one sentence). The two serve different audiences and are intentionally different.
