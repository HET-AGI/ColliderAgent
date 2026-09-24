Unit tests for the memory maintainer (`scripts/memory/distill.py`), the benchmark harness (`scripts/bench/`) and `scripts/install.sh`.
Run from the repo root with `python3 -m pytest scripts/tests -q`; tests use only fixtures under pytest's tmp_path and never touch the network, `~/.claude`, or Magnus.
`smoke.sh` is only exercised with `--dry-run`; the real smoke gate needs a Magnus login on zhustation.
