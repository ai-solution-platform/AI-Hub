<!--
last_updated: 2026-04-29
version: 1.2
update_history:
  - "v1.0 (24 Apr 2026): Post-reorganization README · folder map · 14 memories"
  - "v1.1 (28 Apr 2026 LATE-AM): Op 17 Naming Convention applied · 11 consumer files renamed (clean operational names)"
  - "v1.2 (29 Apr 2026 K.12 re-audit): §Folder Map +/scripts/ +/canonical/ rows · §Folder Map /internal-transformation/ row updated to mention SAKM v1 (replaced stale Layer-3c pitching-mode reference) · §Must-Read memory count 32+→60+ · §Canonical Files +Hub-Index v1.2 · §Operating Principles 10-summary→18-full (added Op14/15/16/17/18) · §File Governance Agent #63 activation status (was 'to be activated' → 'activated 28 Apr 2026') · §Tools section NEW (lint, gate, das-bulk-fix scripts)"
-->
# ANTS 2.0 — AI Command Center

**HQ:** Bangkok · **Founder/CEO:** Nut · **Master Persona:** เฌอคูณ (Cherkun) — CWO
**Roster:** 65 AI Agents (Tier 1–6 + #63 FJA-CDCA sweep) · **Last Reorganized:** 24 Apr 2026 · **Last Re-Audited:** 29 Apr 2026 (K.12 body-level)

---

## 🗺️ Folder Map (Canonical — Post 24 Apr 2026)

| Folder | Purpose | Key Files |
|---|---|---|
| `/agents/` | Agent specs & rosters | Tier 6 Frontier Elite Specs |
| `/archive/` | Superseded / historical versions | 2026-04/, patches/ |
| `/command-center/` | Live unified dashboard | **v2.2** (canonical) |
| `/products/` | Product-facing assets | **AI Solutions Stack v4** (canonical) |
| `/reports/` | Audits, dashboards, analyses | Master Audit + Idea Improvements |
| `/founder-story/` | Nut's narrative assets | Script, OpenQ, W2 Assets |
| `/vm-qa-gate/` | Vision & Mission QA Gate | v1 + Install Package |
| `/internal-transformation/` | Employee upskill/reskill + Shadow Agent system | Communication Plan · **SAKM v1 MasterSpec** (28 Apr) · Sales-Pilot Agent Matrix · Cultural Manifesto "Impossible → I'm possible" |
| `/launches/` | Launch assets by event | post-songkran-20apr/ |
| `/foundational-apr17/` | Early foundational docs (Apr 17) | 9 files |
| `/ecosystem/` | 27-Venture ecosystem (R10) | Dashboard + supporting |
| `/morning-briefs/` | Daily morning briefs | — |
| `/canonical/` | SSOT registry pair (Op 16) | `vm-status.json` (machine) + `canonical-facts.md` (human) — v1.1 / 29 Apr |
| `/scripts/` | Tooling (DAS lint + Pre-Edit gate + bulk-fix + Op-18 sync-check) | `vm-canonical-lint.py` · `pre-edit-lint.sh` · `das-bulk-fix.py` · `hub-index-sync-check.py` (I-NEW-9) |

---

## 📌 Must-Read for Any Agent Starting a New Session

1. **`SESSION_HANDOFF.md`** (memory · continuity brief — read FIRST every session per Op 13)
2. **`MEMORY.md`** (memory index · 60+ memories)
3. **[FILE-MOVEMENT-MANIFEST-24Apr2026.md](./FILE-MOVEMENT-MANIFEST-24Apr2026.md)** ← path truth (append-only)
4. **`reference_file_paths_registry.md`** (memory · canonical path index)
5. **`/canonical/canonical-facts.md`** ⭐ SSOT (human) — single source of truth for V/M, agent count, ecosystem, OP count
6. **`/canonical/vm-status.json`** ⭐ SSOT (machine) — JSON twin · scripts parse this
7. **`/internal-transformation/ANTS-SAKM-MasterSpec.md`** ⭐ NEW (28 Apr) — Shadow Agent Knowledge Mesh v1

---

## 🎯 Canonical Files (Use These · Not the Archive)

| Concept | Path |
|---|---|
| Unified Command Center | `/command-center/ANTS-2.0-Unified-Command-Center.html` (v2.5 · K.13 audit folded) |
| Hub-Index Portal | `/ANTS-2.0-Hub-Index.html` (v1.5 · 27 Apr · K.14) |
| AI Solutions Stack | `/products/ANTS-2.0-AI-Solutions-Stack.html` |
| Master Audit Report | ⚠️ **FOLDED into Command Center K.13** · archived to `/archive/2026-04/master-audit-folded-into-CC/` · open CC tabs (Exec · Roadmap · Risks) instead |
| Audit Dashboard | ⚠️ **FOLDED into Command Center K.14** · archived to `/archive/2026-04/audit-dashboard-folded-into-CC-K14/` · open CC tabs instead |
| GitHub Setup Guide | `/GITHUB-SETUP.md` (NEW K.14 · 5-step team publish guide) |
| Tier 6 Agent Specs | `/agents/ANTS-Tier6-Frontier-Elite-Agents.md` |
| SAKM v1 MasterSpec | `/internal-transformation/ANTS-SAKM-MasterSpec.md` |
| SSOT Registry (pair) | `/canonical/canonical-facts.md` + `vm-status.json` |

---

## 🧭 Operating Principles (18 total · summary — full list in `/canonical/canonical-facts.md` §5)

1. **Wisdom > Intelligence > Data**
2. **AI-Native First** — activate 65 agents before recommending humans (Op 9 sync · Op 10 no drift)
3. **Apple-UX Scale** — body 15.5px, line-height 1.65, antialiased (permanent)
4. **ARAI Closing Block** — every output ends with Actions · Results · Idea Improvement
5. **Op 11** (DEV) → QA Layer-1 + CWO Layer-2
6. **Op 12** (NON-DEV) → Panel Layer-1 + CWO Layer-2 + ARAI block
7. **Op 13** (Session Continuity) → Read `SESSION_HANDOFF.md` first every session
8. **Op 14** (Title Convention) → T2 Exec/P&L · T6 Craft/Research with `(Craft)`/`(Research)` tag
9. **Op 15** (Mid-Session Health Check) → every 3 heavy edits emit 4-line block
10. **Op 16** (Cross-Doc SSOT Discipline) → Pattern A centralize · `/canonical/` pair atomic update
11. **Op 17** (Filename Naming Convention · 28 Apr) → operational filenames stay clean · version+date INSIDE file
12. **Op 18** (Session-Close Sync Discipline · 28 Apr) → Hub-Index sync · body-content updates · Op-18 sign-off block
13. **Default Language** — Thai (เฌอคูณ persona) · English-primary in operational UI for V/M
14. **Activation Syntax** — `[Activated: ...]` prefix every response
15. **HTML ≥150KB × 3 edit rounds** → stop + new session

---

## 🛡️ File Governance

- **Folder Janitor Agent #63 FJA-CDCA** — activated 28 Apr 2026 (early activation · was originally 4 May). Weekly cron Mondays 09:00 ICT + on-demand. 7 sweep targets covering V/M alignment · roster drift · path registry · workflows · workshops · V/M language · OP cross-doc consistency.
- Any file move **must** update `FILE-MOVEMENT-MANIFEST-*.md` with a new dated section (append-only).
- Never delete — always archive to `/archive/YYYY-MM/{category-old}/`.
- Per **Op 17** (28 Apr) — operational/consumer filenames stay clean. No `-v\d`, no `-DDMmmYYYY` suffix on consumer-facing files. Exceptions: `/archive/`, `/founder-story/`, MANIFEST, DAS reports, `/launches/`, `/foundational-apr17/`.

---

## 🛠️ Tools (in `/scripts/`)

| Tool | Purpose | Owner |
|---|---|---|
| `vm-canonical-lint.py` | DAS lint · 4 check categories (V/M strings · agent count · ecosystem · OP count) | I-NEW-1 · 27 Apr |
| `pre-edit-lint.sh` | Pre-save/commit gate · 3 modes (file/--all/--staged) | I-NEW-2 · 27 Apr |
| `das-bulk-fix.py` | Auto-remediation · 3-phase batch (sed P0 + Python P1 + per-file verify) · idempotent | I-NEW-6 · 28 Apr |
| `hub-index-sync-check.py` | Op 18 enforcement · body-diff check (NOT just frontmatter date) | I-NEW-9 · 29 Apr |

---

_Crafted with wisdom, scaled with AI — เฌอคูณ_

---

<!-- Canonical V/M SSOT alignment · auto-injected · do not remove · pair: /canonical/vm-status.json + canonical-facts.md -->

## 📌 Canonical V/M Reference (SSOT)

- **Vision (canonical):** *Human wisdom. AI at scale. Wisdom for everyone.*
- **Mission (canonical):** *Empower people. Build sustainable businesses. Scale crafted AI to the world.*

_Source: `/canonical/canonical-facts.md` + `/canonical/vm-status.json` · Locked Apr 23, 2026 · Op 16 SSOT discipline_
