#!/usr/bin/env python3
"""
diff-shadow.py · ANTS SAKM v2 weekly diff runner
================================================

Owner: HoEng #21 + #63 FJA-CDCA · v1.0 · 2026-04-27 K.15

Purpose: For each registered shadow, compute the diff between Master spec and
         shadow's current state. Write per-shadow diff reports + update the
         registry's divergence_status. Run weekly (Mon 09:00 ICT) via #63 cron.

Philosophy:
    Federated wisdom is real authority — but the registry is the ledger.
    Collective intelligence is the write-back loop — drift is its enemy.

Usage:
    python3 diff-shadow.py                    # full sweep · all shadows
    python3 diff-shadow.py --shadow {id}      # single shadow
    python3 diff-shadow.py --dry-run          # report only · no registry update
    python3 diff-shadow.py --strict           # exit 1 if ANY shadow >= yellow

Exit codes:
    0 = all shadows green
    1 = at least one yellow_warning
    2 = at least one red_blocker
    3 = registry/script error

Idempotent: safe to re-run · only writes if state changed.
"""

from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import sys
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Any

# ----------------------------------------------------------------------
# Config — paths are relative to repo root
# ----------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent.parent  # /sakm/git-blueprint/scripts → repo root
REGISTRY_PATH = REPO_ROOT / "sakm" / "registry" / "shadow-agents.json"
DIFFS_DIR = REPO_ROOT / "sakm" / "registry" / "diffs"
AGENTS_DIR = REPO_ROOT / "sakm" / "agents"  # in real repo this would be /agents/

DEFAULT_THRESHOLDS = {
    "warning_days": 14,
    "blocker_days": 30,
    "blocker_section_count": 3,
}

# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------


def load_registry() -> dict[str, Any]:
    if not REGISTRY_PATH.exists():
        die(f"Registry not found: {REGISTRY_PATH}", 3)
    with open(REGISTRY_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def save_registry(reg: dict[str, Any], dry_run: bool) -> None:
    if dry_run:
        print("[dry-run] registry write SKIPPED")
        return
    reg["_meta"]["last_updated"] = date.today().isoformat()
    reg["_meta"]["last_full_sweep"] = date.today().isoformat()
    with open(REGISTRY_PATH, "w", encoding="utf-8") as fh:
        json.dump(reg, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"[ok] registry updated → {REGISTRY_PATH}")


def die(msg: str, code: int) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def parse_date(s: str | None) -> date | None:
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        return None


def days_since(d: date | None) -> int:
    if d is None:
        return 9999
    return (date.today() - d).days


# ----------------------------------------------------------------------
# Diff engine
# ----------------------------------------------------------------------


def section_split(text: str) -> dict[str, str]:
    """Split markdown into sections by headings (## or ###)."""
    sections: dict[str, str] = {}
    current_key = "_preamble"
    buf: list[str] = []
    for line in text.splitlines():
        if re.match(r"^#{2,3}\s+", line):
            if buf:
                sections[current_key] = "\n".join(buf).strip()
            current_key = line.strip()
            buf = []
        else:
            buf.append(line)
    if buf:
        sections[current_key] = "\n".join(buf).strip()
    return sections


def compute_diff(master_path: Path, shadow_path: Path) -> dict[str, Any]:
    """Return structured diff result."""
    if not master_path.exists():
        return {"error": f"master missing: {master_path}", "diff_score": 1.0}
    if not shadow_path.exists():
        return {"error": f"shadow missing: {shadow_path}", "diff_score": 1.0}

    master_text = master_path.read_text(encoding="utf-8")
    shadow_text = shadow_path.read_text(encoding="utf-8")

    master_sections = section_split(master_text)
    shadow_sections = section_split(shadow_text)

    all_keys = set(master_sections) | set(shadow_sections)
    sections_changed: list[str] = []
    for key in all_keys:
        if master_sections.get(key, "") != shadow_sections.get(key, ""):
            sections_changed.append(key)

    # Line-level similarity ratio (0 = identical · 1 = total divergence)
    sim = difflib.SequenceMatcher(None, master_text, shadow_text).ratio()
    diff_score = round(1.0 - sim, 4)

    # Unified diff for the human report
    unified = list(
        difflib.unified_diff(
            master_text.splitlines(),
            shadow_text.splitlines(),
            fromfile="master",
            tofile="shadow",
            lineterm="",
        )
    )
    lines_changed = sum(1 for ln in unified if ln.startswith(("+", "-")) and not ln.startswith(("+++", "---")))

    return {
        "diff_score": diff_score,
        "sections_changed": len(sections_changed),
        "section_keys_changed": sections_changed,
        "lines_changed": lines_changed,
        "unified_diff": "\n".join(unified[:500]),  # cap to keep report sane
    }


def classify(diff_result: dict[str, Any], last_sync: date | None, thresholds: dict[str, int]) -> str:
    """Return divergence_status: green | yellow_warning | red_blocker."""
    if "error" in diff_result:
        return "red_blocker"
    days = days_since(last_sync)
    sec = diff_result.get("sections_changed", 0)

    if days >= thresholds["blocker_days"] or sec >= thresholds["blocker_section_count"]:
        return "red_blocker"
    if days >= thresholds["warning_days"] or sec >= 1:
        return "yellow_warning"
    return "green"


# ----------------------------------------------------------------------
# Report writers
# ----------------------------------------------------------------------


def write_diff_reports(shadow_id: str, diff_result: dict[str, Any], target_date: date) -> tuple[Path, Path]:
    out_dir = DIFFS_DIR / target_date.isoformat()
    out_dir.mkdir(parents=True, exist_ok=True)

    json_path = out_dir / f"{shadow_id}.diff.json"
    md_path = out_dir / f"{shadow_id}.diff.md"

    json_path.write_text(json.dumps(diff_result, indent=2, ensure_ascii=False), encoding="utf-8")

    md_lines = [
        f"# Diff Report · {shadow_id}",
        f"_Run date: {target_date.isoformat()}_",
        "",
        f"- diff_score: **{diff_result.get('diff_score')}** (0 = identical · 1 = total divergence)",
        f"- sections_changed: **{diff_result.get('sections_changed')}**",
        f"- lines_changed: **{diff_result.get('lines_changed')}**",
        "",
        "## Sections changed",
        "",
    ]
    for k in diff_result.get("section_keys_changed", []):
        md_lines.append(f"- `{k}`")
    md_lines.extend(["", "## Unified diff (first 500 lines)", "", "```diff", diff_result.get("unified_diff", ""), "```"])
    md_path.write_text("\n".join(md_lines), encoding="utf-8")
    return json_path, md_path


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------


def process_shadow(shadow: dict[str, Any], args: argparse.Namespace) -> tuple[str, str]:
    """Process one shadow · return (shadow_id, divergence_status)."""
    sid = shadow.get("shadow_id", "unknown")
    agent_id = shadow.get("agent_id", "unknown")

    # Skip placeholder/pending records
    if shadow.get("status") == "pending_signature":
        print(f"[skip] {sid} · status=pending_signature")
        return sid, "green"

    master_path = AGENTS_DIR / agent_id / "master.md"
    shadow_holder_slug = re.sub(r"[^a-z0-9]+", "_", shadow.get("exported_to", {}).get("holder_name", "unknown").lower())
    shadow_path = AGENTS_DIR / agent_id / "shadows" / f"{shadow_holder_slug}.current.md"

    diff_result = compute_diff(master_path, shadow_path)
    last_sync = parse_date(shadow.get("last_sync_date"))
    status = classify(diff_result, last_sync, DEFAULT_THRESHOLDS)

    if not args.dry_run and "error" not in diff_result:
        json_path, md_path = write_diff_reports(sid, diff_result, date.today())
        shadow["last_diff"] = {
            "run_date": date.today().isoformat(),
            "diff_score": diff_result.get("diff_score"),
            "sections_changed": diff_result.get("sections_changed"),
            "lines_changed": diff_result.get("lines_changed"),
            "report_path": str(md_path.relative_to(REPO_ROOT)),
        }
    shadow["divergence_status"] = status

    icon = {"green": "🟢", "yellow_warning": "🟡", "red_blocker": "🔴"}[status]
    print(f"  {icon} {sid} · status={status} · diff_score={diff_result.get('diff_score')}")
    return sid, status


def main() -> int:
    parser = argparse.ArgumentParser(description="ANTS SAKM v2 weekly diff runner")
    parser.add_argument("--shadow", help="single shadow_id (default: all)")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--strict", action="store_true", help="exit 1 if any shadow != green")
    args = parser.parse_args()

    reg = load_registry()
    shadows = reg.get("shadows", [])
    if args.shadow:
        shadows = [s for s in shadows if s.get("shadow_id") == args.shadow]
        if not shadows:
            die(f"shadow_id not found: {args.shadow}", 3)

    print(f"=== diff-shadow.py · {date.today().isoformat()} · {len(shadows)} shadow(s) ===")
    statuses: list[str] = []
    for shadow in shadows:
        _, st = process_shadow(shadow, args)
        statuses.append(st)

    save_registry(reg, args.dry_run)

    print("\n=== Summary ===")
    print(f"  green: {statuses.count('green')}")
    print(f"  yellow_warning: {statuses.count('yellow_warning')}")
    print(f"  red_blocker: {statuses.count('red_blocker')}")

    if args.strict:
        if "red_blocker" in statuses:
            return 2
        if "yellow_warning" in statuses:
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
