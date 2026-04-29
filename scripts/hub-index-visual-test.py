#!/usr/bin/env python3
"""
hub-index-visual-test.py — Hub-Index Visual Regression Test · I-NEW-20 · K.22

DOM-structure regression test for ANTS-2.0-Hub-Index.html. NOT a pixel diff
(those break on font kerning / spacing) — instead asserts:

  - Section count (h2.sec-head)
  - Footer link count (a[href] inside footer)
  - Required hero h1 substring
  - Required canonical anchor strings
  - Card class instances (e.g. .ix-card · .pdash-card · .arai-card)
  - Total <a href=...> count (within tolerance ±5%)

Baseline is locked in /canonical/hub-index-baseline.json. Update baseline
manually after intentional structural change with `--update-baseline`.

Owner #63 FJA-CDCA + HoEng #21 + Senior SDET #31 · weekly cron + on-demand.

Usage:
  python3 hub-index-visual-test.py                 # diff vs baseline
  python3 hub-index-visual-test.py --update-baseline   # write new baseline
  python3 hub-index-visual-test.py --json          # JSON output
  python3 hub-index-visual-test.py --strict        # exit 1 on any failure
  python3 hub-index-visual-test.py --tolerance 5   # link-count tolerance %
"""

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
TARGET = WORKSPACE / "ANTS-2.0-Hub-Index.html"
BASELINE = WORKSPACE / "canonical" / "hub-index-baseline.json"

# Anchors that MUST be present in any rendered Hub-Index
REQUIRED_ANCHORS = [
    "Single Gateway",                                    # hero h1
    "Operational Command Center",                        # primary section
    "Federated Wisdom",                                  # SAKM section
    "FJA-CDCA",                                          # cron agent section
    "Markdown Reports",                                  # files section
    "Human wisdom. AI at scale. Wisdom for everyone.",   # Vision canonical
    "Empower people. Build sustainable businesses.",     # Mission canonical (substring)
]

# Card class patterns to count
CARD_PATTERNS = [
    ("section_h2", r'<h2[^>]*class="[^"]*sec-head[^"]*"'),
    ("section", r'<section[^>]*class="sec"'),
    ("hero", r'<section[^>]*class="hero"'),
    ("arai", r'<section[^>]*class="arai"'),
]


def extract_metrics(html: str) -> dict:
    metrics = {}
    # Total anchor count
    metrics["a_href_count"] = len(re.findall(r"<a\s+[^>]*href=", html))
    # Footer link count (between <footer ... </footer>)
    footer_m = re.search(r"<footer[^>]*>(.*?)</footer>", html, re.DOTALL | re.IGNORECASE)
    if footer_m:
        metrics["footer_link_count"] = len(re.findall(r"<a\s+[^>]*href=", footer_m.group(1)))
    else:
        metrics["footer_link_count"] = 0
    # Card / section pattern counts
    for name, pattern in CARD_PATTERNS:
        metrics[f"count_{name}"] = len(re.findall(pattern, html))
    # Required anchor presence (boolean)
    metrics["required_anchors_present"] = {
        a: (a in html) for a in REQUIRED_ANCHORS
    }
    metrics["all_anchors_present"] = all(metrics["required_anchors_present"].values())
    # File size (rough sanity bound)
    metrics["file_size_bytes"] = len(html.encode("utf-8"))
    return metrics


def diff_metrics(baseline: dict, current: dict, tolerance_pct: float) -> list:
    """Return list of failures (empty list = clean)."""
    failures = []

    def check_exact(key, label):
        b = baseline.get(key)
        c = current.get(key)
        if b is None:
            return
        if b != c:
            failures.append({
                "category": "structure_drift",
                "severity": "P1",
                "message": f"{label} changed: baseline={b} → current={c}",
                "key": key,
            })

    def check_within_tolerance(key, label, tol_pct):
        b = baseline.get(key)
        c = current.get(key)
        if b is None or b == 0:
            return
        pct = abs(c - b) / b * 100
        if pct > tol_pct:
            failures.append({
                "category": "tolerance_exceeded",
                "severity": "P1",
                "message": f"{label} drift {pct:.1f}% > tolerance {tol_pct}% (baseline={b} → current={c})",
                "key": key,
            })

    # Structural counts must match exactly
    for key, label in [
        ("count_section_h2", "Section h2 count"),
        ("count_section", "<section.sec> count"),
        ("count_hero", "<section.hero> count"),
        ("count_arai", "<section.arai> count"),
        ("footer_link_count", "Footer link count"),
    ]:
        check_exact(key, label)

    # Total <a> count within tolerance
    check_within_tolerance("a_href_count", "Total <a href> count", tolerance_pct)

    # File size within 20% (broad sanity)
    check_within_tolerance("file_size_bytes", "File size", 20)

    # Required anchors
    cur_anchors = current.get("required_anchors_present", {})
    for anchor, present in cur_anchors.items():
        if not present:
            failures.append({
                "category": "anchor_missing",
                "severity": "P0",
                "message": f"Required anchor MISSING: '{anchor}'",
                "key": "required_anchors_present",
            })

    return failures


def write_baseline(metrics: dict):
    BASELINE.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "_meta": {
            "schema": "hub-index-baseline-v1",
            "captured_date": date.today().isoformat(),
            "captured_by": "scripts/hub-index-visual-test.py --update-baseline",
            "purpose": "Visual regression baseline for ANTS-2.0-Hub-Index.html · I-NEW-20 · K.22",
        },
        "metrics": metrics,
    }
    BASELINE.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def load_baseline() -> dict:
    if not BASELINE.exists():
        return {}
    return json.loads(BASELINE.read_text(encoding="utf-8")).get("metrics", {})


def main():
    p = argparse.ArgumentParser(description="Hub-Index Visual Regression Test · I-NEW-20")
    p.add_argument("--update-baseline", action="store_true",
                   help="Capture current state as new baseline (overwrite)")
    p.add_argument("--tolerance", type=float, default=5.0,
                   help="Tolerance %% for link counts (default 5)")
    p.add_argument("--json", action="store_true")
    p.add_argument("--strict", action="store_true")
    args = p.parse_args()

    if not TARGET.exists():
        print(f"❌ Target not found: {TARGET}", file=sys.stderr)
        sys.exit(2)

    html = TARGET.read_text(encoding="utf-8", errors="replace")
    current = extract_metrics(html)

    if args.update_baseline:
        write_baseline(current)
        if args.json:
            print(json.dumps({"action": "baseline_updated", "metrics": current}, indent=2, ensure_ascii=False))
        else:
            print(f"✅ Baseline written: {BASELINE}")
            print(f"   sections={current['count_section_h2']} · footer_links={current['footer_link_count']} · anchors={current['a_href_count']}")
        return

    baseline = load_baseline()
    if not baseline:
        print(f"⚠️  No baseline found at {BASELINE}", file=sys.stderr)
        print(f"   Run with --update-baseline first.", file=sys.stderr)
        if args.strict:
            sys.exit(1)
        return

    failures = diff_metrics(baseline, current, args.tolerance)

    report = {
        "schema": "hub-index-visual-test-v1",
        "date": date.today().isoformat(),
        "target": str(TARGET.relative_to(WORKSPACE)),
        "baseline_date": baseline.get("_baseline_date") if isinstance(baseline, dict) else None,
        "current_metrics": current,
        "failures": failures,
        "pass": len(failures) == 0,
    }

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        if not failures:
            print("✅ Hub-Index visual regression: ALL CLEAN")
            print(f"   sections={current['count_section_h2']} · footer_links={current['footer_link_count']} · anchors={current['a_href_count']} · size={current['file_size_bytes']}B")
        else:
            print(f"❌ Hub-Index visual regression: {len(failures)} failure(s)")
            for f in failures:
                sev = f.get("severity", "P1")
                tag = "🔴" if sev == "P0" else "🟡"
                print(f"   {tag} [{sev}] {f['message']}")

    if args.strict and failures:
        sys.exit(1)


if __name__ == "__main__":
    main()
