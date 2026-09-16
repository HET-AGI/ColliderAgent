#!/usr/bin/env python3
"""Maintain the per-agent lesson memory that ColliderAgent subagents read at start.

Layout under the memory root (default: $CLAUDE_CONFIG_DIR/agent-memory, or
~/.claude/agent-memory when CLAUDE_CONFIG_DIR is unset):

    <agent>/MEMORY.md        index injected into the subagent prompt (<= 200 lines / 25 KB)
    <agent>/lessons/*.md     one lesson per file: frontmatter (schema.json) + body (<= 15 lines)
    <agent>/archive/*.md     decayed lessons (kept on disk, never indexed)

Commands (all deterministic, no LLM):
    rebuild   validate every lesson, merge near-duplicates, rewrite MEMORY.md
    decay     archive lessons with support 1 not confirmed for --stale-days, then rebuild
    propose   list generalizable lessons with support >= --min-support (+ proposals.json)
    import    merge lessons harvested from another memory root, then rebuild
    new       write one schema-valid lesson file, then rebuild

The frontmatter parser is a small YAML subset: `key: value` scalars, double/single-quoted
strings, inline lists `[a, "b"]`, block lists (`- item` lines), and `# comments` after
unquoted values. Quote any value that contains ` #` or a leading special character.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import sys
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().with_name("schema.json")
INDEX_MAX_LINES = 200
INDEX_MAX_BYTES = 25_000
BODY_MAX_LINES = 15
STAGES = ("feynrules", "ufo", "calchep", "madgraph", "madanalysis", "micromegas", "pheno", "orchestrator")
TARGET_SKILL = {
    "feynrules": "feynrules-model-generator",
    "ufo": "ufo-generator",
    "calchep": "calchep-generator",
    "madgraph": "madgraph-simulator",
    "madanalysis": "madanalysis-analyzer",
    "micromegas": "micromegas-calculator",
    "pheno": "pheno-pipeline-orchestrator",
    "orchestrator": "pheno-pipeline-orchestrator",
}
FIELD_ORDER = ("stage", "blueprint", "symptom", "root_cause", "fix", "evidence",
               "generalizable", "support", "first_seen", "last_confirmed", "tags")
INDEX_NOTE = ("One line per lesson, injected into the subagent prompt at start; "
              "details are in lessons/<file> (maintained by scripts/memory/distill.py).")
OVERFLOW_LINE = "- … {k} more lessons not indexed (run distill.py --propose or open lessons/)"
DEFAULT_BODY = "Symptom, root cause and fix are in the frontmatter; add context below (max 15 lines)."
EXIT_OK, EXIT_ERROR, EXIT_INVALID = 0, 1, 2


class LessonError(ValueError):
    """A lesson file that cannot be parsed or fails the schema."""


# --------------------------------------------------------------------------- frontmatter
def split_frontmatter(text: str) -> tuple[str, str]:
    """Return (frontmatter, body) of a lesson file."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise LessonError("missing frontmatter (file must start with '---')")
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[1:i]), "\n".join(lines[i + 1:])
    raise LessonError("unterminated frontmatter (no closing '---')")


def _strip_comment(s: str) -> str:
    if s.startswith("#"):
        return ""
    return re.split(r"\s+#", s, maxsplit=1)[0].strip()


def _split_inline_list(s: str) -> list[str]:
    items, cur, quote, i = [], [], None, 0
    while i < len(s):
        c = s[i]
        if quote:
            cur.append(c)
            if quote == '"' and c == "\\" and i + 1 < len(s):
                cur.append(s[i + 1])
                i += 2
                continue
            if c == quote:
                quote = None
        elif c in "\"'":
            quote = c
            cur.append(c)
        elif c == ",":
            items.append("".join(cur))
            cur = []
        else:
            cur.append(c)
        i += 1
    items.append("".join(cur))
    return [it.strip() for it in items if it.strip()]


def parse_scalar(raw: str):
    """Parse one YAML-subset scalar (or inline list)."""
    s = raw.strip()
    if not s:
        return None
    if s[0] in "\"'":
        quote = s[0]
        i = 1
        while i < len(s):
            if quote == '"' and s[i] == "\\":
                i += 2
                continue
            if s[i] == quote:
                break
            i += 1
        else:
            raise LessonError(f"unterminated quoted string: {raw.strip()!r}")
        inner = s[1:i]
        if quote == '"':
            try:
                return json.loads('"' + inner + '"')
            except ValueError:
                return inner
        return inner.replace("''", "'")
    s = _strip_comment(s)
    if s == "":
        return None
    if s in ("true", "True"):
        return True
    if s in ("false", "False"):
        return False
    if s in ("null", "~", "None"):
        return None
    if re.fullmatch(r"-?\d+", s):
        return int(s)
    if s.startswith("[") and s.endswith("]"):
        return [parse_scalar(it) for it in _split_inline_list(s[1:-1])]
    return s


def parse_frontmatter(text: str) -> dict:
    """Parse the YAML-subset frontmatter block into a dict."""
    data: dict = {}
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        if line[0] in " \t":
            raise LessonError(f"unexpected indented line: {line.strip()!r}")
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:(.*)$", line)
        if not m:
            raise LessonError(f"cannot parse line: {line.strip()!r}")
        key, rest = m.group(1), m.group(2).strip()
        if key in data:
            raise LessonError(f"duplicate key: {key}")
        bare = rest if rest[:1] in "\"'" else _strip_comment(rest)
        if bare == "":
            items = []
            j = i + 1
            while j < len(lines):
                nxt = lines[j]
                if re.match(r"^\s+-(\s|$)", nxt):
                    items.append(parse_scalar(nxt.lstrip()[1:]))
                elif nxt.strip() and not nxt.lstrip().startswith("#"):
                    break
                j += 1
            data[key] = items if items else None
            i = j
            continue
        data[key] = parse_scalar(rest)
        i += 1
    return data


def yaml_scalar(v) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, int):
        return str(v)
    if v is None:
        return "null"
    s = str(v)
    if re.fullmatch(r"[A-Za-z0-9_./:-]+", s) and s not in ("true", "false", "null", "~", "True", "False", "None") \
            and not re.fullmatch(r"-?\d+", s):
        return s
    return json.dumps(s, ensure_ascii=False)


def dump_frontmatter(meta: dict) -> str:
    keys = [k for k in FIELD_ORDER if k in meta] + [k for k in meta if k not in FIELD_ORDER]
    out = ["---"]
    for k in keys:
        v = meta[k]
        if isinstance(v, list):
            out.append(f"{k}: [{', '.join(yaml_scalar(x) for x in v)}]")
        else:
            out.append(f"{k}: {yaml_scalar(v)}")
    out.append("---")
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------- schema
_SCHEMA_CACHE: dict | None = None


def load_schema() -> dict:
    global _SCHEMA_CACHE
    if _SCHEMA_CACHE is None:
        _SCHEMA_CACHE = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    return _SCHEMA_CACHE


def _type_ok(v, t: str) -> bool:
    if t == "string":
        return isinstance(v, str)
    if t == "integer":
        return isinstance(v, int) and not isinstance(v, bool)
    if t == "number":
        return isinstance(v, (int, float)) and not isinstance(v, bool)
    if t == "boolean":
        return isinstance(v, bool)
    if t == "array":
        return isinstance(v, list)
    if t == "object":
        return isinstance(v, dict)
    if t == "null":
        return v is None
    return True


def _type_name(v) -> str:
    return {bool: "boolean", int: "integer", float: "number", str: "string", list: "array",
            dict: "object", type(None): "null"}.get(type(v), type(v).__name__)


def validate(instance, schema: dict, path: str = "") -> list[str]:
    """Minimal draft-07 validator for the keywords used by schema.json. Returns error strings."""
    errs: list[str] = []
    where = path or "<root>"
    types = schema.get("type")
    if types is not None:
        allowed = types if isinstance(types, list) else [types]
        if not any(_type_ok(instance, t) for t in allowed):
            return [f"{where}: expected {'/'.join(allowed)}, got {_type_name(instance)}"]
    if "enum" in schema and instance not in schema["enum"]:
        errs.append(f"{where}: {instance!r} is not one of {schema['enum']}")
    if isinstance(instance, str):
        if "minLength" in schema and len(instance) < schema["minLength"]:
            errs.append(f"{where}: shorter than {schema['minLength']} characters")
        if "maxLength" in schema and len(instance) > schema["maxLength"]:
            errs.append(f"{where}: longer than {schema['maxLength']} characters")
        if "pattern" in schema and not re.search(schema["pattern"], instance):
            errs.append(f"{where}: {instance!r} does not match {schema['pattern']}")
        if schema.get("format") == "date":
            try:
                dt.date.fromisoformat(instance)
            except ValueError:
                errs.append(f"{where}: {instance!r} is not a valid YYYY-MM-DD date")
    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            errs.append(f"{where}: {instance} is below minimum {schema['minimum']}")
    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            errs.append(f"{where}: needs at least {schema['minItems']} item(s)")
        if "items" in schema:
            for k, item in enumerate(instance):
                errs.extend(validate(item, schema["items"], f"{where}[{k}]"))
    if isinstance(instance, dict):
        for req in schema.get("required", []):
            if req not in instance:
                errs.append(f"{where}: missing required field '{req}'")
        props = schema.get("properties", {})
        for k, v in instance.items():
            child = f"{path}.{k}" if path else k
            if k in props:
                errs.extend(validate(v, props[k], child))
            elif schema.get("additionalProperties") is False:
                errs.append(f"{child}: unknown field")
    return errs


# --------------------------------------------------------------------------- lessons
class Lesson:
    """One lesson file: path, validated frontmatter dict, body text."""

    __slots__ = ("path", "meta", "body")

    def __init__(self, path: Path, meta: dict, body: str = ""):
        self.path = Path(path)
        self.meta = meta
        self.body = body

    @property
    def key(self) -> tuple[str, str]:
        return (self.meta["stage"], normalize_symptom(self.meta["symptom"]))

    def __repr__(self) -> str:
        return f"Lesson({self.path.name}, support={self.meta.get('support')})"


def normalize_symptom(s: str) -> str:
    """Lowercase, replace punctuation by spaces, collapse whitespace."""
    return " ".join(re.sub(r"[^\w\s]", " ", s.lower()).split())


def _date_desc(d: str) -> tuple[int, ...]:
    return tuple(-int(p) for p in d.split("-"))


def load_lesson(path: Path) -> tuple[Lesson, list[str]]:
    """Parse + validate one lesson file. Returns (lesson, warnings); raises LessonError."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        raise LessonError(f"cannot read: {e}") from e
    fm, body = split_frontmatter(text)
    meta = parse_frontmatter(fm)
    errs = validate(meta, load_schema())
    if errs:
        raise LessonError("; ".join(errs))
    warnings = []
    n_body = len([ln for ln in body.strip("\n").splitlines()])
    if n_body > BODY_MAX_LINES:
        warnings.append(f"body has {n_body} lines (> {BODY_MAX_LINES})")
    return Lesson(path, meta, body), warnings


SYMPTOM_MAX = 200


def load_lesson_lenient(path: Path) -> tuple[Lesson, list[str]]:
    """Like load_lesson, but repairs the two format drifts subagents produce: extra top-level keys
    (e.g. the harness's auto-memory `name/description/metadata` block) are dropped, and an over-long
    symptom is truncated to SYMPTOM_MAX with the full text kept in the body. Raises LessonError when
    the file is still invalid afterwards. Returns (lesson, repairs)."""
    text = path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(text)
    known = set(load_schema().get("properties", {}).keys())
    kept, repairs, keep_block = [], [], False
    for ln in fm.splitlines():
        if ln and not ln[0].isspace() and not ln.startswith("-"):
            key = ln.split(":", 1)[0].strip()
            keep_block = key in known
            if not keep_block:
                repairs.append(f"dropped unknown key {key!r}")
        if keep_block:
            kept.append(ln)
    meta = parse_frontmatter("\n".join(kept))
    sym = meta.get("symptom")
    if isinstance(sym, str) and len(sym) > SYMPTOM_MAX:
        meta["symptom"] = sym[:SYMPTOM_MAX - 1].rstrip() + "…"
        body = f"Full symptom: {sym}\n\n" + body.lstrip("\n")
        repairs.append(f"truncated symptom from {len(sym)} to {SYMPTOM_MAX} characters")
    errs = validate(meta, load_schema())
    if errs:
        raise LessonError("; ".join(errs))
    return Lesson(path, meta, body), repairs


def dump_lesson(lesson: Lesson) -> str:
    body = lesson.body.strip("\n")
    return dump_frontmatter(lesson.meta) + (body + "\n" if body else "")


def write_lesson(lesson: Lesson) -> None:
    lesson.path.parent.mkdir(parents=True, exist_ok=True)
    lesson.path.write_text(dump_lesson(lesson), encoding="utf-8")


def merge_lessons(a: Lesson, b: Lesson, sum_support: bool = True) -> Lesson:
    """Merge b into a (a keeps its path, stage, symptom, root cause, body).

    support is summed (or the max when sum_support is False), first_seen is the min,
    last_confirmed the max, evidence the ordered union, fix the longer text, tags the union.
    """
    ma, mb = a.meta, b.meta
    m = dict(ma)
    m["support"] = ma["support"] + mb["support"] if sum_support else max(ma["support"], mb["support"])
    m["first_seen"] = min(ma["first_seen"], mb["first_seen"])
    m["last_confirmed"] = max(ma["last_confirmed"], mb["last_confirmed"])
    evidence = list(ma["evidence"])
    for e in mb["evidence"]:
        if e not in evidence:
            evidence.append(e)
    m["evidence"] = evidence
    if len(mb["fix"]) > len(ma["fix"]):
        m["fix"] = mb["fix"]
    tags = list(ma.get("tags") or [])
    for t in mb.get("tags") or []:
        if t not in tags:
            tags.append(t)
    if tags:
        m["tags"] = tags
    body = a.body if a.body.strip() else b.body
    return Lesson(a.path, m, body)


def dedupe(lessons: list[Lesson]) -> tuple[list[Lesson], list[Path], set[Path]]:
    """Merge lessons sharing (stage, normalised symptom). Returns (kept, removed_paths, changed_paths)."""
    groups: dict[tuple[str, str], list[Lesson]] = {}
    for les in lessons:
        groups.setdefault(les.key, []).append(les)
    kept, removed, changed = [], [], set()
    for grp in groups.values():
        grp.sort(key=lambda l: (-l.meta["support"], l.meta["first_seen"], l.path.name))
        winner = grp[0]
        for other in grp[1:]:
            winner = merge_lessons(winner, other)
            removed.append(other.path)
            changed.add(winner.path)
        kept.append(winner)
    return kept, removed, changed


def slugify(s: str, limit: int = 60) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return (slug[:limit].rstrip("-")) or "lesson"


def unique_path(directory: Path, stem: str, suffix: str = ".md") -> Path:
    cand = directory / f"{stem}{suffix}"
    n = 2
    while cand.exists():
        cand = directory / f"{stem}-{n}{suffix}"
        n += 1
    return cand


# --------------------------------------------------------------------------- agents and index
def default_root() -> Path:
    cfg = os.environ.get("CLAUDE_CONFIG_DIR") or os.path.join(os.path.expanduser("~"), ".claude")
    return Path(cfg) / "agent-memory"


def resolve_root(path_str: str) -> Path:
    """Accept a memory root or a config dir that contains agent-memory/."""
    p = Path(path_str).expanduser()
    if p.name != "agent-memory" and (p / "agent-memory").is_dir():
        return p / "agent-memory"
    return p


def agent_dirs(root: Path, agent: str | None = None) -> list[Path]:
    if not root.is_dir():
        return []
    if agent:
        d = root / agent
        return [d] if d.is_dir() else []
    return sorted(d for d in root.iterdir()
                  if d.is_dir() and not d.name.startswith(".")
                  and ((d / "lessons").is_dir() or (d / "MEMORY.md").is_file()))


def read_agent(agent_dir: Path) -> tuple[list[Lesson], list[tuple[Path, str]], list[str]]:
    """Load every lesson under <agent>/lessons. Returns (lessons, errors, warnings)."""
    lessons, errors, warnings = [], [], []
    ldir = agent_dir / "lessons"
    if not ldir.is_dir():
        return lessons, errors, warnings
    for path in sorted(ldir.glob("*.md")):
        try:
            les, warns = load_lesson(path)
        except LessonError as e:
            errors.append((path, str(e)))
            continue
        lessons.append(les)
        warnings.extend(f"{path}: {w}" for w in warns)
    return lessons, errors, warnings


def validate_root(root: Path, agent: str | None = None) -> tuple[dict[Path, list[Lesson]], list[tuple[Path, str]]]:
    per_agent: dict[Path, list[Lesson]] = {}
    errors: list[tuple[Path, str]] = []
    for d in agent_dirs(root, agent):
        lessons, errs, warns = read_agent(d)
        per_agent[d] = lessons
        errors.extend(errs)
        for w in warns:
            print(f"warning: {w}", file=sys.stderr)
    return per_agent, errors


def report_invalid(errors: list[tuple[Path, str]]) -> int:
    for path, msg in errors:
        print(f"INVALID {path}: {msg}", file=sys.stderr)
    print(f"distill.py: {len(errors)} invalid lesson file(s); nothing was written", file=sys.stderr)
    return EXIT_INVALID


def _one_line(s) -> str:
    return " ".join(str(s).split())


def index_line(lesson: Lesson, agent_dir: Path) -> str:
    m = lesson.meta
    rel = lesson.path.relative_to(agent_dir).as_posix()
    return (f"- [{m['stage']}] {_one_line(m['symptom'])} → {_one_line(m['fix'])} "
            f"(support {m['support']}, last {m['last_confirmed']}) [{rel}]")


def _fits(lines: list[str]) -> bool:
    text = "\n".join(lines) + "\n"
    return len(lines) <= INDEX_MAX_LINES and len(text.encode("utf-8")) <= INDEX_MAX_BYTES


def build_index(agent_name: str, lessons: list[Lesson], agent_dir: Path) -> tuple[str, int]:
    """Render MEMORY.md; returns (text, number of lessons indexed)."""
    ordered = sorted(lessons, key=lambda l: (-l.meta["support"], _date_desc(l.meta["last_confirmed"]), l.path.name))
    header = [f"# Lessons index: {agent_name}", INDEX_NOTE]
    entries = [index_line(l, agent_dir) for l in ordered]
    n = len(entries)
    k = n
    while k > 0:
        candidate = header + entries[:k] + ([OVERFLOW_LINE.format(k=n - k)] if k < n else [])
        if _fits(candidate):
            break
        k -= 1
    lines = header + entries[:k]
    if k < n:
        lines.append(OVERFLOW_LINE.format(k=n - k))
    return "\n".join(lines) + "\n", k


def rebuild_agent(agent_dir: Path, lessons: list[Lesson]) -> dict:
    kept, removed, changed = dedupe(lessons)
    for p in removed:
        p.unlink()
    for les in kept:
        if les.path in changed:
            write_lesson(les)
    text, indexed = build_index(agent_dir.name, kept, agent_dir)
    (agent_dir / "MEMORY.md").write_text(text, encoding="utf-8")
    return {"total": len(kept), "indexed": indexed, "merged": len(removed)}


def rebuild(root: Path, agent: str | None = None) -> int:
    if agent and not (root / agent).is_dir():
        print(f"distill.py: no agent directory {root / agent}", file=sys.stderr)
        return EXIT_ERROR
    per_agent, errors = validate_root(root, agent)
    if errors:
        return report_invalid(errors)
    if not per_agent:
        print(f"distill.py: no agent directories under {root}")
        return EXIT_OK
    for agent_dir, lessons in per_agent.items():
        st = rebuild_agent(agent_dir, lessons)
        print(f"rebuilt {agent_dir.name}: {st['indexed']}/{st['total']} lessons indexed, "
              f"{st['merged']} duplicate(s) merged -> {agent_dir / 'MEMORY.md'}")
    return EXIT_OK


# --------------------------------------------------------------------------- commands
def cmd_rebuild(args) -> int:
    return rebuild(resolve_root(args.root), args.agent)


def cmd_decay(args) -> int:
    root = resolve_root(args.root)
    today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()
    cutoff = today - dt.timedelta(days=args.stale_days)
    per_agent, errors = validate_root(root)
    if errors:
        return report_invalid(errors)
    moved = 0
    for agent_dir, lessons in per_agent.items():
        for les in lessons:
            if les.meta["support"] == 1 and dt.date.fromisoformat(les.meta["last_confirmed"]) < cutoff:
                archive = agent_dir / "archive"
                archive.mkdir(exist_ok=True)
                dest = unique_path(archive, les.path.stem)
                shutil.move(str(les.path), str(dest))
                print(f"archived {agent_dir.name}/lessons/{les.path.name} -> archive/{dest.name} "
                      f"(support 1, last {les.meta['last_confirmed']})")
                moved += 1
    print(f"decay: {moved} lesson(s) archived (last_confirmed before {cutoff.isoformat()}, support 1)")
    return rebuild(root)


def cmd_propose(args) -> int:
    root = resolve_root(args.root)
    if not root.is_dir():
        print(f"distill.py: memory root not found: {root}", file=sys.stderr)
        return EXIT_ERROR
    per_agent, errors = validate_root(root)
    if errors:
        return report_invalid(errors)
    cands = []
    for agent_dir, lessons in per_agent.items():
        for les in lessons:
            m = les.meta
            if m["generalizable"] is True and m["support"] >= args.min_support:
                target = TARGET_SKILL.get(m["stage"])
                cands.append({
                    "agent": agent_dir.name,
                    "file": les.path.relative_to(root).as_posix(),
                    "stage": m["stage"],
                    "blueprint": m["blueprint"],
                    "symptom": m["symptom"],
                    "root_cause": m["root_cause"],
                    "fix": m["fix"],
                    "support": m["support"],
                    "first_seen": m["first_seen"],
                    "last_confirmed": m["last_confirmed"],
                    "evidence": list(m["evidence"]),
                    "target_skill": target,
                    "target_skill_file": f"src/skills/{target}/SKILL.md" if target else None,
                })
    cands.sort(key=lambda c: (-c["support"], _date_desc(c["last_confirmed"]), c["agent"], c["file"]))
    out = Path(args.output) if args.output else root / "proposals.json"
    out.write_text(json.dumps({"generated": dt.date.today().isoformat(), "min_support": args.min_support,
                               "candidates": cands}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if not cands:
        print(f"no promotion candidates (generalizable lessons with support >= {args.min_support})")
    for c in cands:
        print(f"support {c['support']:>3}  [{c['stage']}] {_one_line(c['symptom'])} -> {_one_line(c['fix'])}"
              f"  => {c['target_skill_file']}  ({c['agent']}/{c['file']})")
    print(f"wrote {out} ({len(cands)} candidate(s))")
    return EXIT_OK


def _same_lineage(a: Lesson, b: Lesson) -> bool:
    ea, eb = set(a.meta["evidence"]), set(b.meta["evidence"])
    return ea >= eb or eb >= ea


def cmd_import(args) -> int:
    root = resolve_root(args.root)
    src = resolve_root(args.from_root)
    if not src.is_dir():
        print(f"distill.py: import source not found: {src}", file=sys.stderr)
        return EXIT_ERROR
    if src.resolve() == root.resolve():
        print("distill.py: import source and root are the same directory", file=sys.stderr)
        return EXIT_ERROR
    per_agent, errors = validate_root(root)
    if errors:
        return report_invalid(errors)
    central: dict[str, dict[tuple[str, str], Lesson]] = {
        d.name: {l.key: l for l in ls} for d, ls in per_agent.items()}
    added = merged = unchanged = skipped = 0
    for sdir in agent_dirs(src):
        name = sdir.name
        cdir = root / name
        (cdir / "lessons").mkdir(parents=True, exist_ok=True)
        cmap = central.setdefault(name, {})
        s_lessons, s_errors, _ = read_agent(sdir)
        for path, msg in s_errors:
            try:
                fixed, repairs = load_lesson_lenient(path)
            except (LessonError, Exception) as e:  # noqa: BLE001 - any parse failure means skip
                print(f"skipping invalid {path}: {msg} (repair failed: {e})", file=sys.stderr)
                skipped += 1
                continue
            print(f"repaired {path}: {'; '.join(repairs) or msg}", file=sys.stderr)
            s_lessons.append(fixed)
        for sl in s_lessons:
            cl = cmap.get(sl.key)
            if cl is None:
                dest = unique_path(cdir / "lessons", sl.path.stem)
                nl = Lesson(dest, dict(sl.meta), sl.body)
                write_lesson(nl)
                cmap[sl.key] = nl
                added += 1
                continue
            # A copy that descends from the central lesson (evidence superset/subset, e.g. a warm
            # sandbox) keeps the max support; an independent confirmation adds its support.
            result = merge_lessons(cl, sl, sum_support=not _same_lineage(cl, sl))
            if result.meta != cl.meta or result.body != cl.body:
                write_lesson(result)
                cmap[sl.key] = result
                merged += 1
            else:
                unchanged += 1
    print(f"import from {src}: {added} added, {merged} merged, {unchanged} unchanged, {skipped} skipped")
    return rebuild(root)


def cmd_new(args) -> int:
    root = resolve_root(args.root)
    agent_dir = root / args.agent
    today = args.date or dt.date.today().isoformat()
    meta = {
        "stage": args.stage,
        "blueprint": args.blueprint,
        "symptom": args.symptom,
        "root_cause": args.root_cause,
        "fix": args.fix,
        "evidence": list(args.evidence),
        "generalizable": bool(args.generalizable),
        "support": 1,
        "first_seen": today,
        "last_confirmed": today,
    }
    if args.tag:
        meta["tags"] = list(args.tag)
    errs = validate(meta, load_schema())
    if errs:
        for e in errs:
            print(f"INVALID lesson: {e}", file=sys.stderr)
        return EXIT_INVALID
    body = args.body if args.body is not None else DEFAULT_BODY
    if len(body.strip("\n").splitlines()) > BODY_MAX_LINES:
        print(f"distill.py: body must be at most {BODY_MAX_LINES} lines", file=sys.stderr)
        return EXIT_ERROR
    (agent_dir / "lessons").mkdir(parents=True, exist_ok=True)
    path = unique_path(agent_dir / "lessons", f"{args.stage}-{slugify(args.symptom)}")
    write_lesson(Lesson(path, meta, body))
    print(f"wrote {path}")
    return rebuild(root, args.agent)


# --------------------------------------------------------------------------- CLI
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="distill.py", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", metavar="command")
    sub.required = True

    def add_root(sp):
        sp.add_argument("--root", default=str(default_root()),
                        help="agent-memory root, or a config dir containing agent-memory/ (default: %(default)s)")

    sp = sub.add_parser("rebuild", help="validate, merge duplicates, rewrite MEMORY.md")
    add_root(sp)
    sp.add_argument("--agent", help="only this agent directory")
    sp.set_defaults(func=cmd_rebuild)

    sp = sub.add_parser("decay", help="archive support-1 lessons older than --stale-days, then rebuild")
    add_root(sp)
    sp.add_argument("--stale-days", type=int, default=90, help="days since last_confirmed (default: %(default)s)")
    sp.add_argument("--today", help="override today's date (YYYY-MM-DD), for tests")
    sp.set_defaults(func=cmd_decay)

    sp = sub.add_parser("propose", help="list promotion candidates and write proposals.json")
    add_root(sp)
    sp.add_argument("--min-support", type=int, default=3, help="minimum support (default: %(default)s)")
    sp.add_argument("--output", help="where to write proposals.json (default: <root>/proposals.json)")
    sp.set_defaults(func=cmd_propose)

    sp = sub.add_parser("import", help="merge lessons from another memory root, then rebuild")
    add_root(sp)
    sp.add_argument("--from", dest="from_root", required=True,
                    help="other agent-memory root (or a sandbox config dir containing agent-memory/)")
    sp.set_defaults(func=cmd_import)

    sp = sub.add_parser("new", help="write one schema-valid lesson file, then rebuild")
    add_root(sp)
    sp.add_argument("--agent", required=True, help="agent directory name, e.g. collider-simulator")
    sp.add_argument("--stage", required=True, choices=STAGES)
    sp.add_argument("--blueprint", default="none", help='blueprint id or "none" (default)')
    sp.add_argument("--symptom", required=True, help="what the tool result showed (<= 200 chars)")
    sp.add_argument("--root-cause", required=True, dest="root_cause")
    sp.add_argument("--fix", required=True)
    sp.add_argument("--evidence", action="append", required=True, metavar="E",
                    help="job id or progress file; repeat for more")
    sp.add_argument("--generalizable", action=argparse.BooleanOptionalAction, default=False,
                    help="mark as promotable (default: --no-generalizable)")
    sp.add_argument("--tag", action="append", help="optional tag; repeatable")
    sp.add_argument("--body", help="body text (<= 15 lines)")
    sp.add_argument("--date", help="override today's date (YYYY-MM-DD), for tests")
    sp.set_defaults(func=cmd_new)
    return p


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] in ("--rebuild", "--decay", "--propose", "--import", "--new"):
        argv[0] = argv[0][2:]
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
