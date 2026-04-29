#!/usr/bin/env python3
"""
abbreviation-pair-lint.py — I-NEW-15 · Op 19 Mechanical Enforcement

Reads /canonical/abbreviations.md (SSOT) and scans consumer-facing files
for bare abbreviations not paired with full name on first occurrence.

Op 19 (locked K.15): "Always pair abbreviation with full name on first
occurrence in consumer-facing files (HTML/MD/email/deck). Pattern:
ABBREV (Full Name — Thai gloss optional). Bare codes only allowed in
private memory + insider docs."

Usage:
  python3 abbreviation-pair-lint.py              # full workspace sweep
  python3 abbreviation-pair-lint.py <file>       # single file check
  python3 abbreviation-pair-lint.py --strict     # exit 1 on any P1+

Reports:
  /reports/Abbreviation-Pair-Check-{date}.md   (human)

Owner: Agent #21 HoEng + #51 KM + #63 FJA-CDCA · weekly cron
Built: 2026-04-29 K.18 (per I-NEW-15 spec from K.15 Phase A)
"""

import json, re, sys
from datetime import date
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
GLOSSARY = WORKSPACE / "canonical" / "abbreviations.md"
REPORTS_DIR = WORKSPACE / "reports"

# Files exempt (insider/private context · per Op 19 spec)
EXEMPT_PATHS = ["archive/", "founder-story/", "morning-briefs/",
                "foundational-apr17/", "ObityX_Brand_Sale/",
                "vm-qa-gate/", "internal-transformation/",
                "FILE-MOVEMENT-MANIFEST", "SESSION_HANDOFF.md",
                "MEMORY.md", "/scripts/", "/canonical/abbreviations.md"]

# Window after first occurrence to find pairing (chars · per spec)
PAIRING_WINDOW = 200

# Pairing patterns recognized (per glossary spec)
def is_paired(text_after, full_name):
    """Check if full_name (or close variant) appears in text_after window."""
    # Normalize full name for fuzzy match (split on space/hyphen/&/+)
    fn_words = re.split(r'[\s\-&+/·]+', full_name)
    fn_words = [w for w in fn_words if len(w) >= 3 and w.lower() not in ('and', 'the', 'of')]
    if not fn_words:
        return False
    # Need at least 60% of significant words present
    matched = sum(1 for w in fn_words if w.lower() in text_after.lower())
    return matched / len(fn_words) >= 0.6


def parse_glossary():
    """Parse abbreviations.md tables. Returns list of (abbrev, full_name)."""
    if not GLOSSARY.exists():
        print(f"❌ Glossary not found: {GLOSSARY}", file=sys.stderr)
        sys.exit(2)
    text = GLOSSARY.read_text(encoding='utf-8')
    pairs = []
    # Match table rows: | abbrev | Full Name | ...
    for row in re.findall(r'^\|\s*([A-Z][A-Za-z0-9./_+-]+)\s*\|\s*([^|]+?)\s*\|', text, re.MULTILINE):
        abbrev, full = row
        full = full.strip()
        if not full or full == 'Full Name': continue
        if abbrev in ('Abbreviation', '#', 'ID'): continue
        # Filter out "K.x (e.g. ..." style entries · keep simple ones
        if 'e.g.' in abbrev or '(' in abbrev: continue
        pairs.append((abbrev, full))
    return pairs


def scan_file(filepath, pairs):
    """Scan single file for bare abbreviations missing pairing on first occurrence."""
    findings = []
    try:
        text = filepath.read_text(encoding='utf-8')
    except Exception:
        return findings
    for abbrev, full_name in pairs:
        # Skip if abbrev not in file at all
        if abbrev not in text: continue
        # Find first occurrence position
        # Use word boundary to avoid partial matches (e.g. "DAS" matching inside "DASH")
        match = re.search(r'\b' + re.escape(abbrev) + r'\b', text)
        if not match: continue
        first_pos = match.start()
        # Window: 200 chars BEFORE + AFTER first occurrence
        window_start = max(0, first_pos - PAIRING_WINDOW // 2)
        window_end = min(len(text), first_pos + PAIRING_WINDOW)
        window = text[window_start:window_end]
        if not is_paired(window, full_name):
            line_num = text[:first_pos].count('\n') + 1
            findings.append({
                'abbrev': abbrev,
                'full_name': full_name,
                'line': line_num,
                'context': text[max(0,first_pos-30):first_pos+60].replace('\n', ' ')
            })
    return findings


def main():
    pairs = parse_glossary()
    print(f"\033[34m━━━ Abbreviation Pair Lint · {date.today()} ━━━\033[0m")
    print(f"\033[2mGlossary:\033[0m {len(pairs)} abbreviations loaded from canonical/abbreviations.md")

    # Scope: single file/dir or workspace
    if len(sys.argv) > 1 and not sys.argv[1].startswith('--'):
        target = Path(sys.argv[1])
        if not target.is_absolute():
            target = WORKSPACE / target
        targets = [target] if target.is_file() else list(target.rglob('*'))
    else:
        targets = []
        for ext in ('html', 'md'):
            targets.extend(WORKSPACE.rglob(f'*.{ext}'))

    # Filter exempt
    files = []
    for f in targets:
        if not f.is_file(): continue
        rel = str(f.relative_to(WORKSPACE)) if f.is_relative_to(WORKSPACE) else str(f)
        if any(ex in rel for ex in EXEMPT_PATHS): continue
        files.append(f)

    print(f"\033[2mScope:\033[0m {len(files)} consumer files (exempt paths skipped)")

    all_findings = {}
    for f in files:
        findings = scan_file(f, pairs)
        if findings:
            all_findings[str(f.relative_to(WORKSPACE))] = findings

    total_p1 = sum(len(v) for v in all_findings.values())
    if total_p1 == 0:
        print(f"\n\033[32m✅ ALL CLEAN — Op 19 abbreviation pairing fully compliant\033[0m")
    else:
        print(f"\n\033[33m[P1] {total_p1} bare abbreviations across {len(all_findings)} files\033[0m")
        for rel, fs in list(all_findings.items())[:10]:
            print(f"\n  📄 {rel}")
            for f in fs[:5]:
                print(f"     L{f['line']}  {f['abbrev']} (expected: {f['full_name']})")
                print(f"            ...{f['context']}...")

    # Write report
    REPORTS_DIR.mkdir(exist_ok=True)
    report_md = REPORTS_DIR / f"Abbreviation-Pair-Check-{date.today()}.md"
    lines = [f"# Abbreviation Pair Check · {date.today()}",
             f"**Glossary:** {len(pairs)} abbreviations loaded · **Files:** {len(files)} scanned · **P1:** {total_p1}", ""]
    if total_p1 == 0:
        lines.append("✅ **ALL CLEAN** — Op 19 fully compliant")
    else:
        for rel, fs in all_findings.items():
            lines.append(f"\n### `{rel}` ({len(fs)} bare)")
            for f in fs:
                lines.append(f"- **L{f['line']}** `{f['abbrev']}` (expected pairing: _{f['full_name']}_)")
                lines.append(f"  - Context: `...{f['context']}...`")
    report_md.write_text('\n'.join(lines), encoding='utf-8')
    print(f"\n\033[2m📝 Report:\033[0m {report_md}")

    if '--strict' in sys.argv and total_p1 > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
