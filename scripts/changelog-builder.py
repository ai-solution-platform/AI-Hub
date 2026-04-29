#!/usr/bin/env python3
"""
changelog-builder.py — I-NEW-12 · Change Logs Auto-Aggregate

Parses FILE-MOVEMENT-MANIFEST-24Apr2026.md K.x entries → emits structured JSON
to /canonical/changelog.json · consumed by CC Change Logs tab at runtime.

Removes manual K.x table maintenance in CC HTML. Future Friday Push: this script
runs first → CC reads canonical/changelog.json → table auto-updates.

Auto-overwrite policy: rows older than 6 months → moved to
/archive/changelogs-old/{YYYY-MM}.json (per spec).

Usage:
  python3 changelog-builder.py                # parse manifest · write JSON
  python3 changelog-builder.py --dry-run      # parse · print to stdout
  python3 changelog-builder.py --archive-old  # move >6m rows to archive

Output: /canonical/changelog.json
Owner: Agent #63 FJA-CDCA · weekly cron Mon 09:00 ICT
Built: 2026-04-29 K.18 (per I-NEW-12 spec from K.15 Phase A)
"""

import json, re, sys
from datetime import date, datetime, timedelta
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
MANIFEST = WORKSPACE / "FILE-MOVEMENT-MANIFEST-24Apr2026.md"
OUT_JSON = WORKSPACE / "canonical" / "changelog.json"
ARCHIVE_DIR = WORKSPACE / "archive" / "changelogs-old"

ARCHIVE_THRESHOLD_DAYS = 180  # 6 months


def parse_manifest():
    """Parse K.x sections from manifest · return list of entries.

    K.19 fix · regex tightened to top-level K.\\d+ only:
      • Match  : `## K.12 — ...`, `## K.15 Phase A — ...`, `## K.17 FINAL — ...`
      • Reject : `## K.9.1 Phase 1 — ...`, `## K.12.1 — ...` (sub-section pollution)
    Rationale: K.18 ARAI surfaced sub-sections leaking as separate top-level entries.
    """
    if not MANIFEST.exists():
        print(f"❌ Manifest not found: {MANIFEST}", file=sys.stderr)
        sys.exit(2)
    text = MANIFEST.read_text(encoding='utf-8')
    entries = []
    # Match: ## K.<digits>(?!.<digit>) — Title (date)\n... until next ## K. or EOF
    # Negative lookahead `(?!\.\d)` prevents K.12.1 / K.9.1 / etc. from matching as top-level.
    pattern = r'## (K\.\d+(?!\.\d)(?:\s*Phase\s*\w+)?(?:\s*FINAL)?)\s*[—–-]\s*([^(\n]+?)\s*\(([^)]+)\)\s*\n(.*?)(?=\n## (?:K\.|---)|\Z)'
    for m in re.finditer(pattern, text, re.DOTALL):
        kx, title, date_str, body = m.groups()
        kx = kx.strip()
        title = title.strip()
        # Extract YYYY-MM-DD from date string (e.g. "27 Apr 2026 LATE-PM" → 2026-04-27)
        iso_date = parse_thai_date(date_str)
        # Extract trigger (first line after section · usually starts with "**Trigger:**" )
        trigger = ""
        tm = re.search(r'\*\*Trigger:?\*\*\s*([^\n]+)', body)
        if tm:
            trigger = tm.group(1).strip()
        # Extract ARAI Action (if present)
        action = ""
        am = re.search(r'\*\*Action:?\*\*\s*([^\n]+)', body)
        if am:
            action = am.group(1).strip()[:200]
        # Status flag
        status = "complete"
        if "in progress" in body.lower() or "in-progress" in body.lower():
            status = "in-progress"
        elif "FINAL" in kx or "final" in body.lower()[:100]:
            status = "final"
        entries.append({
            'kx': kx,
            'title': title,
            'date': iso_date,
            'date_raw': date_str,
            'trigger': trigger[:300],
            'action': action,
            'status': status,
            'body_preview': body.strip()[:500].replace('\n', ' ')
        })
    return entries


def parse_thai_date(s):
    """Best-effort parse to ISO date · returns YYYY-MM-DD or None."""
    # Try English month names
    months = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
              'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    for mon_short, mon_num in months.items():
        m = re.search(r'(\d{1,2})\s*' + mon_short + r'\w*\s*(\d{4})', s)
        if m:
            d, y = m.group(1), m.group(2)
            return f"{y}-{mon_num}-{int(d):02d}"
    # Thai months
    thai_months = {'ม.ค.': '01', 'ก.พ.': '02', 'มี.ค.': '03', 'เม.ย.': '04', 'พ.ค.': '05', 'มิ.ย.': '06',
                   'ก.ค.': '07', 'ส.ค.': '08', 'ก.ย.': '09', 'ต.ค.': '10', 'พ.ย.': '11', 'ธ.ค.': '12'}
    for tmon, num in thai_months.items():
        m = re.search(r'(\d{1,2})\s*' + tmon + r'\s*(\d{4})', s)
        if m:
            d, y = m.group(1), m.group(2)
            # Convert Buddhist year to Gregorian if > 2500
            yi = int(y)
            if yi > 2500:
                yi -= 543
            return f"{yi}-{num}-{int(d):02d}"
    return None


def archive_old_entries(entries):
    """Move entries older than 6 months to archive."""
    today = date.today()
    keep, archive = [], []
    for e in entries:
        if not e.get('date'):
            keep.append(e); continue
        try:
            entry_date = datetime.strptime(e['date'], '%Y-%m-%d').date()
            if (today - entry_date).days > ARCHIVE_THRESHOLD_DAYS:
                archive.append(e)
            else:
                keep.append(e)
        except Exception:
            keep.append(e)
    # Group archive by month → write per-month files
    if archive:
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
        by_month = {}
        for e in archive:
            mk = e['date'][:7]  # YYYY-MM
            by_month.setdefault(mk, []).append(e)
        for mk, ms in by_month.items():
            af = ARCHIVE_DIR / f"{mk}.json"
            existing = []
            if af.exists():
                try: existing = json.loads(af.read_text())
                except: pass
            af.write_text(json.dumps(existing + ms, indent=2, ensure_ascii=False), encoding='utf-8')
        print(f"  → Archived {len(archive)} entries across {len(by_month)} months")
    return keep


def main():
    dry_run = '--dry-run' in sys.argv
    archive_old = '--archive-old' in sys.argv

    print(f"\033[34m━━━ Change Logs Auto-Aggregate · {date.today()} ━━━\033[0m")
    entries = parse_manifest()
    print(f"\033[2mManifest:\033[0m parsed {len(entries)} K.x entries")

    if archive_old:
        entries = archive_old_entries(entries)
        print(f"\033[2mAfter archive:\033[0m {len(entries)} entries kept (≤ 6 months)")

    payload = {
        '_meta': {
            'generated_at': datetime.now().isoformat(),
            'source': 'FILE-MOVEMENT-MANIFEST-24Apr2026.md',
            'total_entries': len(entries),
            'archive_threshold_days': ARCHIVE_THRESHOLD_DAYS,
            'owner': 'Agent #63 FJA-CDCA · weekly cron'
        },
        'entries': entries
    }

    if dry_run:
        print(json.dumps(payload, indent=2, ensure_ascii=False)[:2000] + "\n... (truncated)")
    else:
        OUT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding='utf-8')
        print(f"\033[32m✅ Wrote {len(entries)} entries to {OUT_JSON.relative_to(WORKSPACE)}\033[0m")
        print(f"\033[2mNext:\033[0m CC Change Logs tab can fetch this JSON at runtime · auto-replaces hardcoded table")


if __name__ == "__main__":
    main()
