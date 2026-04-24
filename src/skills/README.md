# ColliderAgent — Skills

**Reusable skill modules loaded by coding agents (Claude Code, Cursor, Codex, ...) to execute collider-physics tasks.**

Each skill is a directory containing a `SKILL.md` (frontmatter + workflow) plus optional `references/` and `templates/`. Skills are the portable unit of domain knowledge — the same directory can be consumed by any agent that understands the Agent Skills format, or registered on a Magnus station for cloud-side invocation.

## Skills

| Skill | Description |
|---|---|
| [`feynrules-model-generator`](feynrules-model-generator/) | 从 LaTeX 拉氏量生成 FeynRules `.fr` 模型文件 |
| [`feynrules-model-validator`](feynrules-model-validator/) | 校验 FeynRules `.fr` 的物理自洽性，并验证 UFO 能否被 MadGraph5 正确导入 |
| [`ufo-generator`](ufo-generator/) | 将 `.fr` 模型转换为 UFO 格式，供 MadGraph5 / Herwig / Sherpa 使用 |
| [`calchep-generator`](calchep-generator/) | 将 `.fr` 模型转换为 CalcHEP 格式，供 CalcHEP / micrOmegas 使用 |
| [`madgraph-simulator`](madgraph-simulator/) | 用 MadGraph5 生成蒙特卡洛事件，支持 Pythia8 簇射与 Delphes 探测器模拟 |
| [`madanalysis-analyzer`](madanalysis-analyzer/) | 用 MadAnalysis5 分析蒙卡事件，产出运动学分布与 cutflow 表 |
| [`micromegas-calculator`](micromegas-calculator/) | 用 micrOmegas 计算暗物质遗迹丰度、直接探测与间接探测观测量 |
| [`magnus`](magnus/) | 通过 `magnus` CLI 在云集群上调度蓝图任务 |
| [`pheno-pipeline-orchestrator`](pheno-pipeline-orchestrator/) | 编排从拉氏量到图表的完整唯象流水线，支持多阶段与增量任务 |
| [`reproduction-guide-generator`](reproduction-guide-generator/) | 为已完成的分析生成可复现的实验包（含 `run_all.sh` 与 README） |
| [`execution-summarizer`](execution-summarizer/) | 流水线结束后生成从 prompt 到代码的映射摘要报告 |

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
