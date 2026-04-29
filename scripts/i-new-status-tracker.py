#!/usr/bin/env python3
"""
i-new-status-tracker.py — I-NEW Status Board · I-NEW-30 · K.23

Reads /canonical/i-new-status.json (SSOT) and verifies each I-NEW item:
  - SHIPPED: artifact path exists in workspace
  - STUB: artifact path exists (skeleton)
  - SPEC / DEFERRED: no artifact required
  - MAC: artifact exists (Mac script ready)
  - GAP: no validation (placeholder)

Detects mismatches:
  - SHIPPED but artifact missing → P0
  - SHIPPED but artifact empty (0 bytes) → P0
  - state=DEFERRED but artifact exists → P1 (wisdom flag · should not have been built)
  - totals_self_reported != actual count by state → P1

Output: human-readable status table + JSON report.
Owner: #63 FJA-CDCA Target #14 + #51 KM · weekly cron Mondays 09:30 ICT.

Usage:
  python3 i-new-status-tracker.py              # full report
  python3 i-new-status-tracker.py --json       # JSON to stdout only
  python3 i-new-status-tracker.py --strict     # exit 1 on any mismatch
  python3 i-new-status-tracker.py --state SHIPPED   # filter by state
"""

import argparse
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
SSOT = WORKSPACE / "canonical" / "i-new-status.json"
REPORTS_DIR = WORKSPACE / "reports"

# ANSI colors
G = "\033[32m"
R = "\033[31m"
Y = "\033[33m"
B = "\033[34m"
DIM = "\033[2m"
N = "\033[0m"

STATE_BADGES = {
    "SHIPPED": f"{G}✅ SHIPPED{N}",
    "STUB": f"{Y}🟡 STUB{N}",
    "SPEC": f"{Y}🟡 SPEC{N}",
    "DEFERRED": f"{B}⏸  DEFERRED{N}",
    "MAC": f"{B}🔵 MAC{N}",
    "GAP": f"{DIM}⚪ GAP{N}",
}


def load_ssot() -> dict:
    if not SSOT.exists():
        print(f"{R}❌ SSOT not found: {SSOT}{N}", file=sys.stderr)
        sys.exit(2)
    return json.loads(SSOT.read_text(encoding="utf-8"))


def verify_artifact(artifact_str: str) -> dict:
    """Parse an artifact field and verify file existence.

    Handles:
      - Single path: "scripts/foo.py"
      - Multi-path: "scripts/foo.py + scripts/bar.json"
      - Path with annotation: "scripts/foo.py (function bar)"
    """
    if not artifact_str:
        return {"missing": [], "empty": [], "ok": []}
    # Strip parenthetical annotations
    cleaned = re.sub(r"\s*\([^)]+\)", "", artifact_str)
    paths = [p.strip() for p in cleaned.split("+")]
    missing, empty, ok = [], [], []
    for p in paths:
        if not p:
            continue
        full = WORKSPACE / p.lstrip("/")
        if not full.exists():
            missing.append(p)
        elif full.is_file() and full.stat().st_size == 0:
            empty.append(p)
        else:
            ok.append(p)
    return {"missing": missing, "empty": empty, "ok": ok}


def main():
    p = argparse.ArgumentParser(description="I-NEW Status Tracker · I-NEW-30 · K.23")
    p.add_argument("--json", action="store_true", help="JSON output to stdout")
    p.add_argument("--strict", action="store_true", help="exit 1 on any mismatch")
    p.add_argument("--state", help="filter by state (SHIPPED/STUB/SPEC/MAC/DEFERRED/GAP)")
    p.add_argument("--no-report", action="store_true", help="skip writing report file")
    args = p.parse_args()

    ssot = load_ssot()
    items = ssot.get("items", [])
    self_reported = ssot.get("totals_self_reported", {})

    # Per-item verification
    findings = []
    enriched = []
    for item in items:
        state = item.get("state", "?")
        eid = item.get("id", "?")
        name = item.get("name", "")
        artifact = item.get("artifact", "")

        v = verify_artifact(artifact)
        verdict = "ok"

        if state in ("SHIPPED", "STUB", "MAC"):
            if v["missing"]:
                verdict = "missing"
                findings.append({
                    "id": eid,
                    "severity": "P0",
                    "category": "artifact_missing",
                    "message": f"I-NEW-{eid} state={state} but artifact NOT FOUND: {v['missing']}",
                })
            elif v["empty"]:
                verdict = "empty"
                findings.append({
                    "id": eid,
                    "severity": "P0",
                    "category": "artifact_empty",
                    "message": f"I-NEW-{eid} state={state} but artifact is EMPTY (0 bytes): {v['empty']}",
                })

        elif state == "DEFERRED":
            if v["ok"]:
                verdict = "wisdom_violation"
                findings.append({
                    "id": eid,
                    "severity": "P1",
                    "category": "deferred_built_anyway",
                    "message": f"I-NEW-{eid} state=DEFERRED but artifact EXISTS — Op 14 wisdom flag · check ownership",
                })

        enriched.append({**item, "_verdict": verdict, "_artifact_check": v})

    # Aggregate counts
    actual = Counter(i.get("state", "?") for i in items)
    actual_dict = dict(actual)

    # Map keys to self_reported convention
    map_key = {
        "SHIPPED": "shipped",
        "STUB": "stub",
        "SPEC": "spec_only",
        "DEFERRED": "deferred",
        "MAC": "awaiting_mac",
        "GAP": "gap",
    }
    expected_total = self_reported.get("total_known", len(items))
    if expected_total != len(items):
        findings.append({
            "id": "_meta",
            "severity": "P1",
            "category": "total_mismatch",
            "message": f"total_known={expected_total} but items array has {len(items)}",
        })
    for state_name, key in map_key.items():
        expected = self_reported.get(key, 0)
        got = actual_dict.get(state_name, 0)
        if expected != got:
            findings.append({
                "id": "_meta",
                "severity": "P1",
                "category": "self_reported_drift",
                "message": f"self_reported.{key}={expected} but actual {state_name}={got}",
            })

    # Filter (optional)
    display = enriched
    if args.state:
        display = [i for i in enriched if i.get("state") == args.state.upper()]

    report = {
        "schema": "i-new-status-tracker-v1",
        "date": date.today().isoformat(),
        "ssot_version": ssot.get("_meta", {}).get("version"),
        "totals_actual": actual_dict,
        "totals_self_reported": self_reported,
        "total_items": len(items),
        "findings": findings,
        "items": enriched,
    }

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        # Human-readable table
        print(f"{B}📊 I-NEW Status Board{N} · {date.today()} · SSOT v{ssot.get('_meta', {}).get('version', '?')}\n")
        # Header counts
        cnt_str = " · ".join(f"{STATE_BADGES.get(s, s)} {actual_dict.get(s, 0)}" for s in
                             ["SHIPPED", "STUB", "SPEC", "DEFERRED", "MAC", "GAP"]
                             if s in actual_dict)
        print(f"   {cnt_str}\n")
        print(f"   {DIM}Total: {len(items)} I-NEW items tracked{N}\n")

        # Per-item rows
        for item in display:
            state = item.get("state", "?")
            eid = item.get("id", "?")
            name = item.get("name", "")
            verdict = item.get("_verdict", "ok")
            badge = STATE_BADGES.get(state, state)
            mark = ""
            if verdict == "missing":
                mark = f" {R}[MISSING]{N}"
            elif verdict == "empty":
                mark = f" {R}[EMPTY]{N}"
            elif verdict == "wisdom_violation":
                mark = f" {Y}[OP14 FLAG]{N}"
            shipped_k = item.get("shipped_k", "")
            shipped_part = f" {DIM}[{shipped_k}]{N}" if shipped_k else ""
            print(f"   I-NEW-{str(eid).rjust(4)}  {badge:<28} {name[:60]}{shipped_part}{mark}")

        # Findings summary
        print()
        if not findings:
            print(f"{G}✅ All checks pass · zero drift between SSOT and workspace{N}")
        else:
            p0 = [f for f in findings if f.get("severity") == "P0"]
            p1 = [f for f in findings if f.get("severity") == "P1"]
            print(f"{R}P0={len(p0)}{N} · {Y}P1={len(p1)}{N}")
            for f in findings:
                sev = f.get("severity", "P1")
                tag = f"{R}🔴" if sev == "P0" else f"{Y}🟡"
                print(f"   {tag} [{sev}] I-NEW-{f.get('id')} {f.get('message')}{N}")

    # Write report
    if not args.no_report:
        try:
            REPORTS_DIR.mkdir(parents=True, exist_ok=True)
            json_out = REPORTS_DIR / f"I-NEW-Status-Report-{date.today()}.json"
            json_out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
            if not args.json:
                print(f"\n{DIM}📝 Report: {json_out.relative_to(WORKSPACE)}{N}")
        except Exception as e:
            print(f"⚠️  Could not write report: {e}", file=sys.stderr)

    if args.strict and findings:
        sys.exit(1)


if __name__ == "__main__":
    main()
