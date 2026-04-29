---
title: ANTS 2.0 — Canonical Facts Registry (Human-Readable SSOT)
type: canonical-facts-registry
version: 1.3
last_updated: 2026-04-29
owner: Agent #51 KM + Agent #63 FJA-CDCA + CWO Cherkun
pairs_with: ./vm-status.json (machine-readable JSON · same data)
update_protocol: Atomic update with vm-status.json. Op 16 Pattern A.
update_history:
  - "v1.0 (2026-04-27): Initial SSOT registry · 9 sections · 18 forbidden stale strings"
  - "v1.1 (2026-04-29): §5 Operating Principles count corrected 16→18 (added Op 17 Filename Naming Convention + Op 18 Session-Close Sync Discipline · both locked 28 Apr LATE-AM but SSOT not synced until K.12 body-level re-audit). Added '16 Operating Principles' to FORBIDDEN stale counts."
  - "v1.2 (2026-04-27 K.15): §5 Operating Principles count 18→19 (added Op 19 'Always pair abbreviation with full name on first occurrence in consumer-facing files'). Locked from K.14 Nut feedback Issue #5. Added '18 Operating Principles' to FORBIDDEN stale counts."
  - "v1.3 (2026-04-29 K.20): §2 Agent Roster expanded 63 → 65. Added #64 CEcoO (Chief Ecosystem Orchestration Officer · T2 host · Op 14 Orchestration tag) + #65 CDA (Chief Decision Architect & Wisdom Steward · T2 host · Op 14 Steward tag). T2 count 11 → 13. Added '63 agents' to FORBIDDEN stale counts. Trigger: Nut Approve Both decision in Two-Agents-Strategic-Pack-K20."
---

# ANTS 2.0 — Canonical Facts Registry

> **Purpose:** Single human-readable source of truth for every critical fact in ANTS 2.0 workspace. Any agent or human writing prose must `grep` this file (or its JSON twin `vm-status.json`) BEFORE asserting a fact in copy. If a fact appears here and in another file with different wording → other file is wrong.
>
> **Pair:** `./vm-status.json` (machine-readable · scripts parse). Edits to either MUST update both atomically (Op 16 Pattern A · Cross-Doc SSOT Discipline).
>
> **Verification:** `/scripts/vm-canonical-lint.py` reads JSON and scans consumer files. Pre-Edit Lint Gate hook blocks save on divergence.

---

## 1️⃣ Vision & Mission (LOCKED Apr 23, 2026)

**Locked by:** Nut as Board (Type 1 decision)
**Language policy:** English-primary in operational UI (CC, Solutions Stack, dashboards). Thai gloss/supporting text allowed beneath English. Founder-story + memory canonicals exempt.

### Vision (canonical · English-primary)

> **"Human wisdom. AI at scale. Wisdom for everyone."**

- **Required substrings** (all 3 must appear when Vision is rendered): `Human wisdom` · `AI at scale` · `Wisdom for everyone`
- **Thai gloss (optional · supporting):** "ปัญญาคน + AI ที่สเกลได้ + ปัญญาที่เข้าถึงได้ทุกคน"
- **Supporting Thai (optional · subtext):** "ANTS เป็น Technology & Consulting company ที่ AI-Native ช่วย B2B / B2G / B2B2C transform ด้วยปัญญา AI + ภูมิปัญญาคน — ทำให้ wisdom เข้าถึงได้สำหรับทุกคน ไม่ใช่แค่ enterprise ขนาดใหญ่"

### Mission (canonical · English-primary)

> **"Empower people. Build sustainable businesses. Scale crafted AI to the world."**

- **Required substrings** (all 3 must appear when Mission is rendered): `Empower people` · `Build sustainable businesses` · `Scale crafted AI to the world`
- **Thai gloss (optional · supporting):** "เสริมพลังคน · สร้างธุรกิจยั่งยืน · สเกล crafted AI สู่โลก"
- **Supporting Thai (optional · subtext):** "แกนเดียว · หลายธุรกิจ · เป้าหมายเดียวกัน — ใช้ 63 AI Agents (Tier 1–6 + #63 FJA-CDCA) เป็นฐาน ขับ 27 ธุรกิจในเครือ · ethical · impact-first"

### Tagline (Thai)

> **"แกนเดียว · หลายธุรกิจ · เป้าหมายเดียวกัน"**

### Rollout milestones

| Milestone | Date |
|---|---|
| V/M Locked | 2026-04-23 |
| Phase W1 Kickoff | 2026-05-04 |
| All Hands Reveal | 2026-05-20 |

### ❌ FORBIDDEN stale drafts (must NOT appear in operational UI)

- ❌ "เป็นบริษัท Technology & Consulting ที่ AI-Native อันดับต้นของเอเชีย" (pre-Apr-23 draft)
- ❌ "AI-Native Partner for SEA" (older draft)
- ❌ "ใช้ 62 AI Agents" or "ใช้ 52 AI Agents" (stale agent count)

---

## 2️⃣ Agent Roster (canonical = 65)

**Total:** 65 agents
**Structure:** 62 numbered agents (Tier 1–6 · IDs #1–#62) + 1 sweep agent (#63 FJA-CDCA · hosted in Tier 5) + 2 C-Suite agents (#64 CEcoO + #65 CDA · hosted in Tier 2 · added K.20 29 Apr 2026)

### Breakdown by Tier

| Tier | Name | Count | ID Range |
|---|---|---|---|
| T1 | Board & Advisory | **3** | #1–#3 |
| T2 | C-Suite | **13** | #4–#12 + #41 (CSA) + #52 (CCVO) + #64 (CEcoO) + #65 (CDA) |
| T3 | Heads-of | **12** | #13–#24 |
| T4 | Senior Execution | **17** | #25–#40 + variants |
| T5 | Operations & Admin | **9** | #35–#40, #42–#51 (some hosted here) |
| T6 | Frontier Elite | **10** | #53–#62 |
| Sweep | FJA-CDCA | **1** | #63 |
| **TOTAL** | | **65** | |

### Agents #64 + #65 — Added K.20 (29 Apr 2026 · Nut "Approve Both")

> **Canonical V/M reminder** (locked 23 Apr 2026 · Type-1 · non-negotiable · do NOT abbreviate when quoting):
> - Vision: *"Human wisdom. AI at scale. Wisdom for everyone."*
> - Mission: *"Empower people. Build sustainable businesses. Scale crafted AI to the world."*
>
> The "V/M Anchor" column below is a *pointer* (which substring of the full V/M each agent ties to), **not** the V/M itself.

| ID | Code | Full Name | V/M Anchor (pointer to canonical V/M above) | Activation Date |
|---|---|---|---|---|
| #64 | **CEcoO** | Chief Ecosystem Orchestration Officer (Orchestration tag · Op 14) | Vision anchor: "AI at scale" · Mission anchor: "Build sustainable businesses" | 2026-05-22 (W3-W4 phase) |
| #65 | **CDA** | Chief Decision Architect & Wisdom Steward (Steward tag · Op 14) | Vision anchor: "Wisdom for everyone" · Mission anchor: "Empower people" | 2026-05-08 (W2 phase · activates first) |

**Charter + RACI:** `/agents/Agents-64-65-Charter-RACI.md`
**Strategic Pack:** `/reports/Two-Agents-Strategic-Pack-K20.html`
**Sunset review:** 2026-07-01 (Q3 kickoff · I5 retirement review pattern)

### Tier 6 — Frontier Elite

- ID range: **#53–#62** (10 agents)
- Pillars: **AI Frontier · Deep Tech · Brand/Product**
- Benchmarks: **Apple · Anthropic · OpenAI · SpaceX · Tesla · Google**

### Agent #63 — FJA-CDCA (Folded Sweep Agent)

- **Full name:** Folder Janitor + Cross-Doc Consistency Audit
- **Tier host:** T5
- **Activation:** **2026-04-28** (early activation · was originally 4 May)
- **Trigger:** Op 16 SSOT discipline + V/M cascade gap defect
- **Schedule:** Mondays 09:00 ICT + on-demand
- **Targets (7):**
  1. V/M canonical alignment sweep
  2. Agent roster drift detector (62 vs 63 etc.)
  3. Path registry alignment
  4. Workflow patterns consistency
  5. Workshop catalog consistency
  6. V/M language English-primary enforcement
  7. Operating Principles cross-doc consistency

### ❌ FORBIDDEN stale counts

- ❌ "**52 agents**" (pre-Apr-22 count · CCVO #52 added → 52)
- ❌ "**62 agents**" (pre-27-Apr count · #63 FJA-CDCA added → 63)

### ✅ Preserved (NOT stale · do NOT change)

- ✅ "Tier 6 ID range #53–#62" — Tier 6 is exactly 10 agents IDs 53–62 (correct)
- ✅ "Agent #62 = DRE" — literal agent ID for Developer Relations & Ecosystem Lead (correct)
- ✅ Hex colors `#dc2626`, `#6264a7`, etc. — colors, not counts
- ✅ SVG coordinates `cy="62"`, `width="62"`, etc. — geometry, not counts
- ✅ Chart data `[62, 45, 38, 55]` — chart values, not roster counts

---

## 3️⃣ Human Team

**Min:** 5 humans · **Max optional:** 7 (when revenue > THB 30M/year, add #6 Field Operations Engineer)
**Leverage ratio:** 10–16x via AI agent workforce
**Comparable traditional headcount:** ~50–80 people

### 5 minimum roles

| ID | Role | Why human (not AI) |
|---|---|---|
| H1 | Founder/CEO (Nut) | Ultimate accountability · vision-setting · founder-market fit · investor trust · legal signatory |
| H2 | Chief of Staff / Operator | Physical presence · real-time judgment · protects CEO time · human↔AI interface |
| H3 | Head of Client Trust (Enterprise & Government) | Thai B2G face-to-face trust · cultural protocol · golf/funeral attendance |
| H4 | Lead Engineer / Tech Accountable Person | Legal sign-off · production on-call · physical IoT/hardware troubleshooting |
| H5 | Finance & Legal Controller | Signs financial statements · binds company legally · regulator/auditor/bank-facing |

---

## 4️⃣ Ecosystem (R10 = 27 ventures)

**Version:** R10 (24 Apr 2026)
**Total ventures:** 27
**Tagline (Thai):** "แกนเดียว · หลายธุรกิจ · เป้าหมายเดียวกัน"

### Structure

| Group | Count |
|---|---|
| Main | **6** |
| Startup | **4** |
| Investment | **8** |
| Partner | **9** |
| **TOTAL** | **27** |

### ❌ FORBIDDEN stale counts

- ❌ "**29 ventures**" (R9 count · superseded)

### R10 changes from R9

- Renamed "ANTS 2.0" group → "AI Agent Orchestration"
- Dissolved "AI Content Channels" + "AI Digital Agency" sub-units
- Reordered: FinOps last in Startup · TechFlow above Speed Tech

---

## 5️⃣ Operating Principles (19 total)

| # | Principle | Locked |
|---|---|---|
| 1 | Wisdom > Intelligence > Data | foundational |
| 2 | Long-term over short-term | foundational |
| 3 | Unit economics before scaling | foundational |
| 4 | Runway awareness in every decision | foundational |
| 5 | Honest about AI limitations · Nut final decision | foundational |
| 6 | Strategic frameworks over tactical advice | foundational |
| 7 | Acknowledge uncertainty · reduce before acting | foundational |
| 8 | Default Thai · เฌอคูณ persona · wisdom framing | foundational |
| 9 | Sync before recommend (re-read all SSOTs) | foundational |
| 10 | No operations drift (stay on ANTS 2.0) | foundational |
| 11 | QA Layer-1 + CWO Layer-2 review (DEV/TECH) | 22 Apr |
| 12 | Domain panel Layer-1 + CWO Layer-2 + ARAI (NON-DEV) | 22 Apr |
| 13 | Session Continuity (read SESSION_HANDOFF first) | 22 Apr |
| 14 | Title Convention (T2 Exec/P&L · T6 Craft/Research) | 24 Apr |
| 15 | Mid-Session Health Check every 3 heavy edits | 26 Apr |
| 16 | Cross-Doc SSOT Discipline (Pattern A/B/C) | 26 Apr LATE-PM |
| 17 | Filename Naming Convention (clean operational names · version+date go INSIDE file) | 28 Apr LATE-AM |
| 18 | Session-Close Sync Discipline (Hub-Index + body-content + Op 18 sign-off block) | 28 Apr LATE-AM |
| **19** | **Always pair abbreviation with full name on first occurrence** in consumer-facing files (HTML/MD/email/deck). Pattern: `ABBREV (Full Name — Thai gloss optional)`. Bare codes only allowed in private memory + insider docs. | **27 Apr LATE-PM K.15** |

> **Op 18b candidate (proposed in K.12 re-audit · 29 Apr):** Body-content diff check — frontmatter version bump must be accompanied by visible body-content updates that justify the version bump. Trigger: 3rd "อีกแล้ว" recurrence.

### ❌ FORBIDDEN stale counts

- ❌ "18 Operating Principles" (pre-27-Apr-LATE-PM count · superseded by Op 19 abbreviation pairing)
- ❌ "16 Operating Principles" (pre-28-Apr-LATE-AM count · superseded by Op 17 + Op 18)
- ❌ "13 Operating Principles" (pre-Apr-26 count)
- ❌ "11 Operating Principles" (pre-Apr-22 count)

---

## 6️⃣ Frameworks (Working Toolkit)

### Core Values

**3C-E** — **C**lear · **C**ommunication · **C**hange · **E**volution

### Working Framework — 5 Tools

1. **Vision & Mission** — north star (locked Apr 23)
2. **3C-E Loop** — continuous cycle (not checklist)
3. **PAO** — Problem · Action · Outcome
4. **1-3-1** — 1 เป้า · 3 ทาง · 1 คำแนะนำ
5. **ARAI** — Actions · Results · Ideas for Improvement (mandatory closing on every output)

---

## 7️⃣ Consumer Files (must align to this SSOT)

These files render canonical facts in operational UI. Lint script (`vm-canonical-lint.py`) scans these on every sweep:

| File | Domain |
|---|---|
| `/command-center/ANTS-2.0-Unified-Command-Center.html` | Live unified dashboard (K.13: Master Audit folded into 3 tabs) |
| `/products/ANTS-2.0-AI-Solutions-Stack.html` | Product stack |
| `/reports/ANTS-Audit-Dashboard.html` | Audit dashboard (visual companion to CC) |
| ~~`/reports/ANTS-Master-Audit-Report.md`~~ | ⚠️ FOLDED into Command Center K.13 · archived |
| `/internal-transformation/Internal-Transformation-Communication-Plan.md` | Transformation plan |
| `/ANTS-2.0-Hub-Index.html` | Hub navigation |
| `/README.md` | Folder navigation |
| `/ecosystem/ANTS-Ecosystem-Dashboard.html` | Ecosystem dashboard |

---

## 8️⃣ Exempt Paths (do NOT lint these — historical/foundational)

- `/archive/` — superseded versions preserved intentionally
- `/foundational-apr17/` — frozen early docs
- `/launches/` — event-snapshot artifacts
- `/founder-story/` — different rhetorical conventions
- `/canonical/` — SSOT itself
- `/scripts/` — tooling

---

## 9️⃣ Update Protocol (Op Principle 16 — Pattern A)

1. Any change to V/M, agent count, ecosystem, op count, or any canonical fact MUST update **both** `vm-status.json` AND this file (`canonical-facts.md`) in the same commit.
2. Run `/scripts/vm-canonical-lint.py` against all consumer files BEFORE touching them.
3. If lint reports divergence → fix consumer files BEFORE adding new content (don't paint over rust).
4. Pre-Edit Lint Gate hook (I-NEW-2) auto-blocks save on V/M divergence.

---

_Crafted with wisdom, scaled with AI · เฌอคูณ · v1.1 · 29 Apr 2026 (K.12 re-audit · OP count 16→18 corrected · pairs with vm-status.json v1.1)_
