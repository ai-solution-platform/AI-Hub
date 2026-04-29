#!/usr/bin/env python3
"""
sharepoint-wisdom-sync.py — I-NEW-27
====================================
SAKM v2 Forcing Function (K.21)
Owner: #63 FJA-CDCA (Target #13)
Cadence: Weekly · Mon 09:00 ICT cron

Purpose
-------
Detect drift between SharePoint source files and their corresponding
Wisdom Cards. Without this, Agents will reference stale wisdom — exactly
the failure mode SAKM v2 was built to avoid.

Compares:
  - Source file `last_modified` (from SharePoint inventory JSON)
  - Wisdom Card `source_last_modified` (frontmatter field)

Flags:
  - drift > 14 days → P1
  - drift > 30 days → P0
  - source missing  → P0 (orphan card)
  - card missing    → P1 (un-synthesized source)

Outputs
-------
  /sakm/reports/wisdom-drift-{YYYY-MM-DD}.json
  Console summary
  (Future) Slack/Teams alert to CWO via #63 broadcast lane

Usage
-----
  python3 scripts/sharepoint-wisdom-sync.py \
      --inventory sakm/inventory/sharepoint-ableai-index.json \
      --cards-dir sakm/wisdom-cards/ \
      --report-dir sakm/reports/ \
      [--dry-run]

Exit codes
----------
  0 = no drift
  1 = P1 drift only
  2 = P0 drift detected (escalate)
  3 = configuration / IO error

Idempotent · Dry-run default · Threshold gating
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

ISO = "%Y-%m-%dT%H:%M:%S"
DRIFT_P1_DAYS = 14
DRIFT_P0_DAYS = 30


# ---------- Data Models ----------

@dataclass
class SourceRecord:
    """A SharePoint inventory entry."""
    uri: str
    name: str
    path: str
    last_modified: datetime
    sensitivity: str = "INTERNAL"  # PUBLIC|INTERNAL|CONFIDENTIAL|SECRET


@dataclass
class WisdomCard:
    """A parsed Wisdom Card frontmatter snapshot."""
    card_path: Path
    card_id: str
    source_uri: str
    source_last_modified: datetime
    sensitivity: str
    status: str


@dataclass
class DriftFinding:
    severity: str          # P0 | P1
    kind: str              # SOURCE_NEWER | ORPHAN_CARD | UNSYNTHESIZED | SENSITIVITY_MISMATCH
    drift_days: int
    source_uri: str
    source_path: str
    card_path: str | None
    note: str

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class Report:
    generated_at: str
    inventory_path: str
    cards_dir: str
    counts: dict = field(default_factory=dict)
    findings: list[dict] = field(default_factory=list)


# ---------- Parsers ----------

FRONTMATTER_RE = re.compile(
    r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL
)
KV_RE = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.+?)\s*$", re.M)


def parse_frontmatter(text: str) -> dict[str, str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    block = m.group(1)
    return {k: v.strip().strip("\"'") for k, v in KV_RE.findall(block)}


def parse_dt(s: str) -> datetime:
    s = s.strip().rstrip("Z")
    # Tolerant ISO
    for fmt in (ISO, "%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    raise ValueError(f"Unparseable datetime: {s!r}")


def load_inventory(path: Path) -> dict[str, SourceRecord]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    items = raw.get("items", raw if isinstance(raw, list) else [])
    out: dict[str, SourceRecord] = {}
    for it in items:
        try:
            out[it["uri"]] = SourceRecord(
                uri=it["uri"],
                name=it.get("name", ""),
                path=it.get("path", ""),
                last_modified=parse_dt(it["last_modified"]),
                sensitivity=it.get("sensitivity", "INTERNAL"),
            )
        except (KeyError, ValueError) as e:
            print(f"[warn] skipping inventory item: {e}", file=sys.stderr)
    return out


def load_cards(cards_dir: Path) -> dict[str, WisdomCard]:
    out: dict[str, WisdomCard] = {}
    for p in cards_dir.rglob("WC-*.md"):
        fm = parse_frontmatter(p.read_text(encoding="utf-8"))
        if not fm.get("source_uri") or not fm.get("source_last_modified"):
            print(f"[warn] card missing required frontmatter: {p}", file=sys.stderr)
            continue
        try:
            out[fm["source_uri"]] = WisdomCard(
                card_path=p,
                card_id=fm.get("id", p.stem),
                source_uri=fm["source_uri"],
                source_last_modified=parse_dt(fm["source_last_modified"]),
                sensitivity=fm.get("sensitivity_tag", "INTERNAL"),
                status=fm.get("status", "UNKNOWN"),
            )
        except ValueError as e:
            print(f"[warn] {p}: {e}", file=sys.stderr)
    return out


# ---------- Drift Detection ----------

def compute_drift(
    inventory: dict[str, SourceRecord],
    cards: dict[str, WisdomCard],
) -> Iterable[DriftFinding]:
    src_uris = set(inventory.keys())
    card_uris = set(cards.keys())

    # Source newer than card → wisdom-stale
    for uri in src_uris & card_uris:
        src = inventory[uri]
        card = cards[uri]
        delta = (src.last_modified - card.source_last_modified).days
        if delta > DRIFT_P0_DAYS:
            yield DriftFinding(
                severity="P0",
                kind="SOURCE_NEWER",
                drift_days=delta,
                source_uri=uri,
                source_path=src.path,
                card_path=str(card.card_path),
                note=f"Source updated {delta}d after card. Resync required.",
            )
        elif delta > DRIFT_P1_DAYS:
            yield DriftFinding(
                severity="P1",
                kind="SOURCE_NEWER",
                drift_days=delta,
                source_uri=uri,
                source_path=src.path,
                card_path=str(card.card_path),
                note=f"Source updated {delta}d after card. Schedule resync.",
            )
        # Sensitivity mismatch → always P0 (security drift)
        if src.sensitivity != card.sensitivity:
            yield DriftFinding(
                severity="P0",
                kind="SENSITIVITY_MISMATCH",
                drift_days=delta,
                source_uri=uri,
                source_path=src.path,
                card_path=str(card.card_path),
                note=f"Source={src.sensitivity} vs Card={card.sensitivity}",
            )

    # Card without source → orphan
    for uri in card_uris - src_uris:
        card = cards[uri]
        yield DriftFinding(
            severity="P0",
            kind="ORPHAN_CARD",
            drift_days=-1,
            source_uri=uri,
            source_path="(missing)",
            card_path=str(card.card_path),
            note="Source no longer in SharePoint inventory. Verify deletion or re-crawl.",
        )

    # Source without card → un-synthesized (informational)
    for uri in src_uris - card_uris:
        src = inventory[uri]
        yield DriftFinding(
            severity="P1",
            kind="UNSYNTHESIZED",
            drift_days=-1,
            source_uri=uri,
            source_path=src.path,
            card_path=None,
            note="Source not yet synthesized into a Wisdom Card.",
        )


# ---------- CLI ----------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--inventory", type=Path, required=True)
    ap.add_argument("--cards-dir", type=Path, required=True)
    ap.add_argument("--report-dir", type=Path, required=True)
    ap.add_argument("--dry-run", action="store_true", help="Print only, do not write report")
    args = ap.parse_args()

    if not args.inventory.exists():
        print(f"[err] inventory not found: {args.inventory}", file=sys.stderr)
        return 3
    if not args.cards_dir.exists():
        print(f"[err] cards dir not found: {args.cards_dir}", file=sys.stderr)
        return 3

    inventory = load_inventory(args.inventory)
    cards = load_cards(args.cards_dir)
    findings = list(compute_drift(inventory, cards))

    p0 = [f for f in findings if f.severity == "P0"]
    p1 = [f for f in findings if f.severity == "P1"]

    report = Report(
        generated_at=datetime.now(timezone.utc).strftime(ISO + "Z"),
        inventory_path=str(args.inventory),
        cards_dir=str(args.cards_dir),
        counts={
            "sources": len(inventory),
            "cards": len(cards),
            "findings_total": len(findings),
            "P0": len(p0),
            "P1": len(p1),
        },
        findings=[f.as_dict() for f in findings],
    )

    print(f"=== Wisdom Sync Drift Report ===")
    print(f"sources={len(inventory)}  cards={len(cards)}  P0={len(p0)}  P1={len(p1)}")
    for f in (p0 + p1)[:10]:
        print(f"  [{f.severity}] {f.kind} {f.drift_days}d :: {f.source_path or f.source_uri}")

    if not args.dry_run:
        args.report_dir.mkdir(parents=True, exist_ok=True)
        out_path = args.report_dir / f"wisdom-drift-{datetime.now(timezone.utc):%Y-%m-%d}.json"
        out_path.write_text(json.dumps(asdict(report), indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {out_path}")

    if p0:
        return 2
    if p1:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
