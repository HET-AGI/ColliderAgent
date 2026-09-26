| Column | Runs | Success | Wall (h) | LLM calls | Tool calls | Tool errors | Error-refine cycles | Magnus jobs | Max context (k tok) | Tokens in (M) | Exit reasons |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| claude-opus-5 | 5 | 5 | 1.83 | - | - | - | - | 12 | - | 10.1 | - |
| gemini-3.1-pro-preview / adk | 21 | 8 | 1.41 | 117 | 117 | 39 | 39 | 26 | 120 | 8.3 | completed (11), max_llm_calls (10) |
| gemini-3.1-pro-preview / gemini | 7 | 7 | 0.63 | - | 72 | - | - | 11 | - | 3.7 | completed (7) |
| gpt-5.3-codex / codex | 7 | 5 | 0.81 | - | - | - | - | 15 | - | 5.3 | - |
| gpt-5.5 / adk | 7 | 7 | 0.71 | 35 | 39 | 4 | 4 | 13 | 71 | 1.9 | completed (7) |
