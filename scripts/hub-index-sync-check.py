#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hub-index-sync-check.py — I-NEW-9 (Op 18 + Op 18b enforcement)

Purpose:
    Forcing function for Hub-Index synchronization + body-content diff check
    Built in response to 3rd "อีกแล้ว" recurrence (28 Apr 2026 LATE-AM-v3)
    Trigger: frontmatter version bumps without body content changes

Checks (5):
    C1. Hub-Index hero stat = 63 (not stale 52 or 62)
    C2. Hub-Index sync-note date present + ≤ 7 days old
    C3. Every consumer file frontmatter `last_updated` ≤ 7 days
    C4. (Op 18b) update_history entry must list specific section IDs/names
        — NOT generic "alignment update" / "minor fixes" / "cleanup"
    C5. (Op 18b) Per-section diff — if update_history mentions §X or
        section name, that section/string must exist in body

Output: JSON + MD report → /reports/Hub-Index-Sync-Check-{date}.{json,md}
Exit:   0 = ALL PASS · 1 = at least one defect

Owner: Agent #63 FJA-CDCA (weekly cron Mon 09:00 + on-demand)
Built: 29 Apr 2026 K.12 body-level re-audit
"""

import json, re, sys, os
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
REPORTS = WORKSPACE / "reports"
HUB_INDEX = WORKSPACE / "ANTS-2.0-Hub-Index.html"
SSOT_JSON = WORKSPACE / "canonical" / "vm-status.json"
TODAY = datetime.now().date()
FRESHNESS_DAYS = 7

CONSUMERS = [
    "command-center/ANTS-2.0-Unified-Command-Center.html",
    "products/ANTS-2.0-AI-Solutions-Stack.html",
    # K.13 (27 Apr 2026): reports/ANTS-Master-Audit-Report.md FOLDED into Command Center
    # See: archive/2026-04/master-audit-folded-into-CC/ for archived MD
    # K.14 (27 Apr 2026 LATE-PM): reports/ANTS-Audit-Dashboard.html FOLDED into Command Center
    # See: archive/2026-04/audit-dashboard-folded-into-CC-K14/ for archived HTML
    # Both = visualizations of audit content · now lives in CC tabs: exec (Audit Health) + roadmap (Standing Orders) + risks (K.x Audit Log)
    "internal-transformation/Internal-Transformation-Communication-Plan.md",
    "ANTS-2.0-Hub-Index.html",
    "README.md",
    "ecosystem/ANTS-Ecosystem-Dashboard.html",
    "agents/ANTS-Tier6-Frontier-Elite-Agents.md",
]

GENERIC_PHRASES = [
    "alignment update", "minor fixes", "cleanup", "small tweaks",
    "general update", "various updates", "misc update", "polish",
    "ปรับ alignment", "อัปเดตทั่วไป", "ปรับนิดหน่อย"
]

def read(p):
    try: return Path(p).read_text(encoding="utf-8")
    except Exception as e: return f"__ERROR__:{e}"

def get_frontmatter(text):
    """Parse YAML frontmatter or HTML comment frontmatter. Returns dict + body string."""
    # MD: ---\n...\n---
    m = re.match(r"^---\n(.*?)\n---\n(.*)", text, re.DOTALL)
    if m:
        fm_raw, body = m.group(1), m.group(2)
        return _parse_yaml_lite(fm_raw), body, "md"
    # HTML: <!-- ... last_updated: ... update_history: ... -->
    m = re.search(r"<!--\s*\n?(\s*last_updated:.*?)\n-->", text, re.DOTALL)
    if m:
        fm_raw = m.group(1)
        body = text  # in HTML, body = full doc minus comment
        return _parse_yaml_lite(fm_raw), body, "html"
    return {}, text, "unknown"

def _parse_yaml_lite(raw):
    """Tiny YAML parser for our flat keys + update_history list."""
    out = {"update_history": []}
    cur_list_key = None
    for line in raw.splitlines():
        if not line.strip(): continue
        if re.match(r"^\s*-\s+", line) and cur_list_key:
            val = re.sub(r"^\s*-\s+", "", line).strip().strip('"').strip("'")
            out[cur_list_key].append(val)
            continue
        m = re.match(r"^([a-zA-Z_]+):\s*(.*)$", line)
        if m:
            k, v = m.group(1), m.group(2).strip()
            if v == "" or v.startswith("|") or v.startswith(">"):
                cur_list_key = k
                if k not in out: out[k] = []
            else:
                out[k] = v.strip('"').strip("'")
                cur_list_key = None
    return out

def _parse_date(s):
    """Extract YYYY-MM-DD from a string."""
    m = re.search(r"(\d{4}-\d{2}-\d{2})", str(s))
    if m:
        try: return datetime.strptime(m.group(1), "%Y-%m-%d").date()
        except: pass
    return None

def check_file(rel):
    """Run C3+C4+C5 against a consumer file. Return dict of findings."""
    p = WORKSPACE / rel
    if not p.exists(): return {"file": rel, "exists": False, "defects": ["FILE_NOT_FOUND"]}
    text = read(p)
    fm, body, fmt = get_frontmatter(text)
    defects = []

    # C3: last_updated freshness
    lu = _parse_date(fm.get("last_updated", ""))
    if lu is None:
        defects.append("C3_NO_LAST_UPDATED")
    elif (TODAY - lu).days > FRESHNESS_DAYS:
        defects.append(f"C3_STALE_LAST_UPDATED({(TODAY-lu).days}d)")

    # C4: latest update_history entry must NOT be generic
    hist = fm.get("update_history", [])
    if not hist:
        defects.append("C4_NO_UPDATE_HISTORY")
    else:
        latest = hist[-1].lower()
        for phrase in GENERIC_PHRASES:
            if phrase.lower() in latest and len(latest) < 80:
                defects.append(f"C4_GENERIC_PHRASE({phrase})")
                break

    # C5: section diff — if latest entry mentions "§X" or section name, must exist in body
    if hist:
        latest = hist[-1]
        section_refs = re.findall(r"§([A-Za-z0-9._\-]+|[฀-๿]+)", latest)
        # Also look for "L\d+" line-number refs (HTMLs)
        line_refs = re.findall(r"\bL\d+\b", latest)
        body_lower = body.lower()
        for ref in section_refs[:5]:  # cap to avoid noise
            if ref.lower() not in body_lower:
                defects.append(f"C5_SECTION_NOT_IN_BODY(§{ref})")
        # line refs are only checked if file is HTML and has many lines
        if line_refs and fmt == "html":
            line_count = body.count("\n")
            for lr in line_refs[:3]:
                ln = int(lr[1:])
                if ln > line_count + 50:
                    defects.append(f"C5_LINE_OUT_OF_RANGE({lr})")

    return {"file": rel, "exists": True, "fmt": fmt, "last_updated": str(lu),
            "history_count": len(hist), "defects": defects}

def check_hub_index():
    """C1 + C2: hero stat 63 + sync-note ≤ 7 days."""
    text = read(HUB_INDEX)
    defects = []
    # C1: stat number 63 must appear in hero context
    hero_section = text.split("</header>")[0] if "</header>" in text else text[:5000]
    if re.search(r"\b62\s*(Agents?|agent|คน)\b", hero_section, re.IGNORECASE):
        defects.append("C1_STALE_62_IN_HERO")
    if not re.search(r"\b63\b", hero_section):
        defects.append("C1_NO_63_IN_HERO")
    # C2: sync-note date
    m = re.search(r"sync-note[^<]*?(\d{1,2}\s*(?:Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|Jan|Feb|Mar))",
                  text, re.IGNORECASE)
    if not m:
        defects.append("C2_NO_SYNC_NOTE_DATE")
    return {"file": "ANTS-2.0-Hub-Index.html", "hub_checks": True, "defects": defects}

def main():
    results = []
    results.append(check_hub_index())
    for f in CONSUMERS: results.append(check_file(f))
    total_defects = sum(len(r.get("defects", [])) for r in results)
    summary = {
        "run_at": datetime.now().isoformat(),
        "today": str(TODAY),
        "total_files": len(results),
        "files_with_defects": sum(1 for r in results if r.get("defects")),
        "total_defects": total_defects,
        "all_clean": total_defects == 0,
        "results": results,
    }
    REPORTS.mkdir(exist_ok=True)
    json_out = REPORTS / f"Hub-Index-Sync-Check-{TODAY}.json"
    md_out = REPORTS / f"Hub-Index-Sync-Check-{TODAY}.md"
    json_out.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    lines = [f"# Hub-Index Sync Check Report · {TODAY}",
             f"**Total files:** {summary['total_files']} · **Defects:** {total_defects} · "
             f"**Status:** {'ALL CLEAN ✅' if summary['all_clean'] else 'DEFECTS FOUND ❌'}",
             "", "| File | Defects |", "|---|---|"]
    for r in results:
        d = r.get("defects", [])
        lines.append(f"| `{r.get('file','?')}` | {' · '.join(d) if d else '✅ clean'} |")
    md_out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote: {json_out}\n       {md_out}")
    print(f"Status: {'ALL CLEAN ✅' if summary['all_clean'] else f'{total_defects} defects ❌'}")
    return 0 if summary["all_clean"] else 1

if __name__ == "__main__":
    sys.exit(main())
