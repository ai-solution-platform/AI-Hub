#!/usr/bin/env python3
"""
decision-pack-scaffold.py — I-NEW-24 · Decision Pack Auto-Scaffold (STUB)

K.20.2 (29 Apr 2026) · Pre-built skeleton ready for #65 CDA Phase 2 implementation.
This stub validates the architecture · loads template · injects placeholders ·
auto-injects canonical V/M block. Full MEMORY-scan + CDA-curated pack output
is TODO for Phase 2 (8-21 พ.ค. · 5 hr build).

Owner: #65 CDA Chief Decision Architect (post-activation 2026-05-08)
Spec: /reports/I-NEW-24-25-26-Decision-Scaffold-Specs.md (I-NEW-24)

Usage (planned for Phase 2):
  python3 decision-pack-scaffold.py --kx 21 --topic "Phase 2 kickoff decisions" --n-packs 4
  python3 decision-pack-scaffold.py --kx 21 --auto-detect-pending  # scans MEMORY/SESSION_HANDOFF

STUB BEHAVIOR (current · K.20.2):
  - Validates template exists at /reports/_templates/Decision-Pack-Template.html
  - Validates canonical/vm-status.json present + has required keys
  - Replaces basic placeholders (date, kx, title)
  - Writes to /reports/Pending-Decisions-Pack-K{{KX}}-DRAFT.html (DRAFT suffix until CDA fills)
  - Reports # of placeholders remaining as TODO

Built: 2026-04-29 K.20.2 (CWO + KM #51 · pre-Phase-2 head-start)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

# ───────────────────────── Config ─────────────────────────

WORKSPACE = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = WORKSPACE / "reports" / "_templates" / "Decision-Pack-Template.html"
SSOT_PATH = WORKSPACE / "canonical" / "vm-status.json"
OUTPUT_DIR = WORKSPACE / "reports"

# Placeholder regex · matches {{NAME}} or {{NAME_WITH_UNDERSCORES}}
PLACEHOLDER_RE = re.compile(r"\{\{([A-Z][A-Z0-9_]+)\}\}")


# ───────────────────────── Helpers ─────────────────────────

def load_template() -> str:
    if not TEMPLATE_PATH.exists():
        print(f"❌ Template not found: {TEMPLATE_PATH}", file=sys.stderr)
        sys.exit(2)
    return TEMPLATE_PATH.read_text(encoding="utf-8")


def load_ssot() -> dict:
    if not SSOT_PATH.exists():
        print(f"❌ SSOT not found: {SSOT_PATH}", file=sys.stderr)
        sys.exit(2)
    return json.loads(SSOT_PATH.read_text(encoding="utf-8"))


def replace_basic(template: str, vars: dict) -> str:
    """Replace {{KEY}} placeholders with vars[KEY]. Leaves unmatched placeholders intact."""
    def repl(m: re.Match) -> str:
        key = m.group(1)
        return str(vars.get(key, m.group(0)))  # leave unchanged if key missing
    return PLACEHOLDER_RE.sub(repl, template)


def count_remaining_placeholders(html: str) -> int:
    return len(PLACEHOLDER_RE.findall(html))


# ───────────────────────── Phase 2 TODO ─────────────────────────

def scan_pending_decisions_from_memory() -> list[dict]:
    """
    TODO (Phase 2 build · #65 CDA · 9-10 พ.ค.):
      Scan /spaces/<space-id>/memory/SESSION_HANDOFF.md and MEMORY.md
      for "Pending Nut Decisions" sections · Pending tables · 🚨 Action required blocks.

    Returns list of {pack_name, severity, owner, time_est, why_now, steps[], default_recommendation}.

    Stub returns empty list to demonstrate API surface.
    """
    return []


def auto_classify_severity(decision_text: str) -> str:
    """
    TODO (Phase 2): keyword-based classifier.
      P0: "blocker" / "critical" / "security" / "irreversible"
      P1: "hygiene" / "deferred" / "should"
      P2: "polish" / "nice-to-have"
    """
    t = decision_text.lower()
    if any(w in t for w in ("blocker", "critical", "security", "irreversible", "deadline today", "deadline tomorrow")):
        return "P0"
    if any(w in t for w in ("polish", "nice-to-have", "minor", "cosmetic")):
        return "P2"
    return "P1"


# ───────────────────────── Main ─────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser(description="Decision Pack auto-scaffold · I-NEW-24 stub")
    ap.add_argument("--kx", type=str, required=True, help="K-sweep number e.g. 21 or '21.1'")
    ap.add_argument("--topic", type=str, default="Pending Decisions",
                    help="Top-level pack title")
    ap.add_argument("--n-packs", type=int, default=4,
                    help="Number of decision packs (used for ToC grid columns)")
    ap.add_argument("--required-by", type=str, default="",
                    help="Free-text deadline · e.g. 'Mon 4 พ.ค. 2026'")
    ap.add_argument("--auto-detect-pending", action="store_true",
                    help="(Phase 2 TODO) scan MEMORY for pending decisions instead of using stubs")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print output to stdout instead of writing file")
    args = ap.parse_args()

    print(f"\033[34m━━━ Decision Pack Scaffold · K.{args.kx} · {date.today()} ━━━\033[0m")

    template = load_template()
    ssot = load_ssot()
    print(f"\033[2m✓ Template loaded ({len(template)} bytes)\033[0m")
    print(f"\033[2m✓ SSOT loaded · roster={ssot['agent_roster']['total']} · ops={ssot['operating_principles']['count']}\033[0m")

    if args.auto_detect_pending:
        pending = scan_pending_decisions_from_memory()
        print(f"\033[33m⚠ Phase 2 TODO: --auto-detect-pending detected {len(pending)} (stub returns empty · CDA 9-10 พ.ค. impl)\033[0m")

    today_iso = date.today().isoformat()
    today_th = date.today().strftime("%d %b %Y")  # English month for now

    # Basic placeholder fills (the rest stay as {{...}} for CDA/CWO to complete)
    vars = {
        "KX": args.kx,
        "DATE": today_th,
        "DATE_ISO": today_iso,
        "TITLE": f"Pending Decisions · K.{args.kx}",
        "SESSION_NAME": f"K.{args.kx} Decision Pack",
        "REQUIRED_BY_DATE": args.required_by or "TBD",
        "OP12_PANEL_AGENTS_LIST": "CWO Cherkun · CHRO-AI #12 · CCVO #52 · CFO #7 · KM #51 · #63 FJA-CDCA",
        "N_PACKS": str(args.n_packs),
        "N": str(args.n_packs),
        "PACK_LIST": "TBD by CDA · auto-detect or manual fill",
        "SUBTITLE_DESCRIBING_WHY_THESE_DECISIONS_MATTER_AND_BY_WHEN":
            "TODO: CDA fills · scope of decisions · why these now · downstream tasks unblocked",
    }

    output = replace_basic(template, vars)
    remaining = count_remaining_placeholders(output)
    print(f"\033[2m✓ Basic vars replaced · {remaining} placeholders remaining for CDA/CWO\033[0m")

    suffix = "DRAFT"
    out_path = OUTPUT_DIR / f"Pending-Decisions-Pack-K{args.kx}-{suffix}.html"

    if args.dry_run:
        print(f"\033[2m--- DRY-RUN: would write to {out_path.relative_to(WORKSPACE)} ---\033[0m")
        print(output[:1500] + "\n... (truncated)")
    else:
        out_path.write_text(output, encoding="utf-8")
        print(f"\033[32m✅ Wrote {out_path.relative_to(WORKSPACE)}\033[0m")
        print(f"\033[2mNext step: CDA/CWO fills {remaining} remaining placeholders · then runs scripts/vm-canonical-lint.py · then renames -DRAFT.html → final\033[0m")

    print()
    print(f"\033[33m📋 Phase 2 build TODO (W2-Tue/Wed · 9-10 พ.ค. 2026 · #65 CDA owns):\033[0m")
    print("  1. Implement scan_pending_decisions_from_memory() — regex MEMORY+SESSION_HANDOFF for pending blocks")
    print("  2. Implement auto-classify severity (P0/P1/P2 from keywords)")
    print("  3. Generate <section class='pack'> per detected decision · auto-fill steps from MEMORY context")
    print("  4. Auto-run scripts/vm-canonical-lint.py + auto-inject canonical V/M block if missing")
    print("  5. Add --skip-confirm flag for full-auto mode")
    print("  6. Add tests in /scripts/tests/test_decision_pack_scaffold.py")


if __name__ == "__main__":
    main()
