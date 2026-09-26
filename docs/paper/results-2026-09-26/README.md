# Model C 与综合 S4 对比（2026‑09‑26）

这一轮补齐论文 Table S4 的"传统 agent 框架"一列（Model C = Google ADK 单循环 agent + Gemini 3.1 Pro），并做了两组对照，回答一个问题：**现代编码型 agent（Claude Code / Codex / Gemini CLI）在多轮"执行‑报错‑修正"、长上下文的长程任务上，是否明显优于传统的单循环工具型 agent，且这种优势来自结构而不只是模型。**

| 文件 | 内容 |
|---|---|
| `tables.md` | `aggregate.py` 输出：S3（成功 run 的均值）、S4（模型 × harness × benchmark）、S5（合并所有模型的失败模式）与每个成功 run 的 footnote |
| `runs.csv` | 每个 run 一行（84 行：本轮 53 个沙盒 + 9/16、9/24 的 31 个文档记录） |
| `longhorizon_light.md` / `longhorizon_heavy.md` | 每个"模型 / harness"列的长程指标：LLM 调用、工具调用、工具报错、报错‑修正循环、上下文峰值、token、退出原因（后四项只有 ADK 的事件日志能测） |
| `figures/` | 每次尝试的结果图，`<arxiv>_fig<N>__<model-harness>__a<attempt>[-FAILED].png` |

判定标准与 9/24 相同（端到端 + 与参考图定性一致，数值偏差进 footnote；失败模式 model / generation / analysis / infrastructure），判图先由 Opus 5 辅助、再逐张人工核对；本轮另加**作业来源检查**（`scripts/bench/job_provenance.py`，见第 6 节）。

## 1. 各列的设置

| 列 | 模型 | harness | 运行方式 |
|---|---|---|---|
| A | Claude Opus 4.6（2026‑02‑05） | Claude Code 2.1.28x，v2 skills + 4 个子 agent | 9/16 与 9/24 的数据（`results-2026-09-24/`） |
| A′ | Claude Opus 5 | 同上 | 本轮补跑 5 题 ×1（ALP、U(1)′ 为 9/16 数据） |
| B | GPT‑5.3‑Codex（2026‑02‑05，与 Opus 4.6 同日） | Codex CLI 0.155.1，API key，`codex-com` 分支 skills‑only + 4 个自定义 agent | 本轮 7 轻 ×1 + 2 重 ×1 |
| B′ | gpt‑5.5 | 同上（ChatGPT 登录） | 9/24 的 4 题 |
| **C** | **Gemini 3.1 Pro preview**（2026‑02‑19） | **`python-agent/`：Google ADK 2.10 单个 `LlmAgent` + 13 个扁平工具，LiteLLM 经中转，无子 agent / 无 skills / 无记忆 / 无上下文压缩，`max_llm_calls`=150（重题 300），6 h 墙钟** | **7 轻 ×3 + 2 重 ×1** |
| 对照 C₁ | Gemini 3.1 Pro preview | Gemini CLI 0.61（编码型 agent），同一份 `.agents/skills`，无自定义子 agent | 7 轻 ×1 |
| 对照 C₂ | gpt‑5.5 | ADK（与 C 完全相同的代码） | 7 轻 ×1 + 2 重 ×1 |

ADK 只做了"能跑"级别的最小修复（见 commit `e019374`）：加 `run_python`/`run_shell` 工具（否则除 MA5 直方图外任何图都产不出），加逐事件日志用于计量，`madgraph_compile` 接受内置模型名，调用上限从 20 提到 150。工具参数与 zhustation 上的 5 个 blueprint 一致，Magnus 走 `~/.magnus` 的当前站点。

## 2. Table S4（本轮结果，成功/尝试）

| Benchmark | A Opus 4.6 ×3 | A′ Opus 5 | B 5.3‑codex/Codex | B′ 5.5/Codex | **C Gemini/ADK ×3** | C₁ Gemini/Gemini CLI | C₂ 5.5/ADK |
|---|---:|---:|---:|---:|---:|---:|---:|
| Heavy N（1308.2209 Fig. 3） | 3/3 | 1/1 | 1/1 | – | **1/3** | 1/1 | 1/1 |
| U(1)′ scan（1605.02910 Fig. 1） | 3/3 | 1/1 | 1/1 | 1/1 | **1/3** | 1/1 | 1/1 |
| ALP EFT（1701.05379 Fig. 8） | 3/3 | 1/1 | 1/1 | 1/1 | **2/3** | 1/1 | 1/1 |
| General Z′（2103.02708 Fig. 4） | 3/3 | 1/1 | 1/1 | – | **1/3** | 1/1 | 1/1 |
| KK graviton（9909255 Fig. 2） | 3/3 | 1/1 | 1/1 | – | **2/3** | 1/1 | 1/1 |
| MuC η（2104.05720 Fig. 11） | 2/3 | 1/1 | 0/1 | – | **0/3** | 1/1 | 1/1 |
| MuC reach（2104.05720 Fig. 12） | 3/3 | 运行中 | 0/1 | – | **1/3** | 1/1 | 1/1 |
| **轻量 7 题合计** | **20/21** | 6/6 | **5/7** | 4/4（含重题 2） | **8/21** | **7/7** | **7/7** |
| Scalar LQ（2005.06475 Fig. 2，重） | 0/1（TBD） | – | 0/1 | 1/1 | 运行中 | – | 0/1 |
| mono‑τ（1811.07920 Fig. 3，重） | 0/1 | – | 1/1 | 1/1 | 运行中 | – | 运行中 |

Opus 4.8 / Sonnet 5 各 1/1（ALP，9/16）不再列出。

## 3. 长程指标（轻量 7 题，逐 run 均值）

| 列 | run | 成功 | 时长 [h] | LLM 调用 | 工具调用 | 工具报错 | 报错‑修正循环 | Magnus jobs | 上下文峰值 [k tok] | 输入 tokens [M] | 退出原因 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Gemini 3.1 Pro / ADK | 21 | 8 | 1.41 | 117 | 117 | 39 | 39 | 26 | 120 | 8.3 | 11 次自行结束，**10 次触及 150 次上限** |
| gpt‑5.5 / ADK | 7 | 7 | 0.71 | 35 | 39 | 4 | 4 | 13 | 71 | 1.9 | 7 次自行结束 |
| Gemini 3.1 Pro / Gemini CLI | 7 | 7 | 0.63 | – | 72 | – | – | 11 | – | 3.7 | 7 次自行结束 |
| gpt‑5.3‑codex / Codex | 7 | 5 | 0.81 | – | – | – | – | 15 | – | 5.3 | – |
| Opus 5 / Claude Code | 4 | 4 | 1.22 | – | – | – | – | 10 | – | 6.9 | – |

（Codex / Claude Code 的转录里没有逐次工具成功标志，报错‑修正循环不可比，故留空；Gemini CLI 的 `tool_result` 状态对 shell 命令失败不敏感，同样留空。）

ADK+Gemini 21 次 run 的分布：成功的 8 次用 20–126 次调用；失败的 13 次里 10 次是 150 次上限耗尽（其中 7 次卡在事例生成、2 次卡在模型/UFO、1 次画出空图），2 次是 agent 自行放弃，1 次是耦合赋值错误（SSM/ψ 曲线颠倒）。三次 MuC Fig. 11 分别报错 108、78、121 次，上下文膨胀到 379k / 182k / 230k tokens，全部失败。

## 4. 结论（供论文 S4 讨论）

1. **同一模型、换 harness，结果从 8/21 变成 7/7**：Gemini 3.1 Pro 在 Gemini CLI（skills、shell、文件工具、自动上下文管理）里 7 题全部一次通过，平均 0.63 h、72 次工具调用；放进 ADK 单循环后只有 38 % 成功，平均 117 次 LLM 调用、39 次工具报错，近半数 run 触顶。结构差异是主要因素。
2. **但前沿模型能"扛住"糟糕的结构**：gpt‑5.5 在完全相同的 ADK 循环里 7/7，平均只用 35 次调用、4 次报错，上下文峰值 71k。单循环结构对轻量题的惩罚在弱一档的模型上显现，在最强模型上被模型自身的纠错能力掩盖。
3. **长程重题是分水岭**：Scalar LQ / mono‑τ 需要 10 万事例的 Pythia8+Delphes、轻子→光子的 LHE 改写、10 GB 作业空间限制下的分批与清理，20–40 个作业、2.5–6 h。编码型 agent 用自写脚本 + 重新 launch 解决（Codex gpt‑5.5 4.4 h 完成 Scalar LQ，gpt‑5.3‑codex 2.6 h 完成 mono‑τ 且排除限最接近论文）；ADK+gpt‑5.5 在 Scalar LQ 上遇到"工具不支持 LHE 改写"就退回 parton 级近似（判失败），ADK+Gemini 的重题见第 5 节的更新。
4. **失败模式**：ADK 的失败集中在"事例生成阶段的报错循环"（generation 7 次）和"模型/UFO 阶段"（model 4 次），与 Opus 4.6 的唯一失败（MuC Fig. 11 耦合未生效）和 Codex 5.3‑codex 的 MuC 两题失败（同一种耦合问题 + 空等高线）不同：后者是单点物理错误，前者是循环卡死。
5. **U(1)′ 3 TeV 面板的偏差**（9/17、9/24 文档需更正）：尖端 g₁′≈0.48 出现在 Opus 4.6 ×3、Opus 5、gpt‑5.3‑codex、ADK+gpt‑5.5；0.55 在 Gemini CLI；0.65（论文值）只在 Codex gpt‑5.5。这是多数 run 共有的分析选择所致，不是某个模型或 prompt 的固有限制。mono‑τ 同理：Claude 续跑与 Codex gpt‑5.5 偏弱 20–35 %，gpt‑5.3‑codex 基本复现论文（0.88 对 0.8）。

## 5. 本轮的运行记录与异常

- 所有沙盒在 `/playpen1/shiqiu/collideragent-bench_runs/`（/home 只剩 17 GB），汇总后已删除；`invalid/` 下隔离了 1 个无效 run（见第 6 节）。
- 并发 9–12 个 run；轻量题 ADK 0.4–2.8 h，Codex 0.45–1.2 h，Gemini CLI 0.36–0.94 h，Opus 5 0.7–1.7 h。费用：Opus 5 每题 $7–13（Claude CLI 计费）；Codex 与 ADK 走 API key，Gemini 走中转，未单独计费。
- 中转（`api.openlux.ai`）以 OpenAI 兼容格式提供 Gemini，不回传 thought_signature 也能多轮函数调用；LiteLLM 侧未见限流。
- Gemini CLI 需 `~/.gemini/settings.json` 里 `security.auth.selectedType = "gemini-api-key"` 且 `security.folderTrust.enabled = false`，否则无头模式报 "Invalid auth method" / 不信任目录；`--output-format stream-json` 给出可计量的事件流。
- Codex 改用 API key 登录后 gpt‑5.3‑codex 可用（ChatGPT 登录不可用），B 列因此得以用与 Opus 4.6 同日发布的模型完成。

### 5.1 重题（更新中）

| run | 结果 |
|---|---|
| Codex gpt‑5.3‑codex Scalar LQ | 失败（generation）：LUXlep PDF 装不上（blueprint `--pdf` 在 zhustation 缺 `lhapdf-config`），0.8 h 放弃；gpt‑5.5 与 Opus 4.6 当时用 MG5 内 `pdlabel/lhaid` 绕过 |
| Codex gpt‑5.3‑codex mono‑τ | 成功（2.64 h，8 个作业，排除边界贴 RH 带，0.8 TeV 处 0.88 对论文 ≈0.8） |
| ADK gpt‑5.5 Scalar LQ | 失败（generation）：只做 parton 级，未做 Pythia8/Delphes/选择，自行做"分辨率近似"（0.68 h，67 次调用） |
| ADK gpt‑5.5 mono‑τ | 运行中 |
| ADK Gemini Scalar LQ | 运行中 |
| ADK Gemini mono‑τ | 运行中 |

## 6. 基准有效性：共享作业列表

Magnus 站点的作业列表对所有 run 可见且不清理（833+ 条）。本轮第一个 gpt‑5.3‑codex Heavy N 用 7 分钟"完成"：它 `magnus jobs` 搜到 9/16 Opus 4.6 提交的 pp→μN 扫描作业，`magnus logs` 读出截面直接画图，没有建模型。处理：该 run 隔离到 `invalid/` 并重跑；所有 harness 的 prompt 追加 `scripts/bench/benchmark_rules.md`（只能用本会话提交的作业，不得搜索作业列表）；每个完成的沙盒用 `job_provenance.py` 核对"引用的作业 id ⊆ 本会话提交的 id"（Codex 子线程日志、创建时间落在本 run 窗口内的作业都算本会话）。本轮其余 52 个 run 全部通过。9/24 及更早的 run 没有做过这项检查（沙盒已删），但它们都自己建了模型、提交了 5–42 个作业。

## 7. 还缺什么

- Opus 4.6 在 Scalar LQ / mono‑τ 上的 ×3（脚注 a/b 仍是 TBD）；Opus 5 与 Codex 5.3‑codex 的轻量题 ×3（目前各 ×1）。
- 若要把"结构 vs 模型"的归因做得更严：Opus 4.6 或 Opus 5 放进 ADK 循环（需要 Anthropic API key 经 LiteLLM）。
