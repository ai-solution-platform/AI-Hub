#!/usr/bin/env python3
"""
workshop-output-registry.py — Workshop Output Registry · I-NEW-13 · K.23

Validates /canonical/workshop-outputs.json against:
  - Schema (required fields)
  - URL reachability (HTTP HEAD · live state only · optional)
  - Local file existence (file state)
  - Confidential list overlap detection (block if any registry entry == confidential)
  - State transition validation (state must be one of allowed enum)

Reports: status table + JSON.

Usage:
  python3 workshop-output-registry.py                   # validate · no HTTP
  python3 workshop-output-registry.py --check-urls      # HTTP HEAD live URLs
  python3 workshop-output-registry.py --json
  python3 workshop-output-registry.py --strict          # exit 1 on findings

Owner: Senior Content & Copy #27 + HoEng #21 + #63 FJA-CDCA Target #5
"""

import argparse
import json
import sys
from datetime import date
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
SSOT = WORKSPACE / "canonical" / "workshop-outputs.json"
REPORTS_DIR = WORKSPACE / "reports"

ALLOWED_STATES = {"live", "internal", "tbd", "wip", "private"}
ALLOWED_OUTPUT_TYPES = {"url", "file", "drive", "notion"}
REQUIRED_FIELDS = ["code", "title", "category", "output_type", "state"]


def load_ssot():
    if not SSOT.exists():
        print(f"❌ SSOT not found: {SSOT}", file=sys.stderr)
        sys.exit(2)
    return json.loads(SSOT.read_text(encoding="utf-8"))


def http_head(url: str, timeout: float = 5.0) -> int:
    try:
        import urllib.request
        req = urllib.request.Request(url, method="HEAD",
                                      headers={"User-Agent": "ANTS-WorkshopRegistry/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status
    except Exception as e:
        return -1


def main():
    p = argparse.ArgumentParser(description="Workshop Output Registry · I-NEW-13 · K.23")
    p.add_argument("--check-urls", action="store_true",
                   help="HTTP HEAD live-state URLs (network required)")
    p.add_argument("--json", action="store_true")
    p.add_argument("--strict", action="store_true")
    p.add_argument("--no-report", action="store_true")
    args = p.parse_args()

    ssot = load_ssot()
    items = ssot.get("items", [])
    confidential_list = ssot.get("_confidential_workshops", {}).get("list", [])

    findings = []
    enriched = []

    for item in items:
        # Schema check
        for field in REQUIRED_FIELDS:
            if field not in item:
                findings.append({
                    "code": item.get("code", "?"),
                    "severity": "P0",
                    "category": "schema_missing_field",
                    "message": f"Missing required field: '{field}'",
                })

        state = item.get("state", "?")
        ot = item.get("output_type", "?")
        loc = item.get("location", "")
        title = item.get("title", "")
        code = item.get("code", "?")

        if state not in ALLOWED_STATES:
            findings.append({
                "code": code, "severity": "P1",
                "category": "state_invalid",
                "message": f"State '{state}' not in {sorted(ALLOWED_STATES)}",
            })

        if ot not in ALLOWED_OUTPUT_TYPES:
            findings.append({
                "code": code, "severity": "P1",
                "category": "output_type_invalid",
                "message": f"output_type '{ot}' not in {sorted(ALLOWED_OUTPUT_TYPES)}",
            })

        # Confidential overlap detection
        for conf_name in confidential_list:
            if conf_name.lower() in title.lower():
                findings.append({
                    "code": code, "severity": "P0",
                    "category": "confidential_leak",
                    "message": f"Workshop '{title}' overlaps confidential list entry '{conf_name}' — must NOT be in registry",
                })

        # State requires location (live · internal · file)
        if state in ("live", "internal") and not loc:
            findings.append({
                "code": code, "severity": "P1",
                "category": "location_missing",
                "message": f"state={state} requires location · empty",
            })

        # File state · verify local file exists
        check = {"verdict": "pending"}
        if ot == "file" and loc:
            full = WORKSPACE / loc.lstrip("/")
            if full.exists():
                check["verdict"] = "file_ok"
            else:
                check["verdict"] = "file_missing"
                findings.append({
                    "code": code, "severity": "P0",
                    "category": "file_missing",
                    "message": f"output_type=file location='{loc}' does NOT exist",
                })

        # URL state · HTTP HEAD if --check-urls
        if args.check_urls and ot == "url" and state == "live" and loc.startswith("http"):
            status = http_head(loc)
            check["http"] = status
            if status not in (200, 301, 302, 304):
                findings.append({
                    "code": code, "severity": "P1",
                    "category": "url_unreachable",
                    "message": f"HTTP {status} for {loc}",
                })

        enriched.append({**item, "_check": check})

    # State distribution counts
    state_counts = {}
    for item in items:
        s = item.get("state", "?")
        state_counts[s] = state_counts.get(s, 0) + 1

    report = {
        "schema": "workshop-output-registry-v1",
        "date": date.today().isoformat(),
        "ssot_version": ssot.get("_meta", {}).get("version"),
        "totals": {"items": len(items), "by_state": state_counts},
        "findings": findings,
        "items": enriched,
    }

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"📋 Workshop Output Registry · {date.today()}")
        print(f"   {len(items)} workshops · " + " · ".join(f"{k}={v}" for k, v in state_counts.items()))
        print()
        for item in items:
            code = item.get("code", "?")
            state = item.get("state", "?")
            title = item.get("title", "")
            badge = {
                "live": "🟢",
                "internal": "🔵",
                "tbd": "🟡",
                "wip": "⚪",
                "private": "🔒",
            }.get(state, "?")
            print(f"   {badge} {code:<5} {state:<8} {title[:55]}")
        print()
        if not findings:
            print("✅ All checks pass · zero schema or content drift")
        else:
            p0 = [f for f in findings if f["severity"] == "P0"]
            p1 = [f for f in findings if f["severity"] == "P1"]
            print(f"P0={len(p0)} · P1={len(p1)}")
            for f in findings[:20]:
                tag = "🔴" if f["severity"] == "P0" else "🟡"
                print(f"   {tag} [{f['severity']}] {f['code']}: {f['message']}")

    if not args.no_report:
        try:
            REPORTS_DIR.mkdir(parents=True, exist_ok=True)
            json_out = REPORTS_DIR / f"Workshop-Registry-Report-{date.today()}.json"
            json_out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
            if not args.json:
                print(f"\n📝 Report: {json_out.relative_to(WORKSPACE)}")
        except Exception as e:
            print(f"⚠️  Could not write report: {e}", file=sys.stderr)

    if args.strict and findings:
        sys.exit(1)


if __name__ == "__main__":
    main()
