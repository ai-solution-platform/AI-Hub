#!/usr/bin/env python3
"""
lint-orchestrator.py — Run all ANTS 2.0 lint gates in one shot · I-NEW-31 · K.23

Replaces the 6-command Friday Push pre-flight with a single command:
  python3 scripts/lint-orchestrator.py

Runs (in this order):
  1. DAS canonical sweep        (vm-canonical-lint.py)
  2. Hub-Index sync check        (hub-index-sync-check.py)
  3. Hub-Index visual regression (hub-index-visual-test.py)
  4. Workshop output registry    (workshop-output-registry.py)
  5. I-NEW status tracker        (i-new-status-tracker.py)
  6. Memory consolidation        (memory-consolidate.py · advisory only)

Exit codes:
  0  → all gates PASS (P1 advisory OK)
  1  → at least one gate FAILED (P0 found)
  2  → script crashed before/while running

Usage:
  python3 lint-orchestrator.py                # human-readable summary
  python3 lint-orchestrator.py --json         # JSON to stdout
  python3 lint-orchestrator.py --strict       # exit 1 even on P1 (Friday Push gate)
  python3 lint-orchestrator.py --skip memory  # skip specific gate(s)
  python3 lint-orchestrator.py --memory-dir <path>  # for memory-consolidate

Owner: HoEng #21 + Senior SDET #31 + #63 FJA-CDCA Target #15 (I-NEW-31)
"""

import argparse
import json
import re
import subprocess
import sys
import time
from datetime import date
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
SCRIPTS = WORKSPACE / "scripts"
REPORTS_DIR = WORKSPACE / "reports"

# ANSI
G = "\033[32m"
R = "\033[31m"
Y = "\033[33m"
B = "\033[34m"
DIM = "\033[2m"
N = "\033[0m"

GATES = [
    {
        "id": "das",
        "name": "DAS canonical sweep",
        "script": "vm-canonical-lint.py",
        "args": [],
        "p0_pattern": r"P0=(\d+)",
        "clean_pattern": r"ALL CLEAN",
    },
    {
        "id": "hub-sync",
        "name": "Hub-Index sync check",
        "script": "hub-index-sync-check.py",
        "args": [],
        "p0_pattern": r"FAIL|FAIL!|❌",
        "clean_pattern": r"ALL CLEAN",
    },
    {
        "id": "hub-visual",
        "name": "Hub-Index visual regression",
        "script": "hub-index-visual-test.py",
        "args": [],
        "p0_pattern": r"failure",
        "clean_pattern": r"ALL CLEAN",
    },
    {
        "id": "workshop",
        "name": "Workshop output registry",
        "script": "workshop-output-registry.py",
        "args": ["--no-report"],
        "p0_pattern": r"P0=(\d+)",
        "clean_pattern": r"All checks pass",
    },
    {
        "id": "inew",
        "name": "I-NEW status tracker",
        "script": "i-new-status-tracker.py",
        "args": ["--no-report"],
        "p0_pattern": r"P0=(\d+)",
        "clean_pattern": r"All checks pass",
    },
    {
        "id": "memory",
        "name": "Memory consolidation",
        "script": "memory-consolidate.py",
        "args": ["--no-report"],
        "p0_pattern": r"_will_never_match_",
        "clean_pattern": r"All clean",
        "advisory_only": True,
        "needs_memory_dir": True,
    },
]


def strip_ansi(s: str) -> str:
    return re.sub(r"\x1b\[[0-9;]*m", "", s)


def run_gate(gate: dict, memory_dir: str = None, timeout: float = 60.0) -> dict:
    script_path = SCRIPTS / gate["script"]
    if not script_path.exists():
        return {
            "id": gate["id"],
            "name": gate["name"],
            "status": "MISSING",
            "elapsed_sec": 0,
            "p0_count": 0,
            "advisory_only": gate.get("advisory_only", False),
            "summary": f"Script not found: {script_path}",
        }
    args = list(gate["args"])
    if gate.get("needs_memory_dir") and memory_dir:
        args = ["--memory-dir", memory_dir] + args
    start = time.time()
    try:
        result = subprocess.run(
            ["python3", str(script_path), *args],
            capture_output=True, text=True, timeout=timeout,
        )
        elapsed = time.time() - start
        out = strip_ansi(result.stdout + result.stderr)
        # Parse P0 count
        p0_count = 0
        m = re.search(gate["p0_pattern"], out)
        if m and m.groups():
            try:
                p0_count = int(m.group(1))
            except ValueError:
                p0_count = 1 if m.group(0) else 0
        elif m:
            p0_count = 1  # boolean match (FAIL keyword)
        clean_match = re.search(gate["clean_pattern"], out, re.IGNORECASE)
        if clean_match and p0_count == 0:
            status = "PASS"
        elif gate.get("advisory_only"):
            status = "ADVISORY"
        elif p0_count > 0:
            status = "FAIL"
        elif result.returncode != 0:
            status = "ERROR"
        else:
            status = "PASS"
        # Extract last meaningful line
        last_lines = [ln for ln in out.strip().splitlines() if ln.strip()][-3:]
        return {
            "id": gate["id"],
            "name": gate["name"],
            "status": status,
            "elapsed_sec": round(elapsed, 2),
            "p0_count": p0_count,
            "advisory_only": gate.get("advisory_only", False),
            "summary": " · ".join(last_lines)[:200],
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {
            "id": gate["id"],
            "name": gate["name"],
            "status": "TIMEOUT",
            "elapsed_sec": timeout,
            "p0_count": 0,
            "summary": f"Timed out after {timeout}s",
            "advisory_only": gate.get("advisory_only", False),
        }
    except Exception as e:
        return {
            "id": gate["id"],
            "name": gate["name"],
            "status": "ERROR",
            "elapsed_sec": round(time.time() - start, 2),
            "p0_count": 0,
            "summary": str(e),
            "advisory_only": gate.get("advisory_only", False),
        }


def main():
    p = argparse.ArgumentParser(description="Lint orchestrator · I-NEW-31 · K.23")
    p.add_argument("--json", action="store_true")
    p.add_argument("--strict", action="store_true",
                   help="Exit 1 even on advisory findings (Friday Push gate)")
    p.add_argument("--skip", nargs="*", default=[],
                   help="Gate IDs to skip (das, hub-sync, hub-visual, workshop, inew, memory)")
    p.add_argument("--memory-dir", default=None,
                   help="Memory directory for memory-consolidate")
    p.add_argument("--timeout", type=float, default=60.0)
    p.add_argument("--no-report", action="store_true")
    args = p.parse_args()

    skip_set = set(args.skip)
    gates_to_run = [g for g in GATES if g["id"] not in skip_set]

    # Auto-detect memory dir if not provided
    memory_dir = args.memory_dir
    if not memory_dir:
        candidates = [
            "/sessions/stoic-friendly-allen/mnt/.auto-memory",
            str(Path.home() / "Library/Application Support/Claude/local-agent-mode-sessions"),
        ]
        for c in candidates:
            if Path(c).exists():
                memory_dir = c
                break

    results = []
    if not args.json:
        print(f"{B}🚀 Lint Orchestrator · {date.today()}{N}")
        print(f"   {DIM}Running {len(gates_to_run)} gate(s) sequentially{N}\n")

    for gate in gates_to_run:
        if not args.json:
            print(f"   {DIM}→ {gate['name']}...{N}", end="", flush=True)
        r = run_gate(gate, memory_dir=memory_dir, timeout=args.timeout)
        results.append(r)
        if not args.json:
            badge = {
                "PASS": f"{G}✅ PASS{N}",
                "FAIL": f"{R}❌ FAIL{N}",
                "ADVISORY": f"{Y}🟡 ADVISORY{N}",
                "MISSING": f"{R}❌ MISSING{N}",
                "ERROR": f"{R}❌ ERROR{N}",
                "TIMEOUT": f"{R}⏱  TIMEOUT{N}",
            }.get(r["status"], r["status"])
            print(f" {badge} {DIM}({r['elapsed_sec']}s){N}")

    # Summary
    pass_count = sum(1 for r in results if r["status"] == "PASS")
    fail_count = sum(1 for r in results if r["status"] in ("FAIL", "MISSING", "ERROR", "TIMEOUT"))
    advisory_count = sum(1 for r in results if r["status"] == "ADVISORY")

    report = {
        "schema": "lint-orchestrator-v1",
        "date": date.today().isoformat(),
        "totals": {
            "pass": pass_count,
            "fail": fail_count,
            "advisory": advisory_count,
            "total": len(results),
        },
        "results": results,
    }

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print()
        if fail_count == 0 and advisory_count == 0:
            print(f"{G}✅ ALL {pass_count} GATES PASS · zero defects · zero advisories{N}")
        elif fail_count == 0:
            print(f"{G}✅ {pass_count} PASS{N} · {Y}{advisory_count} advisory{N}")
        else:
            print(f"{R}❌ {fail_count} FAIL{N} · {G}{pass_count} PASS{N} · {Y}{advisory_count} advisory{N}")
            for r in results:
                if r["status"] not in ("PASS", "ADVISORY"):
                    print(f"   {R}↳ {r['name']}: {r['summary']}{N}")

    if not args.no_report:
        try:
            REPORTS_DIR.mkdir(parents=True, exist_ok=True)
            json_out = REPORTS_DIR / f"Lint-Orchestrator-Report-{date.today()}.json"
            json_out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
            if not args.json:
                print(f"\n{DIM}📝 Report: {json_out.relative_to(WORKSPACE)}{N}")
        except Exception as e:
            print(f"⚠️  Could not write report: {e}", file=sys.stderr)

    # Exit code
    if fail_count > 0:
        sys.exit(1)
    if args.strict and advisory_count > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
