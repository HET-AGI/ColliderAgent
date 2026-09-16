#!/usr/bin/env bash
# Install this checkout's skills and agents into a Claude Code config dir, or check the
# installed copies for drift (docs/superpowers/specs/2026-09-16-skill-evolution-design.md, 2.4).
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: scripts/install.sh [--check] [--target <dir>]

Copies src/skills/<skill>/ and src/agents/*.md into <dir>/skills and <dir>/agents.
<dir> defaults to $CLAUDE_CONFIG_DIR, or $HOME/.claude when that is unset.
Every skill directory present in src/skills replaces the installed one wholesale;
skills that exist only under the target are left untouched.

  --check         copy nothing; diff every src skill/agent against the installed copy,
                  list the drift and exit 1 (exit 0 when everything is identical)
  --target <dir>  install into / check against <dir> instead of the config dir
  -h, --help      show this help
USAGE
}

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_SKILLS="$REPO_ROOT/src/skills"
SRC_AGENTS="$REPO_ROOT/src/agents"
TARGET="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
CHECK=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --check) CHECK=1; shift ;;
    --target)
      [[ $# -ge 2 ]] || { echo "install.sh: --target needs a value" >&2; exit 2; }
      TARGET="$2"; shift 2 ;;
    --target=*) TARGET="${1#--target=}"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "install.sh: unknown argument: $1" >&2; usage >&2; exit 2 ;;
  esac
done

[[ -d "$SRC_SKILLS" && -d "$SRC_AGENTS" ]] || {
  echo "install.sh: src/skills or src/agents missing under $REPO_ROOT" >&2; exit 2; }

# A skill is a directory under src/skills that contains SKILL.md (loose files are skipped).
skills=()
for d in "$SRC_SKILLS"/*/; do
  [[ -f "${d}SKILL.md" ]] || continue
  skills+=("$(basename "$d")")
done
agents=()
for f in "$SRC_AGENTS"/*.md; do
  [[ -f "$f" ]] || continue
  agents+=("$(basename "$f")")
done
[[ ${#skills[@]} -gt 0 ]] || { echo "install.sh: no skills found in $SRC_SKILLS" >&2; exit 2; }

if [[ $CHECK -eq 1 ]]; then
  drift=()
  for s in "${skills[@]}"; do
    if [[ ! -d "$TARGET/skills/$s" ]]; then
      drift+=("skills/$s: not installed")
    elif ! out="$(diff -rq "$SRC_SKILLS/$s" "$TARGET/skills/$s" 2>&1)"; then
      drift+=("skills/$s: differs")
      while IFS= read -r line; do [[ -n "$line" ]] && drift+=("    $line"); done <<< "$out"
    fi
  done
  for a in "${agents[@]}"; do
    if [[ ! -f "$TARGET/agents/$a" ]]; then
      drift+=("agents/$a: not installed")
    elif ! cmp -s "$SRC_AGENTS/$a" "$TARGET/agents/$a"; then
      drift+=("agents/$a: differs")
    fi
  done
  if [[ ${#drift[@]} -eq 0 ]]; then
    echo "install.sh --check: ${#skills[@]} skills and ${#agents[@]} agents in $TARGET match $REPO_ROOT/src"
    exit 0
  fi
  echo "install.sh --check: drift between $REPO_ROOT/src and $TARGET:" >&2
  printf '  %s\n' "${drift[@]}" >&2
  echo "run: scripts/install.sh --target '$TARGET'" >&2
  exit 1
fi

mkdir -p "$TARGET/skills" "$TARGET/agents"
for s in "${skills[@]}"; do
  rm -rf "${TARGET:?}/skills/${s:?}"
  cp -R "$SRC_SKILLS/$s" "$TARGET/skills/$s"
done
for a in "${agents[@]}"; do
  cp "$SRC_AGENTS/$a" "$TARGET/agents/$a"
done
echo "install.sh: installed ${#skills[@]} skills and ${#agents[@]} agents into $TARGET"
