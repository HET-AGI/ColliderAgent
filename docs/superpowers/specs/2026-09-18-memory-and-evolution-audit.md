# 审计：subagent 的运行时经验该放在哪里、怎么读、怎么防止僵化（2026-09-18）

数据来源：2026-09-16/17 的 13 个沙盒（9 个 Opus 4.6 + Opus 5/4.8/Sonnet 5 各 1 + Opus 5 复核 1），每个沙盒的主会话与子 agent transcript。

## 1. 数据：各类 subagent 的报错与试错

| subagent | 工具调用 | magnus run | 报错结果 | 主要报错签名 |
|---|---:|---:|---:|---|
| collider-simulator | 5226 | 102 | 69 | `InvalidCmd('only one laststep argument is allowed')` ×5、`invalid ... argument` ×3、`delphes not install` ×2、`Unknown parameter(s): process_dir, seed, timeout` ×1、`Parameter 'output': expected str` ×1、job 上传 "No space left on device"、`is not a valid directory` ×2 |
| model-generator | 568 | 56 | 25 | `ImportError` ×13（其中 Python-2 `raise UFOError, "msg"` 在 4 个独立 run 里各被重新发现一次）、`KeyError` ×5、validate 失败 3、`WolframScript did not produce valid output` 2、`InvalidCmd: No particle generate in model` 1 |
| pheno-analyzer | 166 | 0 | 12 | `No module named 'pylhe'`、`No such file: 'latex'`（usetex）、brentq 无符号变化 |

FeynRules 一步的试错（validate / generate-ufo / madgraph-compile 次数）：Opus 4.6 多数为 1/1/2–5，Sonnet 5 为 4/5/4，Opus 4.8 为 3/3/2，Scalar LQ（4.6）为 3/3/5。其中可机械消除的：Python-2 raise（4 次）、`M$GaugeGroups` 字面量出现在注释里导致 blueprint 把扩展模型当作独立模型（我们自己的 `templates/skeleton.fr` 第 42 行注释就带这个词，已改）、`FSD[` 泄漏 Mathematica（Sonnet 5 的两处）。

## 2. 逐问回答

**Q1 经验写到一个文件还是按 subagent 分？后续怎么读？**
按 subagent 分，这不是设计偏好而是 Claude Code 的机制：agent 文件里 `memory: user` 让每个子 agent 拥有 `~/.claude/agent-memory/<agent>/`，harness 在子 agent 启动时把该目录 `MEMORY.md` 的前 200 行（≤25 KB）注入其 system prompt，并给它该目录的 Read/Write/Edit。读取不需要任何检索代码；写入由子 agent 在阶段结束时按 run-lessons 契约完成。这次 13 个沙盒里子 agent 一共写了 28 条 schema 合规的 lesson，说明"子 agent 不能写 memory"的前提不成立——不能的是它看不到父会话的上下文，也不会被注入父会话的 auto-memory。阶段边界就是故障类型边界（FeynRules 语法 / MG5 launch / 分析），所以按 agent 分正好；跨阶段的 lesson（collider-simulator 在 compile 时发现的 UFO 缺陷）由 `distill.py route` 按 `stage` 字段搬到归属 agent（feynrules/ufo/calchep → model-generator 等）。

**Q2 FeynRules 这一步如何用经验大幅减少试错，又不被 pattern 卡死？**
按脆弱度分三层，经验只在第三层进 memory：
1. 机械性、可判定的失败 → 脚本，不进 memory 也不进 prose：`ufo-generator/scripts/ufo_fix.py`（修 Python-2 raise、删 `__pycache__`、逐文件 py_compile、报告 Mathematica 泄漏与空 lorentz/vertices）、`feynrules-model-generator/scripts/fr_lint.py`（`M$GaugeGroups` 字面量、`FSD[`、单字符 ClassName、括号不平衡、`Width -> 0`、h.c. 与 HC[] 不一致）。这次 13 次 ImportError 和多轮 validate 里的大部分会被这两个脚本在提交前拦下，每次省一个云端往返。这正是论文里说的 sedimentation：进化的落点是代码，不是记忆。
2. 工具契约事实（参数名、blueprint 的怪癖）→ skill 文本，这是 `/skill-evolve` 的目标。
3. 需要判断的启发式（SU(2) 场强要按分量展开、CC[] 用在有色费米子上、Majorana 归一化）→ memory，且只作为"症状匹配时的提示"：索引行给症状和修法，agent 必须打开文件看证据并用工具结果验证；lesson 与契约或任务冲突时以后者为准；新增 `contradictions` 计数（试了没用就 +1），达到 support 时自动退出提名和索引前列；`generalizable: false` 永不提升；decay 归档长期未确认的条目。僵化的另一个来源是"同一事实换了措辞就成了新条目、support 永远是 1"，已把去重改成同 stage+blueprint 下的词集相似度（4 条 Python-2 raise 的不同写法现在合并为 support 4 并进入提名）。
   比规则更有效的 FeynRules 记忆是**已验证的模型文件本身**（example-based）：建议给 feynrules-model-generator 加 `references/examples/`，但只放非 benchmark 模型（`python-agent/tests/assets/` 已有 6 个），否则 S5 的三次 attempt 会被污染。

**Q3 evolution 是直接改 skill，还是加 memory？**
两者都要，分层：memory 是子 agent 自写、按阶段、低成本、可撤销的 staging 层；skill 是人工把关的持久层，只接收在 ≥3 个独立 run 里重复、且过 smoke 门禁的条目；脚本是机械失败的最终落点。没有 memory 层，skill 的改动只能靠人翻 transcript（这次 4 个 run 各自重新发现同一个 bug 就是例子）；没有 skill/脚本层，memory 会越积越多并把一次性的 workaround 当规则。

## 3. 本分支已落实（commit 见 git log）
- `distill.py`：`route` 子命令；词集相似度去重；`contradictions` 字段进 schema、索引行、提名过滤。
- `ufo_fix.py`、`fr_lint.py` 及测试；skeleton.fr 去掉致病注释；ufo-generator / feynrules-model-validator / feynrules-model-generator / run-lessons / model-generator / pheno-analyzer 文本接入。
- pheno-analyzer 环境事实：无 pylhe、无 pyhepmc、无 LaTeX。

## 4. 事例生成一步：参数类报错已写入 skill（commit 见 git log），存储上限的数值未改，等 collaborator 改完 Magnus 存储参数再同步
collider-simulator 这次的参数类报错，已作为 madgraph-simulator skill 的 "Parameters and syntax that cost retries in earlier runs" 一节：
- 重簇射既有 run 的语法只有一种：`launch -i <dir>` 后 `pythia8 run_XX --laststep=delphes`（"only one laststep argument"×5、"invalid argument"×3 来自试错这一句）。
- blueprint 只接受 schema 里的参数；`process_dir`、`seed`、`timeout` 都不存在（用 `set iseed` 设种子）；`--output` 必填字符串。
- `delphes not install` 出现在 `launch -i` 重簇射时未启用 detector 开关的情形；`No events file corresponding to run` 是 `--laststep` 指到不存在的 run。
- 10 GB 打包上限与 `!` 清理已写入（commit 61800a9），存储参数放宽后需同步改数值。

## 5. 依赖类报错的修复（2026-09-18）
- `No module named 'pylhe'`（pheno-analyzer）、`pyhepmc` 缺失：已安装，并写入根目录 `requirements.txt` 与 `python-agent/pyproject.toml` 的 `analysis` 可选依赖组；README 的先决条件改为 `pip install -r requirements.txt`，`magnus-sdk>=0.8`。
- `latex could not be found`（matplotlib `text.usetex`）：不是 pip 依赖，主机不装 TeX；pheno-analyzer 契约改为用 mathtext、禁用 usetex。
- `lhapdf-config` 本地不存在：PDF 集由 launch job 的 `--pdf` 安装，skill 已说明本地不做任何 PDF 操作。
- 新增 `scripts/check_env.py`（magnus 站点、Python 栈版本、可选工具），`run_benchmark.sh` 启动前调用；其输出即论文 Table S2 的 agent runtime 行。
- FeynRules 示例库 `references/examples/`（W'、top-philic Z'、Hill 标量、standalone SM），刻意排除两个 benchmark 模型。
