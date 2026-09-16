#!/usr/bin/env bash
# Assistive figure judge: compares the sandbox's newest output figure with a reference image
# through `claude -p` (vision, Read tool only) and writes verdict.yaml. A human confirms the
# verdict before it goes into a table (judged_by says so).
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: scripts/bench/judge.sh <sandbox> <reference.png>

Finds the newest output/figures/*.png|*.pdf in <sandbox> (a PDF is rasterised with
pdftoppm when no PNG of the same name exists), asks the judge model to compare it with the
reference image, and writes <sandbox>/verdict.yaml:

  success: true|false|null         null when the judge output could not be parsed
  failure_mode: model|generation|analysis|infrastructure|null
  notes: "..."                     raw judge text when parsing failed
  judged_by: "<model> (assistive; human confirm required)"

Environment: JUDGE_MODEL (default claude-opus-5), JUDGE_MAX_TURNS (default 4; only passed
when the installed CLI supports --max-turns).
USAGE
}

if [[ $# -ge 1 ]]; then
  case "$1" in -h|--help) usage; exit 0 ;; esac
fi
[[ $# -eq 2 ]] || { usage >&2; exit 2; }
[[ -d "$1" ]] || { echo "judge.sh: sandbox not found: $1" >&2; exit 2; }
[[ -f "$2" ]] || { echo "judge.sh: reference image not found: $2" >&2; exit 2; }
SANDBOX="$(cd "$1" && pwd)"
REF="$(cd "$(dirname "$2")" && pwd)/$(basename "$2")"
JUDGE_MODEL="${JUDGE_MODEL:-claude-opus-5}"
JUDGED_BY="$JUDGE_MODEL (assistive; human confirm required)"
VERDICT="$SANDBOX/verdict.yaml"

write_verdict() {  # <success> <failure_mode|null> <notes> <produced|->
  SUCCESS="$1" FAILURE_MODE="$2" NOTES="$3" PRODUCED="$4" REF="$REF" JUDGED_BY="$JUDGED_BY" \
  python3 - "$VERDICT" <<'PY'
import json, os, sys
q = lambda s: json.dumps(s, ensure_ascii=False)
fm = os.environ["FAILURE_MODE"]
lines = [
    f"success: {os.environ['SUCCESS']}",
    f"failure_mode: {fm if fm in ('model', 'generation', 'analysis', 'infrastructure') else 'null'}",
    f"notes: {q(os.environ['NOTES'])}",
    f"judged_by: {q(os.environ['JUDGED_BY'])}",
    f"produced_figure: {q(os.environ['PRODUCED'])}",
    f"reference_figure: {q(os.environ['REF'])}",
]
open(sys.argv[1], "w", encoding="utf-8").write("\n".join(lines) + "\n")
PY
  cat "$VERDICT"
}

# --- newest produced figure --------------------------------------------------------------
FIG_DIR="$SANDBOX/output/figures"
NEWEST=""
if [[ -d "$FIG_DIR" ]]; then
  NEWEST="$(find "$FIG_DIR" -maxdepth 1 -type f \( -iname '*.png' -o -iname '*.pdf' \) -printf '%T@ %p\n' \
            | sort -rn | head -n 1 | cut -d' ' -f2-)"
fi
if [[ -z "$NEWEST" ]]; then
  write_verdict false null "no figure found under output/figures (nothing to judge)" "-"
  exit 0
fi
PRODUCED="$NEWEST"
if [[ "${NEWEST,,}" == *.pdf ]]; then
  SAME_STEM="${NEWEST%.*}.png"
  if [[ -f "$SAME_STEM" ]]; then
    PRODUCED="$SAME_STEM"
  else
    command -v pdftoppm >/dev/null 2>&1 || { write_verdict null null "newest figure is a PDF and pdftoppm is not installed: $NEWEST" "$NEWEST"; exit 1; }
    pdftoppm -png -r 150 -singlefile "$NEWEST" "$SANDBOX/judge_figure"
    PRODUCED="$SANDBOX/judge_figure.png"
  fi
fi

# --- ask the judge model ---------------------------------------------------------------
PROMPT="You are an assistive judge for a particle-physics paper-reproduction benchmark.
Produced figure (image file): $PRODUCED
Reference figure (image file): $REF
Use the Read tool to open both image files, then decide whether the produced figure reproduces the reference: same observable and axes, same qualitative shape and normalisation, and the labelled features (peaks, cut-offs, curves, legend entries) in the right place. Cosmetic differences (colours, fonts, legend position, binning, style) do not matter.
Reply with ONLY one JSON object and nothing else (no prose, no code fence):
{\"success\": true or false, \"failure_mode\": \"model\" or \"generation\" or \"analysis\" or \"infrastructure\" or null, \"notes\": \"one or two sentences\"}
failure_mode is null when success is true; otherwise choose the most likely stage that went wrong: model (Lagrangian/UFO/parameters), generation (process, cuts, beams, event generation), analysis (observable, histogramming, normalisation, plotting), infrastructure (tooling, missing or unreadable output)."

CLAUDE_ARGS=(-p "$PROMPT" --model "$JUDGE_MODEL" --output-format json --allowedTools Read)
if claude --help 2>/dev/null | grep -q -- '--max-turns'; then
  CLAUDE_ARGS+=(--max-turns "${JUDGE_MAX_TURNS:-4}")
fi
RAW="$SANDBOX/judge_raw.json"
set +e
claude "${CLAUDE_ARGS[@]}" > "$RAW" 2> "$SANDBOX/judge_stderr.log"
RC=$?
set -e

# --- parse the verdict ------------------------------------------------------------------
RAW="$RAW" RC="$RC" PRODUCED="$PRODUCED" REF="$REF" JUDGED_BY="$JUDGED_BY" python3 - "$VERDICT" <<'PY'
import json, os, re, sys
q = lambda s: json.dumps(s, ensure_ascii=False)
try:
    text = open(os.environ["RAW"], encoding="utf-8", errors="replace").read()
except OSError:
    text = ""
result_text = text
try:
    data = json.loads(text)
    if isinstance(data, dict) and isinstance(data.get("result"), str):
        result_text = data["result"]
except ValueError:
    pass
verdict = None
m = re.search(r"\{.*\}", result_text, re.S)
if m:
    try:
        verdict = json.loads(m.group(0))
    except ValueError:
        verdict = None
if isinstance(verdict, dict) and isinstance(verdict.get("success"), bool):
    success = "true" if verdict["success"] else "false"
    fm = verdict.get("failure_mode")
    fm = fm if fm in ("model", "generation", "analysis", "infrastructure") else "null"
    notes = str(verdict.get("notes") or "")
else:
    success, fm = "null", "null"
    notes = "judge output could not be parsed (claude exit %s): %s" % (os.environ["RC"], result_text.strip()[:1500])
lines = [
    f"success: {success}",
    f"failure_mode: {fm}",
    f"notes: {q(notes)}",
    f"judged_by: {q(os.environ['JUDGED_BY'])}",
    f"produced_figure: {q(os.environ['PRODUCED'])}",
    f"reference_figure: {q(os.environ['REF'])}",
]
open(sys.argv[1], "w", encoding="utf-8").write("\n".join(lines) + "\n")
print(open(sys.argv[1], encoding="utf-8").read(), end="")
PY
