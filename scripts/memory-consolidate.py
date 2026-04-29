#!/usr/bin/env python3
"""
memory-consolidate.py — Memory Consolidation Cron · I-NEW-18 · K.22

Scans the auto-memory directory and detects:
  - Orphans: memory files NOT referenced in MEMORY.md index
  - Index leaks: MEMORY.md entries pointing to files that no longer exist
  - Duplicate candidates: filename + name-frontmatter similarity ≥ 0.75
  - Stale projects: type=project files older than --stale-days (default 30)
  - Oversized index: MEMORY.md > 24.4KB (loaded portion may truncate)

Output: advisory report — does NOT auto-merge or auto-delete.
Owner #51 KM + #63 FJA-CDCA · weekly cron Mondays 09:30 ICT (after DAS sweep)

Usage:
  python3 memory-consolidate.py                              # default scan
  python3 memory-consolidate.py --memory-dir <path>          # custom dir
  python3 memory-consolidate.py --stale-days 45              # adjust threshold
  python3 memory-consolidate.py --json                       # JSON to stdout
  python3 memory-consolidate.py --strict                     # exit 1 on findings
"""

import argparse
import json
import os
import re
import sys
from datetime import date, datetime, timedelta
from difflib import SequenceMatcher
from pathlib import Path

DEFAULT_MEMORY_DIR_CANDIDATES = [
    Path.home() / "Library" / "Application Support" / "Claude" / "local-agent-mode-sessions",
    Path("/sessions/stoic-friendly-allen/mnt/.auto-memory"),
]

INDEX_FILE = "MEMORY.md"
INDEX_LIMIT_BYTES = 24576  # 24KB soft limit before truncation
DEFAULT_STALE_DAYS = 30
SIMILARITY_THRESHOLD = 0.75


def find_memory_dir(explicit: Path = None) -> Path:
    if explicit:
        if not explicit.exists():
            print(f"❌ Memory dir does not exist: {explicit}", file=sys.stderr)
            sys.exit(2)
        return explicit
    # Search known locations
    for c in DEFAULT_MEMORY_DIR_CANDIDATES:
        if c.exists() and (c / INDEX_FILE).exists():
            return c
        # Recurse one level (session UUID layouts)
        if c.exists() and c.is_dir():
            for sub in c.rglob(INDEX_FILE):
                return sub.parent
    print("❌ Could not locate memory directory. Pass --memory-dir.", file=sys.stderr)
    sys.exit(2)


def parse_index(index_path: Path) -> dict:
    """Parse MEMORY.md index — return {filename: line_text}"""
    refs = {}
    if not index_path.exists():
        return refs
    text = index_path.read_text(encoding="utf-8", errors="replace")
    for ln in text.splitlines():
        m = re.search(r"\(([A-Za-z0-9_\-\.]+\.md)\)", ln)
        if m:
            refs[m.group(1)] = ln.strip()
    return refs


def parse_frontmatter(file_path: Path) -> dict:
    """Extract YAML frontmatter (name, type, description)."""
    fm = {}
    try:
        text = file_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return fm
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return fm
    body = m.group(1)
    for ln in body.splitlines():
        kv = re.match(r"^([a-zA-Z_]+):\s*(.*)$", ln)
        if kv:
            fm[kv.group(1).strip()] = kv.group(2).strip().strip('"').strip("'")
    return fm


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def detect_duplicates(files: list, threshold: float) -> list:
    """Return list of (file_a, file_b, score, reason) tuples."""
    pairs = []
    n = len(files)
    for i in range(n):
        a = files[i]
        for j in range(i + 1, n):
            b = files[j]
            # 1. Filename stem similarity
            sa, sb = a["path"].stem, b["path"].stem
            score_filename = similarity(sa, sb)
            # 2. Frontmatter name similarity (if both have names)
            score_name = 0.0
            if a["fm"].get("name") and b["fm"].get("name"):
                score_name = similarity(a["fm"]["name"], b["fm"]["name"])
            best = max(score_filename, score_name)
            if best >= threshold:
                # Skip same-prefix series files (project_K20.1 vs project_K20.2 — intentional)
                if re.search(r"K\d+(\.\d+)?_", sa) and re.search(r"K\d+(\.\d+)?_", sb):
                    if abs(int(re.search(r"K(\d+)", sa).group(1)) - int(re.search(r"K(\d+)", sb).group(1))) <= 1:
                        continue
                # Skip same-prefix idea improvements series
                if re.search(r"I_NEW_\d+", sa) and re.search(r"I_NEW_\d+", sb):
                    continue
                # Skip op_principle_N series (different OPs, intentionally separate)
                if re.search(r"op_principle_\d+", sa) and re.search(r"op_principle_\d+", sb):
                    continue
                # Skip K_x series (project_Kxx_yyy vs project_Kyy_zzz — different sweeps)
                if re.search(r"^project_K\d+", sa) and re.search(r"^project_K\d+", sb):
                    continue
                # Skip idea_improvement_I<N>_command (different commands · sister files)
                if re.search(r"idea_improvement_I\d+_", sa) and re.search(r"idea_improvement_I\d+_", sb):
                    continue
                # Skip idea_improvements_* prose-similar series (I_NEW_N_to_M ranges)
                if re.search(r"idea_improvements?_I", sa) and re.search(r"idea_improvements?_I", sb):
                    continue
                pairs.append({
                    "file_a": a["path"].name,
                    "file_b": b["path"].name,
                    "score": round(best, 3),
                    "reason": "filename_sim" if score_filename >= score_name else "name_frontmatter_sim",
                })
    return pairs


def main():
    p = argparse.ArgumentParser(description="Memory Consolidation Cron · I-NEW-18 · K.22")
    p.add_argument("--memory-dir", type=Path, default=None)
    p.add_argument("--stale-days", type=int, default=DEFAULT_STALE_DAYS)
    p.add_argument("--threshold", type=float, default=SIMILARITY_THRESHOLD)
    p.add_argument("--json", action="store_true", help="JSON output to stdout")
    p.add_argument("--strict", action="store_true", help="exit 1 if any findings")
    p.add_argument("--no-report", action="store_true", help="skip writing report file")
    args = p.parse_args()

    mem_dir = find_memory_dir(args.memory_dir)
    index_path = mem_dir / INDEX_FILE

    # 1. Collect ALL .md filenames on disk (for orphan/leak comparison)
    all_on_disk = {f.name for f in mem_dir.glob("*.md")}
    # Files we analyze deeply (skip index + handoff brief)
    skip = {INDEX_FILE, "SESSION_HANDOFF.md"}
    md_files = []
    for f in sorted(mem_dir.glob("*.md")):
        if f.name in skip:
            continue
        fm = parse_frontmatter(f)
        md_files.append({
            "path": f,
            "fm": fm,
            "mtime": datetime.fromtimestamp(f.stat().st_mtime),
            "size": f.stat().st_size,
        })

    # 2. Parse index
    index_refs = parse_index(index_path)
    index_size = index_path.stat().st_size if index_path.exists() else 0

    # 3. Detect orphans (files NOT in index · use full on-disk set · skip handoff/index)
    analyzable_on_disk = all_on_disk - skip
    orphans = sorted(analyzable_on_disk - set(index_refs.keys()))

    # 4. Detect index leaks (entries pointing to missing files · check vs ALL on-disk)
    leaks = sorted(set(index_refs.keys()) - all_on_disk)

    # 5. Detect duplicate candidates
    duplicates = detect_duplicates(md_files, args.threshold)

    # 6. Stale project files
    cutoff = datetime.now() - timedelta(days=args.stale_days)
    stale = []
    for f in md_files:
        if f["fm"].get("type", "") == "project" and f["mtime"] < cutoff:
            stale.append({
                "file": f["path"].name,
                "age_days": (datetime.now() - f["mtime"]).days,
                "name": f["fm"].get("name", ""),
            })

    # 7. Index size warning
    index_oversized = index_size > INDEX_LIMIT_BYTES

    # 8. Assemble report
    report = {
        "schema": "memory-consolidate-v1",
        "date": date.today().isoformat(),
        "memory_dir": str(mem_dir),
        "totals": {
            "md_files": len(md_files),
            "index_entries": len(index_refs),
            "orphans": len(orphans),
            "leaks": len(leaks),
            "duplicates": len(duplicates),
            "stale_projects": len(stale),
            "index_size_bytes": index_size,
            "index_oversized": index_oversized,
        },
        "orphans": orphans,
        "leaks": leaks,
        "duplicates": duplicates,
        "stale_projects": stale,
    }

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"📂 Memory dir: {mem_dir}")
        print(f"📊 {len(md_files)} files · {len(index_refs)} index entries · index {index_size}B")
        print()
        if orphans:
            print(f"🟡 Orphans ({len(orphans)}) — files NOT in MEMORY.md index:")
            for o in orphans[:20]:
                print(f"   - {o}")
            if len(orphans) > 20:
                print(f"   ... +{len(orphans) - 20} more")
            print()
        if leaks:
            print(f"🔴 Index leaks ({len(leaks)}) — entries pointing to MISSING files:")
            for l in leaks:
                print(f"   - {l}")
            print()
        if duplicates:
            print(f"🟡 Duplicate candidates ({len(duplicates)}) — score ≥ {args.threshold}:")
            for d in duplicates[:15]:
                print(f"   {d['score']:.2f}  {d['file_a']}  ↔  {d['file_b']}  ({d['reason']})")
            if len(duplicates) > 15:
                print(f"   ... +{len(duplicates) - 15} more")
            print()
        if stale:
            print(f"🟡 Stale projects ({len(stale)}) — older than {args.stale_days} days:")
            for s in stale[:10]:
                print(f"   {s['age_days']:>3}d  {s['file']}")
            if len(stale) > 10:
                print(f"   ... +{len(stale) - 10} more")
            print()
        if index_oversized:
            print(f"🔴 Index oversized: {index_size}B > {INDEX_LIMIT_BYTES}B soft limit")
            print(f"   → MEMORY.md may truncate on load. Shorten line entries.")
            print()
        total_findings = len(orphans) + len(leaks) + len(duplicates) + len(stale)
        if total_findings == 0 and not index_oversized:
            print("✅ All clean.")
        else:
            print(f"📝 Total advisory findings: {total_findings}"
                  + (" (+ index oversized)" if index_oversized else ""))

    # 9. Write report file (unless --no-report)
    if not args.no_report:
        try:
            workspace_root = Path(__file__).resolve().parent.parent
            reports_dir = workspace_root / "reports"
            reports_dir.mkdir(parents=True, exist_ok=True)
            json_out = reports_dir / f"Memory-Consolidate-Report-{date.today()}.json"
            json_out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
            if not args.json:
                print(f"\n📝 Report: {json_out}")
        except Exception as e:
            print(f"⚠️  Could not write report: {e}", file=sys.stderr)

    if args.strict:
        total = len(orphans) + len(leaks) + len(duplicates) + len(stale)
        sys.exit(1 if (total > 0 or index_oversized) else 0)


if __name__ == "__main__":
    main()
