| Column | Runs | Success | Wall (h) | LLM calls | Tool calls | Tool errors | Error-refine cycles | Magnus jobs | Max context (k tok) | Tokens in (M) | Exit reasons |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| claude-opus-4-6 | 4 | 4 | 2.44 | - | - | - | - | 24 | - | 38.9 | - |
| claude-opus-5 | 2 | 2 | 2.13 | - | - | - | - | 16 | - | 13.6 | - |
| gemini-3.1-pro-preview / adk | 2 | 0 | 2.04 | 300 | 300 | 52 | 50 | 28 | 169 | 28.4 | max_llm_calls (2) |
| gpt-5.3-codex / codex | 2 | 1 | 1.72 | - | - | - | - | 13 | - | 9.5 | - |
| gpt-5.5 / adk | 2 | 0 | 1.22 | 54 | 57 | 13 | 12 | 18 | 91 | 3.7 | completed (2) |

Claude Code 两行是 2026‑09‑27/28 的 6 个 run（Opus 4.6 xhigh 第 2–3 次尝试 ×2 题，Opus 5 第 1 次 ×2 题，全部成功，`longhorizon_table.py /playpen1/shiqiu/collideragent-bench_runs --benchmarks 2005.06475,1811.07920`）；Codex / ADK 行来自 2026‑09‑26。
