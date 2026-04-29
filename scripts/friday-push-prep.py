#!/usr/bin/env python3
"""
friday-push-prep.py — Friday Push Ritual automation companion · I-NEW-32 · K.23

Automates Steps 1+2+4 of docs/friday-push-ritual.md (Step 3 = git push remains
manual Mac terminal because sandbox cannot push). Run before paste of
publish-to-github.sh to pre-validate Friday Push readiness.

Steps:
  Step 1 · Lint orchestrator (--strict for Friday gate · zero advisory tolerance)
  Step 2 · Hub-Index sync check (already covered in orchestrator · re-run for sanity)
  [Step 3 · Manual Mac paste of ./scripts/publish-to-github.sh — NOT automated]
  Step 4 · Optionally: HEAD check live Hub-Index URL (post-push verification)

Output: 1-line Stop Tape format ready to paste in conversation.

Usage:
  python3 friday-push-prep.py                  # pre-push checks
  python3 friday-push-prep.py --post-push      # Step 4 only · verify URL HTTP 200
  python3 friday-push-prep.py --kref K.23      # for Stop Tape labelling
  python3 friday-push-prep.py --json

Owner: EA #40 (calendar) + CCVO #52 (discipline) + #63 FJA-CDCA Target #16 (I-NEW-32)
"""

import argparse
import json
import re
import subprocess
import sys
import time
import urllib.request
from datetime import date
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
HUB_INDEX_URL = "https://ai-solution-platform.github.io/AI-Hub/ANTS-2.0-Hub-Index.html"
ORCHESTRATOR = WORKSPACE / "scripts" / "lint-orchestrator.py"

G = "\033[32m"
R = "\033[31m"
Y = "\033[33m"
B = "\033[34m"
N = "\033[0m"


def run_orchestrator(strict: bool = False) -> dict:
    if not ORCHESTRATOR.exists():
        return {"status": "MISSING", "summary": "lint-orchestrator.py not found"}
    args = ["python3", str(ORCHESTRATOR), "--json", "--no-report"]
    if strict:
        args.append("--strict")
    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=120)
        report = json.loads(result.stdout) if result.stdout.strip() else {}
        return {
            "status": "PASS" if result.returncode == 0 else "FAIL",
            "totals": report.get("totals", {}),
            "results": report.get("results", []),
            "returncode": result.returncode,
        }
    except Exception as e:
        return {"status": "ERROR", "summary": str(e)}


def head_url(url: str, timeout: float = 10.0, retries: int = 2) -> int:
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, method="HEAD",
                                          headers={"User-Agent": "ANTS-FridayPush/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.status
        except Exception as e:
            if attempt < retries:
                time.sleep(2)
                continue
            return -1
    return -1


def stop_tape(kref: str, status: str, lint_pass: int, lint_fail: int,
              hub_http: int = None, blocked_step: int = None, reason: str = "") -> str:
    if status == "ok":
        suffix = ""
        if hub_http is not None:
            suffix = f" · Pages {hub_http}"
        return f"✅ Friday Push {kref} · DAS clean · sync clean{suffix} · audit log appended"
    elif status == "blocked":
        return f"🟡 Friday Push {kref} BLOCKED at Step {blocked_step} · reason: {reason} · next attempt: <fill>"
    return ""


def main():
    p = argparse.ArgumentParser(description="Friday Push Prep · I-NEW-32 · K.23")
    p.add_argument("--kref", default="K.<x>", help="K-ref for Stop Tape labelling")
    p.add_argument("--post-push", action="store_true",
                   help="Run Step 4 only (HEAD check Hub-Index URL)")
    p.add_argument("--url", default=HUB_INDEX_URL, help="Hub-Index URL to verify")
    p.add_argument("--strict", action="store_true",
                   help="Treat advisory as failure (recommended for Friday)")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    timestamp = date.today().isoformat()
    report = {
        "schema": "friday-push-prep-v1",
        "date": timestamp,
        "kref": args.kref,
        "mode": "post_push" if args.post_push else "pre_push",
        "steps": [],
    }

    if args.post_push:
        # Step 4 only · URL verification
        if not args.json:
            print(f"{B}🔎 Friday Push · Step 4 · URL HEAD verification{N}")
            print(f"   → HEAD {args.url}")
        status = head_url(args.url)
        ok = 200 <= status < 400
        report["steps"].append({"id": "step4_url", "status": status, "pass": ok})
        if args.json:
            print(json.dumps(report, indent=2, ensure_ascii=False))
        else:
            if ok:
                print(f"   {G}✅ HTTP {status}{N}")
                print()
                print(stop_tape(args.kref, "ok", 0, 0, hub_http=status))
            else:
                print(f"   {R}❌ HTTP {status} (expected 2xx/3xx){N}")
                print()
                print(stop_tape(args.kref, "blocked", 0, 0, blocked_step=4,
                                reason=f"URL HEAD returned {status}"))
                sys.exit(1)
        return

    # Pre-push (Steps 1+2)
    if not args.json:
        print(f"{B}🚀 Friday Push Prep · {timestamp} · {args.kref}{N}\n")
        print(f"   {B}Step 1+2 · Lint orchestrator (6 gates){N}")

    orch = run_orchestrator(strict=args.strict)
    totals = orch.get("totals", {})
    pass_n = totals.get("pass", 0)
    fail_n = totals.get("fail", 0)
    adv_n = totals.get("advisory", 0)
    report["steps"].append({
        "id": "step1_2_lints",
        "status": orch["status"],
        "pass": pass_n, "fail": fail_n, "advisory": adv_n,
    })

    if not args.json:
        if orch["status"] == "PASS":
            print(f"   {G}✅ {pass_n} PASS{N} · {Y}{adv_n} advisory{N}")
        else:
            print(f"   {R}❌ {fail_n} FAIL{N} · {G}{pass_n} PASS{N} · {Y}{adv_n} advisory{N}")
            for r in orch.get("results", []):
                if r["status"] not in ("PASS", "ADVISORY"):
                    print(f"      {R}↳ {r['name']}: {r['summary']}{N}")

    # Decision
    blocked = orch["status"] != "PASS"
    if not args.json:
        print()
        if not blocked:
            print(f"{G}✅ Pre-push checks PASS — ready for Step 3 (Mac paste){N}")
            print()
            print(f"   {B}Step 3 · Mac terminal (manual paste · sandbox cannot push):{N}")
            print(f"     cd \"/Users/thanakanpermthong/Desktop/AI/ANTS 2.0 - AI Command Center/ANTS 2.0 - AI Command Center\"")
            print(f"     ./scripts/publish-to-github.sh")
            print()
            print(f"   {B}Step 4 · After push, verify URL:{N}")
            print(f"     python3 scripts/friday-push-prep.py --post-push --kref {args.kref}")
            print()
            print(f"   {B}Stop Tape (paste in conversation after push success):{N}")
            print(f"     ✅ Friday Push {args.kref} · DAS clean · sync clean · Pages 200 · audit log appended")
        else:
            reason = ""
            for r in orch.get("results", []):
                if r["status"] not in ("PASS", "ADVISORY"):
                    reason = r["name"]
                    break
            print(f"{R}❌ Pre-push BLOCKED at Step 1/2 — fix gate failures before paste{N}")
            print(f"   Recommended: python3 scripts/das-bulk-fix.py --apply (if DAS P0)")
            print()
            print(stop_tape(args.kref, "blocked", pass_n, fail_n,
                            blocked_step=1, reason=reason or "lint failure"))

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))

    if blocked:
        sys.exit(1)


if __name__ == "__main__":
    main()
