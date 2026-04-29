#!/usr/bin/env python3
"""
merge-ceremony.py · ANTS SAKM v2 monthly merge ceremony runner
==============================================================

Owner: KM #51 (Layer-1) + เฌอคูณ CWO (Layer-2) · v1.0 · 2026-04-27 K.15

Purpose: Run a structured merge ceremony for one shadow. Reviews pending
         write-back proposals, lets the human ceremony pair (Nut + shadow_holder)
         decide merge/split/preserve, and writes an audit-trail decision log.

Philosophy:
    Collective intelligence requires ceremony. The script does NOT auto-merge;
    it organizes the diff, enumerates options, and captures human judgment.

Usage:
    python3 merge-ceremony.py --shadow {shadow_id}                # interactive
    python3 merge-ceremony.py --shadow {shadow_id} --plan {file}  # batch from a YAML plan
    python3 merge-ceremony.py --list-pending                      # what needs ceremony

Exit codes:
    0 = ceremony complete · all decisions captured
    1 = aborted by operator
    2 = no pending write-backs for shadow
    3 = registry/script error
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent.parent
REGISTRY_PATH = REPO_ROOT / "sakm" / "registry" / "shadow-agents.json"
CEREMONIES_DIR = REPO_ROOT / "sakm" / "ceremonies"
AGENTS_DIR = REPO_ROOT / "sakm" / "agents"


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------


def load_registry() -> dict[str, Any]:
    if not REGISTRY_PATH.exists():
        die(f"Registry not found: {REGISTRY_PATH}", 3)
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def save_registry(reg: dict[str, Any]) -> None:
    reg["_meta"]["last_updated"] = date.today().isoformat()
    REGISTRY_PATH.write_text(json.dumps(reg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def die(msg: str, code: int) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def list_pending_writebacks(shadow: dict[str, Any]) -> list[dict[str, Any]]:
    return [wb for wb in shadow.get("write_backs", []) if not wb.get("merged")]


def find_shadow(reg: dict[str, Any], sid: str) -> dict[str, Any]:
    for s in reg.get("shadows", []):
        if s.get("shadow_id") == sid:
            return s
    die(f"shadow_id not found: {sid}", 3)
    return {}  # unreachable


# ----------------------------------------------------------------------
# Ceremony workflow
# ----------------------------------------------------------------------


CEREMONY_AGENDA = """\
# Merge Ceremony Agenda · {shadow_id}

**Date:** {today}
**Participants:** Nut · Shadow holder · KM #51
**Layer-2 sign-off:** เฌอคูณ (CWO)

## Order
1. **Read** the unified diff (last `diff-shadow.py` report)
2. **Review** every pending write-back proposal (one by one)
3. **Decide** for each: `merge_into_master` · `keep_local_only` · `split_into_new_agent` · `defer_next_ceremony`
4. **Log** decision + rationale (for federated wisdom audit trail)
5. **ARAI** block (Actions · Results · Idea Improvements)

## Decision categories (per Boundary Contract)

- **Master wins** when: V/M language · Op Principles · Hot Rules · canonical agent count · core framework
- **Shadow wins** when: holder-jurisdiction specifics · client-specific case history · vendor-specific tactics
- **Unresolved → Nut** (human-in-the-loop)

## Pending write-backs

{pending_block}
"""


def write_agenda(shadow: dict[str, Any], pending: list[dict[str, Any]]) -> Path:
    sid = shadow["shadow_id"]
    today = date.today().isoformat()
    out_dir = CEREMONIES_DIR / f"{today}__{sid}"
    out_dir.mkdir(parents=True, exist_ok=True)
    pending_block = "\n".join(
        f"### Write-back #{i + 1} · {wb.get('date')} · `{wb.get('section_path', 'n/a')}`\n\n> {wb.get('summary', '')}\n"
        for i, wb in enumerate(pending)
    ) or "_(none — ceremony for routine sync only)_"
    agenda_text = CEREMONY_AGENDA.format(shadow_id=sid, today=today, pending_block=pending_block)
    agenda_path = out_dir / "agenda.md"
    agenda_path.write_text(agenda_text, encoding="utf-8")
    return agenda_path


def prompt_decision(wb: dict[str, Any]) -> tuple[str, str]:
    print(f"\n--- Write-back · {wb.get('date')} · {wb.get('section_path', '?')} ---")
    print(f"Summary: {wb.get('summary', '')[:300]}")
    print("\nOptions:")
    print("  1) merge_into_master")
    print("  2) keep_local_only")
    print("  3) split_into_new_agent")
    print("  4) defer_next_ceremony")
    while True:
        choice = input("Decision [1-4]: ").strip()
        if choice in {"1", "2", "3", "4"}:
            break
    decision_map = {
        "1": "merge_into_master",
        "2": "keep_local_only",
        "3": "split_into_new_agent",
        "4": "defer_next_ceremony",
    }
    rationale = input("Rationale (one line): ").strip()
    return decision_map[choice], rationale


def write_decisions_log(shadow: dict[str, Any], decisions: list[dict[str, Any]]) -> Path:
    sid = shadow["shadow_id"]
    today = date.today().isoformat()
    out_dir = CEREMONIES_DIR / f"{today}__{sid}"
    out_dir.mkdir(parents=True, exist_ok=True)
    log_path = out_dir / "decisions.md"

    lines = [
        f"# Merge Ceremony Decisions · {sid}",
        f"_Date: {today}_",
        "",
        "| # | Date | Section | Decision | Rationale |",
        "|---|---|---|---|---|",
    ]
    for i, d in enumerate(decisions, start=1):
        lines.append(
            f"| {i} | {d['date']} | `{d['section_path']}` | **{d['decision']}** | {d['rationale']} |"
        )
    lines.extend(
        [
            "",
            "## ARAI block",
            "",
            "**Actions:** apply merge decisions to master.md · update registry · notify shadow holder",
            "**Results:** TBD · re-run diff next Monday to confirm convergence",
            "**Idea Improvements:** _capture during ceremony · move to /reports/ if generalizable_",
        ]
    )
    log_path.write_text("\n".join(lines), encoding="utf-8")
    return log_path


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description="ANTS SAKM v2 merge ceremony runner")
    parser.add_argument("--shadow", help="shadow_id to run ceremony for")
    parser.add_argument("--list-pending", action="store_true")
    args = parser.parse_args()

    reg = load_registry()

    if args.list_pending:
        print("=== Shadows with pending write-backs ===")
        for s in reg.get("shadows", []):
            pending = list_pending_writebacks(s)
            if pending:
                print(f"  {s['shadow_id']} · {len(pending)} pending")
        return 0

    if not args.shadow:
        die("--shadow {shadow_id} required (or use --list-pending)", 3)

    shadow = find_shadow(reg, args.shadow)
    pending = list_pending_writebacks(shadow)

    if not pending:
        print(f"[ok] {args.shadow} has no pending write-backs · routine sync only")
        agenda_path = write_agenda(shadow, [])
        print(f"  agenda → {agenda_path}")
        return 2

    agenda_path = write_agenda(shadow, pending)
    print(f"[start] ceremony agenda → {agenda_path}")
    print(f"[info] {len(pending)} pending write-back(s) to review")

    decisions: list[dict[str, Any]] = []
    for wb in pending:
        decision, rationale = prompt_decision(wb)
        wb["merged"] = decision == "merge_into_master"
        wb["merge_decision_by"] = "ceremony_pair"
        decisions.append(
            {
                "date": wb.get("date", "n/a"),
                "section_path": wb.get("section_path", "n/a"),
                "decision": decision,
                "rationale": rationale,
            }
        )

    log_path = write_decisions_log(shadow, decisions)
    save_registry(reg)
    print(f"\n[done] decisions → {log_path}")
    print(f"[done] registry updated → {REGISTRY_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
