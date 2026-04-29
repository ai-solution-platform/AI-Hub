#!/usr/bin/env python3
"""
vm-canonical-lint.py — Direction Alignment Sweep (DAS) · I-NEW-1

Reads /canonical/vm-status.json (SSOT) and scans consumer HTML/MD files in
workspace. Reports V/M, agent count, ecosystem, operating principle divergences.

Check categories:
  C1 = check_vm (V/M canonical · zero-substring + stale-draft)
  C2 = check_agent_count (roster drift · 52/62/63 stale)
  C3 = check_ecosystem (27 ventures · 29 stale)
  C4 = check_op_count (19 OPs · 11/13/16/18 stale)
  C5 = strip_history_blocks (preprocessor · I-NEW-10 · K.12)
  C6 = check_hot_rules (Hot Rule drift detector · I-NEW-14 · K.22)
  C7 = check_vm_anchors_full (V/M anchors 1→6 partial detection · I-NEW-19 · K.22)

Usage:
  python3 vm-canonical-lint.py                 # full workspace sweep
  python3 vm-canonical-lint.py <file>          # single file
  python3 vm-canonical-lint.py <dir>           # single directory
  python3 vm-canonical-lint.py --json          # JSON output to stdout only
  python3 vm-canonical-lint.py --strict        # exit 1 on any defect (for hooks)
  python3 vm-canonical-lint.py --no-report     # skip writing report files

Reports:
  /reports/DAS-Sweep-Report-{date}.md   (human)
  /reports/DAS-Sweep-Report-{date}.json (machine)

Owner: Agent #21 HoEng + #51 KM + #63 FJA-CDCA
Activated: 2026-04-28 (early activation per V/M cascade gap defect 27 Apr 2026)
"""

import json
import os
import re
import sys
from datetime import date
from pathlib import Path

# Default workspace root (script lives in /scripts/)
WORKSPACE = Path(__file__).resolve().parent.parent
SSOT_PATH = WORKSPACE / "canonical" / "vm-status.json"
REPORTS_DIR = WORKSPACE / "reports"

# ANSI colors for terminal output
G = "\033[32m"
R = "\033[31m"
Y = "\033[33m"
B = "\033[34m"
DIM = "\033[2m"
N = "\033[0m"


def load_ssot():
    if not SSOT_PATH.exists():
        print(f"{R}ERROR: SSOT not found at {SSOT_PATH}{N}", file=sys.stderr)
        sys.exit(2)
    with open(SSOT_PATH, encoding="utf-8") as f:
        return json.load(f)


def is_exempt(file_path: Path, ssot: dict) -> bool:
    try:
        rel = file_path.relative_to(WORKSPACE)
    except ValueError:
        return False
    rel_str = str(rel).replace(os.sep, "/")
    for ex in ssot.get("exempt_paths", []):
        ex_clean = ex.strip("/")
        if rel_str.startswith(ex_clean + "/") or rel_str == ex_clean:
            return True
    # Also exempt the SSOT files themselves
    if rel_str.startswith("canonical/") or rel_str.startswith("scripts/"):
        return True
    # Exempt by filename pattern (audit trails, lint reports, etc.)
    fname = file_path.name
    for pattern in ssot.get("exempt_filename_patterns", []):
        if pattern in fname:
            return True
    # Always exempt script-output reports (data lists · not consumer content)
    # K.19: extended beyond DAS-Sweep-Report to cover I-NEW-9 + I-NEW-15 outputs.
    SCRIPT_OUTPUT_PREFIXES = (
        "DAS-Sweep-Report",
        "Abbreviation-Pair-Check",   # I-NEW-15 abbreviation-pair-lint.py output
        "Hub-Index-Sync-Check",      # I-NEW-9 hub-index-sync-check.py output
    )
    if any(fname.startswith(p) for p in SCRIPT_OUTPUT_PREFIXES):
        return True
    return False


def collect_files(target: Path, ssot: dict) -> list:
    files = []
    if target.is_file():
        return [target]
    for root, _dirs, filenames in os.walk(target):
        for fn in filenames:
            p = Path(root) / fn
            if p.suffix.lower() not in (".html", ".md", ".htm"):
                continue
            if is_exempt(p, ssot):
                continue
            files.append(p)
    return sorted(files)


def line_of(content: str, idx: int) -> int:
    return content[:idx].count("\n") + 1


def check_vm(content: str, ssot: dict) -> list:
    findings = []
    vm = ssot["vision_mission"]

    # Forbidden stale drafts
    for forbidden in vm.get("stale_drafts_forbidden", []):
        if forbidden in content:
            idx = content.find(forbidden)
            findings.append({
                "category": "vm_stale_draft",
                "severity": "P0",
                "line": line_of(content, idx),
                "message": f"Stale V/M draft: '{forbidden[:60]}...'",
                "matched": forbidden[:80],
            })

    # If file mentions Vision concepts, expect canonical substrings
    has_vision_ctx = bool(re.search(r"\b[Vv]ision\b|วิสัยทัศน์|🌟 Vision", content))
    has_mission_ctx = bool(re.search(r"\b[Mm]ission\b|พันธกิจ|🎯 Mission", content))

    if has_vision_ctx:
        required = vm["vision"]["en_required_substrings"]
        present = [r for r in required if r in content]
        if len(present) == 0:
            findings.append({
                "category": "vm_vision_canonical_missing",
                "severity": "P1",
                "message": (
                    "Vision is referenced but ZERO canonical substrings present. "
                    f"Expected one of: {required}"
                ),
            })

    if has_mission_ctx:
        required = vm["mission"]["en_required_substrings"]
        present = [r for r in required if r in content]
        if len(present) == 0:
            findings.append({
                "category": "vm_mission_canonical_missing",
                "severity": "P1",
                "message": (
                    "Mission is referenced but ZERO canonical substrings present. "
                    f"Expected one of: {required}"
                ),
            })

    return findings


def check_agent_count(content: str, ssot: dict) -> list:
    """Detect stale 'N agents/Agents/คน' in TEXT (not coords/IDs/colors).

    False-positives we must AVOID:
      - Tier 6 ID range "#53–#62"
      - Agent #62 = DRE literal id
      - Hex colors (#dc2626 etc.)
      - SVG coords (cy="62", points="...50,62..." etc.)
      - Chart data values
    """
    findings = []
    canonical = ssot["agent_roster"]["total"]
    stale_counts = ssot["agent_roster"]["stale_counts_forbidden"]

    for stale in stale_counts:
        s = str(stale)
        # Patterns that ONLY match prose contexts (not numeric attributes/coords)
        patterns = [
            (rf"\b{s}\s+(AI\s+)?[Aa]gents?\b", f"'{s} agent(s)' in text"),
            (rf"\b{s}\s+คน\s+·\s+[Aa]gent", f"'{s} คน · Agent' in text"),
            (rf"ทีม\s+AI\s+{s}\s+คน", f"'ทีม AI {s} คน'"),
            (rf"แผนผังองค์กร\s*\({s}\)", f"'แผนผังองค์กร ({s})'"),
            (rf"แผนผังองค์กร\s*\({s}\s+[Aa]gents?", f"'แผนผังองค์กร ({s} Agents'"),
            (rf"\b{s}-[Aa]gent\b", f"'{s}-Agent' compound"),
            (rf"\bRoster\s+{s}\b", f"'Roster {s}'"),
            (rf"\b{s}\s+persona\b", f"'{s} persona'"),
            (rf"EXECUTION\s*·\s*{s}\s+[Aa]gents?", f"EXECUTION · {s} agents badge"),
            (rf">{s}<\s*</text>", f"SVG text '>{s}<' (probable agent count label)"),
        ]
        for pattern, desc in patterns:
            for m in re.finditer(pattern, content):
                findings.append({
                    "category": "agent_count_stale",
                    "severity": "P0",
                    "line": line_of(content, m.start()),
                    "message": f"Stale agent count: {desc} (canonical = {canonical})",
                    "matched": m.group(0),
                })

    return findings


def check_ecosystem(content: str, ssot: dict) -> list:
    findings = []
    canonical = ssot["ecosystem"]["total_ventures"]
    stale = ssot["ecosystem"].get("stale_counts_forbidden", [])
    for s_int in stale:
        s = str(s_int)
        patterns = [
            (rf"\b{s}\s+ventures?\b", f"'{s} ventures'"),
            (rf"\b{s}\s+ธุรกิจในเครือ\b", f"'{s} ธุรกิจในเครือ'"),
            (rf"\bEcosystem\s+{s}\b", f"'Ecosystem {s}'"),
            (rf"\becosystem-{s}\b", f"'ecosystem-{s}'"),
        ]
        for pattern, desc in patterns:
            for m in re.finditer(pattern, content):
                findings.append({
                    "category": "ecosystem_count_stale",
                    "severity": "P0",
                    "line": line_of(content, m.start()),
                    "message": f"Stale ecosystem count: {desc} (canonical = {canonical})",
                    "matched": m.group(0),
                })
    return findings


def check_hot_rules(content: str, ssot: dict) -> list:
    """C6 (I-NEW-14 · K.22) · Hot Rules Drift Detector.

    Detects Hot Rule count drift in consumer files.

    Per-file checks:
      - Intra-file drift: multiple `\d+ Hot Rules?` values in the same file
      - Canonical mismatch: count differs from SSOT.hot_rules.count (if defined)

    Cross-file aggregation (in main()) emits an additional P1 if multiple
    distinct counts exist across the workspace.
    """
    findings = []
    canonical = ssot.get("hot_rules", {}).get("count")
    pattern = r"\b(\d+)\s+Hot\s+Rules?\b"

    counts_found = []
    for m in re.finditer(pattern, content):
        n = int(m.group(1))
        counts_found.append((n, m.start(), m.group(0)))

    if not counts_found:
        return findings

    unique = sorted({n for n, _, _ in counts_found})

    # Intra-file drift
    if len(unique) > 1:
        findings.append({
            "category": "hot_rules_drift_intrafile",
            "severity": "P1",
            "message": (
                f"Hot Rule count drift WITHIN file: {unique}. "
                f"Pick one canonical count and update all references."
            ),
            "matched": str(unique),
        })

    # Canonical mismatch (only when SSOT defines a count)
    if canonical is not None:
        for n, idx, raw in counts_found:
            if n != canonical:
                findings.append({
                    "category": "hot_rules_count_stale",
                    "severity": "P1",
                    "line": line_of(content, idx),
                    "message": (
                        f"Stale Hot Rule count: '{raw}' "
                        f"(canonical = {canonical} per SSOT)"
                    ),
                    "matched": raw,
                })

    return findings


def check_vm_anchors_full(content: str, ssot: dict) -> list:
    """C7 (I-NEW-19 · K.22) · V/M Anchor Full Check (1 → 6 anchors).

    Upgrade of C1 (check_vm). Where C1 only flags ZERO-substring presence,
    C7 flags PARTIAL canonical:

      Vision: 3 substrings ('Human wisdom', 'AI at scale', 'Wisdom for everyone')
      Mission: 3 substrings ('Empower people', 'Build sustainable businesses',
                              'Scale crafted AI to the world')
      Total: 6 anchors per canonical V/M block

    Rules:
      - 1 ≤ vision_present < 3      → P1 partial-vision
      - 1 ≤ mission_present < 3     → P1 partial-mission
      - vision_present == 3 AND     → P2 advisory (file hosts canonical Vision
        mission_present == 0          but no Mission · likely intentional hero
                                      banner · advisory only)
      - vision_present == 3 AND     → P1 inconsistent (file partially hosts
        0 < mission_present < 3       canonical block)
    """
    findings = []
    vm = ssot["vision_mission"]
    vision_subs = vm["vision"]["en_required_substrings"]
    mission_subs = vm["mission"]["en_required_substrings"]

    vision_present = [s for s in vision_subs if s in content]
    mission_present = [s for s in mission_subs if s in content]

    nv, nm = len(vision_present), len(mission_present)
    Nv, Nm = len(vision_subs), len(mission_subs)

    # Partial Vision (1 or 2 of 3)
    if 0 < nv < Nv:
        missing = [s for s in vision_subs if s not in content]
        findings.append({
            "category": "vm_vision_anchors_partial",
            "severity": "P1",
            "message": (
                f"Vision is PARTIALLY canonical ({nv}/{Nv}). "
                f"Missing substrings: {missing}"
            ),
        })

    # Partial Mission (1 or 2 of 3)
    if 0 < nm < Nm:
        missing = [s for s in mission_subs if s not in content]
        findings.append({
            "category": "vm_mission_anchors_partial",
            "severity": "P1",
            "message": (
                f"Mission is PARTIALLY canonical ({nm}/{Nm}). "
                f"Missing substrings: {missing}"
            ),
        })

    # File hosts FULL Vision but inconsistent Mission
    if nv == Nv and 0 < nm < Nm:
        findings.append({
            "category": "vm_block_inconsistent",
            "severity": "P1",
            "message": (
                f"File hosts canonical Vision ({Nv}/{Nv}) but Mission is "
                f"{nm}/{Nm} — likely partial canonical V/M block. "
                f"Either complete Mission to {Nm}/{Nm} or remove Mission refs."
            ),
        })

    # File hosts FULL Vision but ZERO Mission (advisory)
    if nv == Nv and nm == 0:
        # Most operational consumer files should have BOTH; advise but don't fail
        findings.append({
            "category": "vm_block_vision_only",
            "severity": "P2",
            "message": (
                "File hosts canonical Vision but NO Mission substrings — "
                "likely hero banner or partial reference. Consider adding "
                "Mission for full canonical V/M block."
            ),
        })

    return findings


def check_op_count(content: str, ssot: dict) -> list:
    findings = []
    canonical = ssot["operating_principles"]["count"]
    stale_op_counts = [11, 13]  # pre-Apr-26 stales
    for s_int in stale_op_counts:
        if s_int == canonical:
            continue
        s = str(s_int)
        pattern = rf"\b{s}\s+Operating\s+Principles?\b"
        for m in re.finditer(pattern, content):
            findings.append({
                "category": "op_count_stale",
                "severity": "P1",
                "line": line_of(content, m.start()),
                "message": f"Stale Op Principle count: '{m.group(0)}' (canonical = {canonical})",
                "matched": m.group(0),
            })
    return findings


def strip_history_blocks(content: str) -> str:
    """Replace update_history block content with whitespace-only lines.

    Preserves line numbers (each removed line replaced by ''), so findings
    on body content still report accurate line numbers.

    Strips:
      1. YAML frontmatter `update_history:` list (MD files: between ---...---)
      2. HTML comment frontmatter blocks containing `update_history:`
      3. Standalone YAML `update_history:` blocks not inside frontmatter

    Why: I-NEW-10 (29 Apr 2026 K.12) — update_history entries legitimately
    document historical states (e.g., "62 → 63" or "29 ventures (R9 baseline)")
    and were causing P0 false-positives in K.12 closeout. Op 16 SSOT discipline
    requires lint to focus on body content, NOT historical metadata.
    """
    # --- Strategy 1: Strip HTML comment blocks containing update_history: ---
    # Pattern: <!-- ... update_history: ... --> (multiline)
    def _blank_html_comment(m):
        # Replace with same number of newlines to preserve line numbers
        return "\n" * m.group(0).count("\n")

    content = re.sub(
        r"<!--[^>]*?update_history:[^>]*?-->",
        _blank_html_comment,
        content,
        flags=re.DOTALL,
    )

    # --- Strategy 2: Strip MD YAML frontmatter update_history list ---
    # Pattern: in YAML block (---...---), update_history: followed by
    # indented `- "..."` lines until a non-indented line OR end of block
    fm_match = re.match(r"^(---\n)(.*?)(\n---\n)", content, re.DOTALL)
    if fm_match:
        prefix, fm_body, suffix = fm_match.group(1), fm_match.group(2), fm_match.group(3)
        # Find update_history: block within frontmatter
        # Match: "update_history:\n" followed by lines starting with whitespace+dash OR continuation
        def _blank_yaml_history(m):
            return m.group(1) + "\n" * m.group(2).count("\n")

        # Simple pattern: update_history: followed by any indented (≥1 space/tab) line.
        # Handles last line without trailing \n (frontmatter capture trims it).
        fm_body_clean = re.sub(
            r"(update_history:\s*\n)((?:[ \t]+[^\n]*(?:\n|$))+)",
            _blank_yaml_history,
            fm_body,
            flags=re.MULTILINE,
        )
        content = prefix + fm_body_clean + suffix + content[fm_match.end():]

    # --- Strategy 3: Strip standalone Update history sections in MD body ---
    # Pattern: ## Update history\n followed by - bullet list until next ## or EOF
    def _blank_md_history(m):
        return m.group(1) + "\n" * m.group(2).count("\n")

    content = re.sub(
        r"(##\s+Update\s+history\s*\n)((?:[ \t]*-[^\n]*\n|[ \t]*\n)+)",
        _blank_md_history,
        content,
        flags=re.IGNORECASE,
    )

    return content


def lint_file(path: Path, ssot: dict) -> list:
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return [{
            "category": "read_error",
            "severity": "ERROR",
            "message": f"Failed to read: {e}",
        }]
    # I-NEW-10 (29 Apr K.12): strip update_history blocks before lint checks
    # to prevent false positives from historical refs documented in metadata
    scan_content = strip_history_blocks(content)
    findings = []
    findings.extend(check_vm(scan_content, ssot))                 # C1
    findings.extend(check_agent_count(scan_content, ssot))        # C2
    findings.extend(check_ecosystem(scan_content, ssot))          # C3
    findings.extend(check_op_count(scan_content, ssot))           # C4 (Op Principles)
    # C5 = strip_history_blocks (preprocessor · I-NEW-10)
    findings.extend(check_hot_rules(scan_content, ssot))          # C6 (I-NEW-14 · K.22)
    findings.extend(check_vm_anchors_full(scan_content, ssot))    # C7 (I-NEW-19 · K.22)
    return findings


def write_reports(report_data: dict):
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    today = report_data["date"]
    md_path = REPORTS_DIR / f"DAS-Sweep-Report-{today}.md"
    json_path = REPORTS_DIR / f"DAS-Sweep-Report-{today}.json"

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# DAS Sweep Report — {today}\n\n")
        f.write(f"**Files scanned:** {report_data['files_scanned']}  \n")
        f.write(f"**Files with findings:** {report_data['files_with_findings']}  \n")
        f.write(f"**Total defects:** P0={report_data['total_p0']} · P1={report_data['total_p1']}\n\n")
        f.write(f"_Generated by_ `/scripts/vm-canonical-lint.py` · "
                f"_SSOT_ `/canonical/vm-status.json`\n\n")
        if report_data["files_with_findings"] == 0:
            f.write("## ✅ ALL CLEAN\n\nNo canonical-fact divergences found.\n")
        else:
            f.write("## Findings by File\n\n")
            for rel, findings in report_data["findings"].items():
                f.write(f"### 📄 `{rel}`\n\n")
                for fi in findings:
                    line_info = f" (L{fi['line']})" if fi.get("line") else ""
                    f.write(f"- **[{fi['severity']}{line_info}]** {fi['message']}\n")
                    if fi.get("matched"):
                        f.write(f"  - Matched: `{fi['matched']}`\n")
                f.write("\n")
        f.write("\n---\n\n")
        f.write("## ARAI · DAS Sweep\n\n")
        f.write(f"- **Action:** Ran `vm-canonical-lint.py` against {report_data['files_scanned']} consumer files\n")
        if report_data['total_p0'] + report_data['total_p1'] == 0:
            f.write("- **Result:** ✅ Zero defects · all canonical facts aligned\n")
        else:
            f.write(f"- **Result:** {report_data['total_p0']} P0 + {report_data['total_p1']} P1 defects surfaced · listed above\n")
        f.write("- **Idea:** Schedule next sweep Monday 09:00 ICT (#63 FJA-CDCA) · auto-emit Slack/Teams alert if defects > 0\n")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)

    return md_path, json_path


def main():
    args = sys.argv[1:]
    json_only = "--json" in args
    strict = "--strict" in args
    no_report = "--no-report" in args
    args = [a for a in args if not a.startswith("--")]

    ssot = load_ssot()

    if args:
        target = Path(args[0]).resolve()
        if not target.exists():
            print(f"{R}ERROR: {target} not found{N}", file=sys.stderr)
            sys.exit(2)
        files = collect_files(target, ssot)
    else:
        files = collect_files(WORKSPACE, ssot)

    all_findings = {}
    total_p0, total_p1, total_err = 0, 0, 0

    for path in files:
        findings = lint_file(path, ssot)
        if findings:
            try:
                rel = str(path.relative_to(WORKSPACE)).replace(os.sep, "/")
            except ValueError:
                rel = str(path)
            all_findings[rel] = findings
            total_p0 += sum(1 for f in findings if f["severity"] == "P0")
            total_p1 += sum(1 for f in findings if f["severity"] == "P1")
            total_err += sum(1 for f in findings if f["severity"] == "ERROR")

    today = date.today().isoformat()
    report_data = {
        "date": today,
        "files_scanned": len(files),
        "files_with_findings": len(all_findings),
        "total_p0": total_p0,
        "total_p1": total_p1,
        "total_errors": total_err,
        "findings": all_findings,
    }

    if json_only:
        print(json.dumps(report_data, ensure_ascii=False, indent=2))
    else:
        # Terminal pretty-print
        print(f"\n{B}━━━ DAS Sweep · {today} ━━━{N}")
        print(f"{DIM}SSOT:{N} {SSOT_PATH.relative_to(WORKSPACE)}")
        print(f"{DIM}Scope:{N} {len(files)} files (HTML+MD · exempt paths skipped)\n")
        if not all_findings:
            print(f"{G}✅ ALL CLEAN — no canonical-fact divergences found{N}\n")
        else:
            for rel, findings in all_findings.items():
                print(f"{B}📄 {rel}{N}")
                for fi in findings:
                    color = R if fi["severity"] == "P0" else (Y if fi["severity"] == "P1" else DIM)
                    line_info = f" L{fi['line']}" if fi.get("line") else ""
                    print(f"  {color}[{fi['severity']}{line_info}]{N} {fi['message']}")
                    if fi.get("matched"):
                        print(f"    {DIM}→ '{fi['matched']}'{N}")
                print()
            print(f"Total: {R}P0={total_p0}{N} · {Y}P1={total_p1}{N}\n")

        if not no_report:
            md_path, json_path = write_reports(report_data)
            print(f"{DIM}📝 Reports:{N}")
            print(f"   {md_path.relative_to(WORKSPACE)}")
            print(f"   {json_path.relative_to(WORKSPACE)}\n")

    if strict and (total_p0 > 0 or total_p1 > 0 or total_err > 0):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
