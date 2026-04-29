# `/scripts/` — Direction Alignment Sweep (DAS) Toolkit

Tools for preventing V/M, agent count, ecosystem, and operating-principle drift across operational files. Owned by **Agent #63 FJA-CDCA** (Tier 5 sweep agent · early-activated 28 Apr 2026).

## Files

| File | Idea | Purpose |
|---|---|---|
| `vm-canonical-lint.py` | I-NEW-1 | Python DAS lint script. Reads `/canonical/vm-status.json` SSOT, scans HTML/MD, reports defects. |
| `pre-edit-lint.sh` | I-NEW-2 | Bash gate wrapper. Block save/commit on V/M divergence. |
| `README.md` | — | This file. |

## Quick start

```bash
# Full workspace sweep (writes report to /reports/DAS-Sweep-Report-YYYY-MM-DD.{md,json})
python3 scripts/vm-canonical-lint.py

# Lint a single file
python3 scripts/vm-canonical-lint.py command-center/ANTS-2.0-Unified-Command-Center.html

# Strict mode (exits 1 on defects · for hooks)
python3 scripts/vm-canonical-lint.py --strict

# JSON-only output (machine pipeline)
python3 scripts/vm-canonical-lint.py --json

# Pre-edit gate (manual · before saving an HTML/MD)
scripts/pre-edit-lint.sh path/to/file.html
```

## Activate as git pre-commit hook

```bash
chmod +x scripts/pre-edit-lint.sh scripts/vm-canonical-lint.py

# In a git repo:
cat > .git/hooks/pre-commit <<'EOF'
#!/usr/bin/env bash
exec "$(git rev-parse --show-toplevel)/scripts/pre-edit-lint.sh" --staged
EOF
chmod +x .git/hooks/pre-commit
```

## What it checks (canonical = `/canonical/vm-status.json`)

1. **V/M canonical strings** — Vision/Mission must contain canonical English substrings when the file references them
2. **V/M stale drafts** — forbidden draft phrases (e.g., "AI-Native Partner for SEA", "เป็นบริษัท Technology & Consulting...")
3. **Agent count** — text "62 agents" / "52 agents" / etc. forbidden (canonical = 63)
4. **Ecosystem count** — text "29 ventures" forbidden (canonical = 27)
5. **Operating Principles count** — text "11/13 Operating Principles" forbidden (canonical = 16)

## What it does NOT flag (false positives intentionally allowed)

- Tier 6 ID range `#53–#62` — accurate (10 agents)
- Agent #62 = DRE literal ID
- Hex colors `#dc2626`, `#6264a7`
- SVG coordinates `cy="62"`, `width="62"`, polyline points
- Chart data `[62, 45, 38, 55]`

The script uses pattern context (looking for "agents", "คน", "Agent", "persona", "Roster", "EXECUTION ·") to avoid false positives.

## Exempt paths (not scanned)

Configured in `vm-status.json` `exempt_paths`:

- `/archive/` — superseded files preserved intentionally
- `/foundational-apr17/` — frozen early docs
- `/launches/` — event-snapshot artifacts
- `/founder-story/` — different rhetorical conventions
- `/canonical/` — SSOT itself
- `/scripts/` — tooling

## Output

| Location | Format | Audience |
|---|---|---|
| stdout (terminal) | colored text | human · interactive |
| `/reports/DAS-Sweep-Report-{date}.md` | markdown | human · review |
| `/reports/DAS-Sweep-Report-{date}.json` | JSON | machine · CI/dashboard |

## Schedule

- **Mondays 09:00 ICT** — automated weekly sweep (#63 FJA-CDCA)
- **On-demand** — invoked manually after major edits
- **Pre-commit hook** — every commit (if hook installed)

## Update protocol (Op Principle 16 — Pattern A)

Any change to canonical facts MUST update **both** `vm-status.json` AND `canonical-facts.md` atomically. Then re-run `vm-canonical-lint.py` to confirm consumer files still align.

## Linked Ideas

- I-NEW-1 — this script (`vm-canonical-lint.py`)
- I-NEW-2 — gate wrapper (`pre-edit-lint.sh`)
- I-NEW-3 — `/canonical/vm-status.json` SSOT
- I-NEW-5 — `/canonical/canonical-facts.md` companion
- I-NEW-4 — Op 12 CC walk-through (executes deeper section-by-section panel review)

## Owner & escalation

- **Primary:** Agent #63 FJA-CDCA (Tier 5)
- **Build:** Agent #21 HoEng (Engineering)
- **Schema:** Agent #51 KM (Knowledge Management)
- **QA:** Agent #31 SDET
- **Layer-2 review:** เฌอคูณ (CWO)

---

_Crafted with wisdom, scaled with AI · เฌอคูณ · 28 Apr 2026_
