#!/usr/bin/env python3
"""
das-bulk-fix.py — Auto-remediation companion to vm-canonical-lint.py

Workflow:
  Phase 1: Bulk P0 sweep (mechanical drift — agent count stale strings)
           Word-boundary regex, derived from SSOT stale_counts_forbidden
  Phase 2: P1 canonical V/M block injection
           Per-file SSOT-branded block (HTML <section> for HTML, MD blockquote for MD)
  Phase 3: Per-file gate verify (Op 11 QA Layer-1) via vm-canonical-lint.py

Usage:
  python3 scripts/das-bulk-fix.py                  # dry-run · show plan
  python3 scripts/das-bulk-fix.py --apply          # apply changes
  python3 scripts/das-bulk-fix.py --apply --phase 1   # P0 only
  python3 scripts/das-bulk-fix.py --apply --phase 2   # P1 only
  python3 scripts/das-bulk-fix.py --threshold 5    # only run if defects > 5

Idempotent: safe to re-run. Skips files that already pass lint.

Owner: Agent #63 FJA-CDCA (Tier 5 · folded sweep agent)
Created: 2026-04-28 · K.9 batch promotion (I-NEW-6)
SSOT: /canonical/vm-status.json
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SSOT_JSON = ROOT / "canonical" / "vm-status.json"
LINT_SCRIPT = ROOT / "scripts" / "vm-canonical-lint.py"

# ANSI colors for terminal output
C = {"red": "\033[31m", "green": "\033[32m", "yellow": "\033[33m",
     "blue": "\033[34m", "dim": "\033[2m", "reset": "\033[0m"}


def load_ssot():
    """Load canonical SSOT for stale counts + V/M substrings."""
    return json.loads(SSOT_JSON.read_text(encoding="utf-8"))


def run_lint(target=None):
    """Run vm-canonical-lint.py and parse JSON output. Returns defect dict."""
    cmd = ["python3", str(LINT_SCRIPT)]
    if target:
        cmd.append(str(target))
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    # Find latest DAS report JSON
    reports = sorted((ROOT / "reports").glob("DAS-Sweep-Report-*.json"))
    if not reports:
        return {}
    return json.loads(reports[-1].read_text(encoding="utf-8"))


def phase1_p0_sweep(files, ssot, apply=False):
    """Bulk find/replace for stale agent counts. Word-boundary anchored."""
    canonical_count = ssot["agent_roster"]["total"]  # 63
    stale_counts = ssot["agent_roster"]["stale_counts_forbidden"]  # [52, 62]
    stale_pattern = "|".join(str(n) for n in stale_counts)

    # Pattern A: "X agents/Agents/agent/Agent/AI Agents" → "63 ..."
    pat_a = re.compile(rf'\b({stale_pattern}) (AI Agents|Agents|agents|agent|Agent)\b')
    # Pattern B: "X-Agent" / "X-agent" compound → "63-..."
    pat_b = re.compile(rf'\b({stale_pattern})-(Agent|agent)\b')

    changes = []
    for path_str in files:
        path = ROOT / path_str
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        new_text = pat_a.sub(f"{canonical_count} \\2", text)
        new_text = pat_b.sub(f"{canonical_count}-\\2", new_text)
        if new_text != text:
            n_changes = len(pat_a.findall(text)) + len(pat_b.findall(text))
            changes.append((path_str, n_changes))
            if apply:
                path.write_text(new_text, encoding="utf-8")
    return changes


def phase2_p1_inject(file_needs, ssot, apply=False):
    """Inject canonical V/M block. file_needs = {path: (need_v, need_m)}."""
    vision = ssot["vision_mission"]["vision"]["en"]
    mission = ssot["vision_mission"]["mission"]["en"]

    def md_block(v, m):
        parts = ["", "", "---", "",
                 "<!-- Canonical V/M SSOT alignment · auto-injected · do not remove · "
                 "pair: /canonical/vm-status.json + canonical-facts.md -->",
                 "", "## 📌 Canonical V/M Reference (SSOT)", ""]
        if v: parts.append(f"- **Vision (canonical):** *{vision}*")
        if m: parts.append(f"- **Mission (canonical):** *{mission}*")
        parts += ["", "_Source: `/canonical/canonical-facts.md` + `/canonical/vm-status.json` "
                  "· Locked Apr 23, 2026 · Op 16 SSOT discipline_", ""]
        return "\n".join(parts)

    def html_block(v, m):
        parts = ["", "",
                 "<!-- ═══════════════════════════════════════════════════════════════ -->",
                 "<!-- Canonical V/M SSOT alignment · auto-injected · do not remove   -->",
                 "<!-- Pair: /canonical/vm-status.json + canonical-facts.md           -->",
                 "<!-- ═══════════════════════════════════════════════════════════════ -->",
                 '<section style="margin:32px auto;max-width:960px;padding:18px 22px;'
                 'background:#f8fafc;border-left:4px solid #6366f1;border-radius:8px;'
                 'font:13px/1.6 -apple-system,BlinkMacSystemFont,sans-serif;color:#475569;">',
                 '  <div style="font-weight:600;color:#1e293b;margin-bottom:8px;">'
                 '📌 Canonical V/M Reference (SSOT)</div>']
        if v: parts.append(f'  <div style="margin:4px 0;"><strong>Vision '
                           f'(canonical):</strong> <em>{vision}</em></div>')
        if m: parts.append(f'  <div style="margin:4px 0;"><strong>Mission '
                           f'(canonical):</strong> <em>{mission}</em></div>')
        parts += ['  <div style="font-size:11px;color:#94a3b8;margin-top:8px;">'
                  'Source: <code>/canonical/canonical-facts.md</code> + '
                  '<code>/canonical/vm-status.json</code> · Locked Apr 23, 2026 '
                  '· Op 16 SSOT discipline</div>', "</section>", ""]
        return "\n".join(parts)

    changes = []
    for path_str, (need_v, need_m) in file_needs.items():
        path = ROOT / path_str
        if not path.exists():
            continue
        is_html = path_str.endswith(".html")
        # Idempotency check — skip if canonical block already present
        text = path.read_text(encoding="utf-8")
        if "Canonical V/M Reference (SSOT)" in text or "Canonical V/M SSOT alignment" in text:
            continue
        block = html_block(need_v, need_m) if is_html else md_block(need_v, need_m)
        if is_html and "</body>" in text:
            new_text = text.replace("</body>", block + "\n</body>", 1)
        else:
            new_text = text.rstrip() + block
        flags = ("V" if need_v else "") + ("M" if need_m else "")
        flags = "+".join(list(flags))
        changes.append((path_str, flags))
        if apply:
            path.write_text(new_text, encoding="utf-8")
    return changes


def phase3_verify(files):
    """Run lint per file. Returns (clean_count, defect_files)."""
    clean, defective = [], []
    for path_str in files:
        result = subprocess.run(
            ["python3", str(LINT_SCRIPT), path_str],
            capture_output=True, text=True, cwd=ROOT
        )
        out = re.sub(r"\x1b\[[0-9;]*m", "", result.stdout)
        if "ALL CLEAN" in out:
            clean.append(path_str)
        else:
            defective.append(path_str)
    return clean, defective


def derive_defect_map():
    """Parse latest DAS report JSON → returns ({p0_files}, {p1_files: (V, M)})."""
    reports = sorted((ROOT / "reports").glob("DAS-Sweep-Report-*.json"))
    if not reports:
        return [], {}
    data = json.loads(reports[-1].read_text(encoding="utf-8"))
    p0_files = set()
    p1_files = {}
    for entry in data.get("findings", []):
        path = entry["file"]
        for defect in entry.get("defects", []):
            sev = defect.get("severity")
            msg = defect.get("message", "")
            if sev == "P0":
                p0_files.add(path)
            elif sev == "P1":
                need_v, need_m = p1_files.get(path, (False, False))
                if "Vision" in msg: need_v = True
                if "Mission" in msg: need_m = True
                p1_files[path] = (need_v, need_m)
    return list(p0_files), p1_files


def main():
    parser = argparse.ArgumentParser(description="Bulk DAS defect remediation")
    parser.add_argument("--apply", action="store_true", help="Apply changes (default: dry-run)")
    parser.add_argument("--phase", choices=["1", "2", "all"], default="all")
    parser.add_argument("--threshold", type=int, default=0,
                        help="Only run if total defects > threshold")
    args = parser.parse_args()

    print(f"{C['blue']}━━━ das-bulk-fix · {'APPLY' if args.apply else 'DRY-RUN'} "
          f"· phase={args.phase} ━━━{C['reset']}")

    # Run lint to get fresh defect map
    print(f"{C['dim']}→ Running lint to derive defect map…{C['reset']}")
    run_lint()  # generates DAS report JSON
    p0_files, p1_files = derive_defect_map()
    total_defects = len(p0_files) + sum(1 for _ in p1_files)

    if total_defects <= args.threshold:
        print(f"{C['green']}✅ Defects ({total_defects}) ≤ threshold ({args.threshold}) — no action.{C['reset']}")
        return 0

    ssot = load_ssot()

    # Phase 1
    if args.phase in ("1", "all") and p0_files:
        print(f"\n{C['blue']}Phase 1 — P0 sweep on {len(p0_files)} files{C['reset']}")
        changes = phase1_p0_sweep(p0_files, ssot, apply=args.apply)
        for path, n in changes:
            tag = "FIX" if args.apply else "WOULD-FIX"
            print(f"  [{tag}] {path} · {n} match(es)")

    # Phase 2
    if args.phase in ("2", "all") and p1_files:
        print(f"\n{C['blue']}Phase 2 — P1 canonical V/M injection on {len(p1_files)} files{C['reset']}")
        changes = phase2_p1_inject(p1_files, ssot, apply=args.apply)
        for path, flags in changes:
            tag = "INJECT" if args.apply else "WOULD-INJECT"
            print(f"  [{tag}] {path} · {flags}")

    # Phase 3 — verify (only if --apply)
    if args.apply:
        all_files = list(set(p0_files) | set(p1_files.keys()))
        print(f"\n{C['blue']}Phase 3 — Per-file gate verify (Op 11 QA Layer-1){C['reset']}")
        clean, defective = phase3_verify(all_files)
        for f in clean:
            print(f"  {C['green']}✅{C['reset']} {f}")
        for f in defective:
            print(f"  {C['red']}❌{C['reset']} {f}")
        if defective:
            print(f"\n{C['red']}⚠️  {len(defective)} file(s) still defective. "
                  f"Review manually.{C['reset']}")
            return 1
        print(f"\n{C['green']}✅ All {len(clean)} files clean.{C['reset']}")
    else:
        print(f"\n{C['yellow']}DRY-RUN complete. Re-run with --apply to write changes.{C['reset']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
