# ColliderAgent benchmark 结果包（2026-09-24）

论文表格 S3 / S4 / S5 所需的全部实验数据都在这个目录里；`bench_runs/` 下的沙盒（transcript、事件文件、UFO 等中间产物）已经删除，不再保留。

| 文件 | 内容 |
|---|---|
| `tables.md` | `scripts/bench/aggregate.py` 的输出：Table S3（成功 run 的资源均值）、S4（模型 × benchmark 成功/尝试）、S5（benchmark 成功/尝试 + 失败模式）以及每个成功 run 的数值偏差 footnote 原文 |
| `runs.csv` | 每个 run 一行：attempt 编号、模型、harness、effort、成功与否、失败模式、时长、子 agent 调用、Magnus jobs、写入文件数、tokens（主会话 + 全部子 agent）、费用、模型延迟占比、footnote |
| `documented_runs.json` | 沙盒已不存在、数字取自 `docs/paper-tbd-audit-2026-09-16.md` / `handover-2026-09-17.md` 的 run（2026-09-16 的 Opus 4.6 第 1 次尝试和 Opus 5 / Opus 4.8 / Sonnet 5 单次 run） |
| `figures/` | 每个 run 的结果图，命名 `<arxiv>_fig<N>__<model>__a<attempt>[-FAILED].png`；参考图在 `paper-reproduction/<arxiv>/reference/` |

重新生成表格（沙盒存在时）：

```bash
python3 scripts/bench/aggregate.py bench_runs/ \
  --extra docs/paper/results-2026-09-24/documented_runs.json \
  --csv docs/paper/results-2026-09-24/runs.csv > docs/paper/results-2026-09-24/tables.md
```

判定标准（2026-09-16 约定）：端到端跑完并产出所要求的图，且与参考图对应部分定性一致即记为成功；数值偏差写进 footnote。失败模式按论文的四类 model / generation / analysis / infrastructure。每个 verdict 先由 Opus 5 辅助判图（`scripts/bench/judge.sh`），再由人逐张核对。

## 1. Table S5：Opus 4.6（`--effort xhigh`，v2 skills，冷记忆）× 3 次

| Benchmark | 第 1 次（9/16） | 第 2 次（9/24） | 第 3 次（9/24） | 成功/尝试 |
|---|---|---|---|---:|
| Heavy N（1308.2209 Fig. 3） | 成功 0.40 h / $4.2 | 成功 0.37 h / $3.6 | 成功 1.04 h / $6.7 | 3/3 |
| U(1)′ scan（1605.02910 Fig. 1） | 成功* 1.05 h / $9.2 | 成功* 1.07 h / $7.5 | 成功* 0.65 h / $6.1 | 3/3 |
| ALP EFT（1701.05379 Fig. 8） | 成功 0.86 h / $22.2 | 成功* 1.30 h / $10.5 | 成功* 0.87 h / $5.7 | 3/3 |
| General Z′（2103.02708 Fig. 4） | 成功 0.66 h / $13.3 | 成功* 0.59 h / $3.9 | 成功* 0.94 h / $4.4 | 3/3 |
| KK graviton（9909255 Fig. 2） | 成功* 1.35 h / $6.4 | 成功* 0.76 h / $6.1 | 成功* 0.75 h / $6.6 | 3/3 |
| U1 LQ at MuC, η（2104.05720 Fig. 11） | 成功 0.55 h / $5.9 | **失败（model）** 0.74 h / $14.5 | 成功* 0.81 h / $9.7 | 2/3 |
| U1 LQ at MuC, reach（2104.05720 Fig. 12） | 成功* 1.41 h / $20.6 | 成功* 1.38 h / $10.0 | 成功* 0.87 h / $7.4 | 3/3 |
| Scalar LQ m_ej（2005.06475 Fig. 2） | TBD（6.4 h 停止，脚注 a） | 未跑 | 未跑 | 0/1 |
| U1 LQ mono‑τ（1811.07920 Fig. 3） | 失败（infrastructure，脚注 b） | 未跑 | 未跑 | 0/1 |

`*` 有数值偏差 footnote（原文见 `tables.md` 末尾）。7 个轻量 benchmark 共 21 次尝试 20 次成功；唯一失败是 MuC Fig. 11 第 2 次：两条 LQ 曲线与 SM 逐 bin 只差 2–3 %，即 LQ 贡献没有进入事例生成（归为 model）。第 1 次 MuC Fig. 11 没有触发 orchestrator（主会话自己跑完，子 agent 0 次），结果正确。

脚注 a / b 与 2026-09-17 的交接文档相同：Scalar LQ 的 10 万事例 Delphes ROOT（27 GB）超过 launch job 的 10 GB 打包空间；mono‑τ 第 1 次在事例生成后 orchestrator 以"等待下载"结束回合而会话终止。两题的 ×3 补跑没有在本轮进行（每次 4–6 h、xhigh 下 >$100，见第 5 节）。

## 2. Table S3：资源用量（Opus 4.6，成功 run 的均值）

| Benchmark | 次数 | 时长 [h] | 子 agent | Magnus jobs | 文件 | 输入 tokens [M] | 输出 [k] | USD |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Heavy N | 3 | 0.60 | 3.0 | 9.0 | 14.3 | 3.88 | 17.2 | 4.81 |
| U(1)′ scan | 3 | 0.92 | 3.3 | 17.0 | 22.3 | 4.43 | 29.5 | 7.58 |
| ALP EFT | 3 | 1.01 | 3.0 | 6.7 | 16.7 | 15.06 | 30.5 | 12.81 |
| General Z′ | 3 | 0.73 | 3.0 | 7.3 | 14.3 | 8.29 | 25.1 | 7.18 |
| KK graviton | 3 | 0.95 | 2.7 | 9.3 | 14.3 | 3.80 | 28.2 | 6.37 |
| U1 LQ at MuC, η | 2 | 0.68 | 3.0 | 14.0 | 6.0 | 4.43 | 18.4 | 7.81 |
| U1 LQ at MuC, reach | 3 | 1.22 | 3.0 | 19.0 | 21.7 | 13.26 | 38.9 | 12.65 |
| Scalar LQ m_ej（第 1 次，未完成） | – | 6.41 | 2 | 42 | 28 | 214.0 | 220 | – |
| U1 LQ mono‑τ（第 1 次，失败） | – | 4.00 | 2 | 29 | 19 | 181.4 | 219 | 106 |

tokens = 主会话 + 全部子 agent（未缓存 + 缓存写 + 缓存读）；文件 = 写入或编辑的不同路径数；Magnus jobs = `magnus run` 提交次数；USD 取 CLI 的 `total_cost_usd`。逐次的数值在 `runs.csv`。轻量 7 题 21 次 run 的范围：0.37–1.41 h、$3.6–22.2、输入 1.3–36.9 M tokens。模型延迟占 wall‑clock 的比例（transcript 时间戳）：0.23–0.80，中位数 0.55（21 次）；论文里"LLM inference accounts for a minor fraction"一句应改为"轻量 benchmark 中模型推理与集群作业各占约一半，只有 Delphes 级别的 benchmark 和 Dark‑SMEFT campaign 由集群时间主导"。

## 3. Table S4：模型对比

| Benchmark | A：Opus 4.6（Claude Code，×3） | B：GPT‑5.5（Codex CLI 0.155.1，×1） | C：留白 |
|---|---:|---:|---:|
| Heavy N | 3/3 | – | – |
| U(1)′ scan | 3/3 | 1/1（1.03 h，21 jobs，11.0 M tokens） | – |
| ALP EFT | 3/3 | 1/1（0.99 h，9 jobs，13.4 M tokens） | – |
| General Z′ | 3/3 | – | – |
| KK graviton | 3/3 | – | – |
| U1 LQ at MuC, η | 2/3 | – | – |
| U1 LQ at MuC, reach | 3/3 | – | – |
| Scalar LQ m_ej | 0/1 | 1/1*（4.41 h，5 子 agent，24 jobs，75.0 M tokens） | – |
| U1 LQ mono‑τ | 0/1 | 1/1*（2.55 h，3 子 agent，20 jobs，49.4 M tokens） | – |

- **B 列说明**：计划中的 GPT‑5.3‑Codex 在 ChatGPT 登录的 Codex 里不可用（gpt‑5.3‑codex / 5.2‑codex / 5.4 / 5.5‑codex 都被拒绝，需要 API key：`codex login --with-api-key`），本轮用同一账号可用的 gpt‑5.5 代替；Codex 在 `codex-com` 分支（commit cc4c666，与 feat/skill-evolution-v2 的 skills 同步）以 skills‑only 模式运行，同样的 prompt，harness `scripts/bench/run_benchmark_codex.sh`，指标由 `collect_metrics_codex.py` 从事件流和主/子线程 rollout 汇总。Codex 走订阅账号，费用无法计量（`runs.csv` 里为空）。
- **U(1)′ 3 TeV 面板**：Codex/gpt‑5.5 复现出论文的轮廓尖端（g̃ ≈ −0.72，g₁′ ≈ 0.65），而 Opus 4.6 三次和 Opus 5 一次都给出 0.48。因此 2026‑09‑17 文档里"该偏差来自 prompt 的分析流程而非 agent"的说法撤回：prompt 足以得到论文结果，25 % 的偏差是 Claude run 的分析选择。
- **Scalar LQ（Codex/gpt‑5.5）**：端到端完成（4.41 h）：10 万 LUXlep parton 事例、轻子→光子 LHE 替换、Pythia8 + Delphes(ATLAS) 到 LHCO。前两次探测器模拟失败（交互式 re‑shower 找不到 pythia8_card.dat，并撞到 "No space left on device"），第三次改用非交互式 launch 成功。m_ej 信号峰在 3 TeV，峰值约 1.5 events/bin/100 fb⁻¹（论文约 3，低约 2 倍），分布止于 3.8 TeV（论文尾部到 5 TeV）；Delphes 卡用了 anti‑kT R=0.6 而非 0.4。Opus 4.6 第 1 次在同一阶段被停掉（6.4 h），说明该题用当前 skills 是可以完成的，Opus 4.6 的 ×3 补跑值得做。
- **mono‑τ（Codex/gpt‑5.5）**：端到端完成，LH/RH R_D(*) 带与论文一致，排除边界形状一致但整体弱约 30 %（0.8 TeV 处 √|g_c g_b| ≈ 1.07，论文 ≈ 0.8；4 TeV 处到达 4.0，论文的排除区在 5 TeV 仍贴着 RH 带）。Opus 4.6 第 1 次的续跑（另一套独立实现）同样弱 20–35 %，所以这项偏差更可能来自 prompt 规定的分析流程（例如 LHCO 里没有单独的 τ 集合、用 type‑4 jet 代替强子 τ），而不是某一个 agent 的失误；论文的 EFT 有效性线和 150 fb⁻¹ / 3 ab⁻¹ 投影线没有画。
- 2026‑09‑16 的单次跨模型 run（默认 effort）仍然有效：ALP EFT 上 Opus 5 0.87 h / $9.06、Opus 4.8 1.05 h / $12.55、Sonnet 5 1.38 h / $7.54 全部成功；Opus 5 另跑 U(1)′ 一次成功（0.88 h / $14.32）。这些行在 `tables.md` 里作为独立列出现。

## 4. 本轮运行记录（2026‑09‑24）

- 第 2 次尝试 7 题 18:22 UTC 并行启动，全部 0.37–1.38 h 结束。
- 第 3 次尝试 19:42 UTC 启动；其中 4 个 run 在 38–40 min 时死于 `OAuth session expired and could not be refreshed`：沙盒里是 `.credentials.json` 的副本，主 `~/.claude` 一刷新 token 副本就失效。harness 改为符号链接共享凭据（commit 9689e8b）；U(1)′ 那次图和 step‑4 sidecar 已写出、只缺总结，保留为成功并记 footnote；另外 3 个（ALP、KK graviton、MuC Fig. 11）作废并于 20:23 UTC 重启，重启后全部成功。作废的 3 次不计入 S5。
- 辅助判图有一次输出的 JSON 用分号分隔字段导致解析失败（KK graviton 第 3 次），已人工核对并修正 `judge.sh` 的解析。
- 本轮 Opus 4.6 共 14 次有效 run：$102.56、wall‑clock 合计 12.1 h、输入 78.7 M tokens。
- Codex gpt‑5.5 四题（19:05 UTC 启动）：ALP 0.99 h、U(1)′ 1.03 h、mono‑τ 2.55 h、Scalar LQ 4.41 h，全部成功（订阅账号，费用不计）。

## 5. 还缺什么

1. **Scalar LQ 与 mono‑τ 的 Opus 4.6 ×3**：未跑。两题根因都已写进 skills（madgraph‑simulator 的 10 GB 输出限制与 `!` 清理；orchestrator 禁止以"等待"结束回合），但每次预计 1.5–2 h（若顺利）到 4–6 h，xhigh 下 >$100，建议 `--effort high`：`scripts/bench/run_benchmark.sh 2005.06475 2 claude-opus-4-6 --effort high`、`... 1811.07920 3 ...`。
2. **Model B 的 GPT‑5.3‑Codex**：需要 OpenAI API key；有 key 后 `scripts/bench/run_benchmark_codex.sh <arxiv> <fig> gpt-5.3-codex` 即可，其余流程不变。
3. **Model B 的其余 5 个轻量 benchmark 和 ×3**：每题约 1 h，Codex 订阅下无直接费用。
4. **Model C**：留白（可用 Sonnet 5 或 Opus 5，`run_benchmark.sh <arxiv> <fig> claude-sonnet-5`）。
5. Codex 的两个重题（Scalar LQ、mono‑τ）都已完成（成功*，见第 3 节）。
