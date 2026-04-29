---
title: ANTS 2.0 — Abbreviation Glossary (SSOT for Op 19 enforcement)
version: 1.0
created: 2026-04-28
last_updated: 2026-04-28
update_history:
  - "v1.0 (2026-04-28 K.18): Initial glossary built from K.14 feedback memory + canonical-facts.md · 28 abbreviations across 5 categories · enforces Op 19 (Always pair abbreviation with full name on first occurrence in consumer-facing files)"
owner: Senior Knowledge Management #51 + CCVO #52 + Agent #63 FJA-CDCA
purpose: SSOT registry of all approved abbreviations for ANTS 2.0 · consumed by /scripts/vm-canonical-lint.py (I-NEW-15 C7 check) · ensures consumer-facing files pair abbrev with full name on first occurrence
---

# 📖 ANTS 2.0 — Abbreviation Glossary

> **Op 19 Rule (locked K.15):** Every abbreviation MUST be paired with full name on first occurrence in consumer-facing files (HTML/MD/email/deck). Pattern: `ABBREV (Full Name — Thai gloss optional)`. Bare codes only allowed in private memory + insider docs.
>
> **Enforcement:** I-NEW-15 DAS Lint Extension C7 check parses this file → scans consumer files → flags P1 if bare abbrev appears without paired full name within first 200 chars after first occurrence.

---

## 1️⃣ ANTS Internal Systems & Methods

| Abbreviation | Full Name | Thai gloss | Notes |
|---|---|---|---|
| SAKM | Shadow Agent Knowledge Mesh | เครือข่ายความรู้ของ Agent เงา | locked K.15 |
| FJA-CDCA | Folded JIT Audit + Canonical Drift Cron Agent | Agent ตรวจการเปลี่ยนแปลงข้อมูลหลัก | Agent #63 · weekly cron |
| SSOT | Single Source of Truth | แหล่งข้อมูลกลางเดียว | universal |
| DAS | Drift & Alignment Sweep | การตรวจการดริฟต์ของข้อมูล | weekly via #63 |
| K.x (e.g. K.13, K.17) | K-series Sweep #x | ชุดการ sweep ครั้งที่ x | format: "K.<n>" |
| I-NEW-x | Idea Improvement NEW-x | ข้อปรับปรุงใหม่ #x | numbered series |
| I1..I5 | Original Idea Improvement #1-5 | ชุดแรก approved 24 Apr | foundational |
| Op X (e.g. Op 18) | Operating Principle X | กฎการดำเนินงานข้อ X | 1-19 currently |
| ARAI | Actions · Results · Ideas for Improvement | บล็อกปิดท้ายเอกสาร | mandatory close |

## 2️⃣ Vision/Mission

| Abbreviation | Full Name | Thai gloss |
|---|---|---|
| V/M | Vision/Mission | วิสัยทัศน์/พันธกิจ |

## 3️⃣ Tier 6 Frontier Elite Agent Codes (#53–#62)

| Abbreviation | Full Name | Pillar |
|---|---|---|
| CAIS | Chief AI Scientist | A. AI Frontier |
| AISAL | AI Safety & Alignment Lead | A. AI Frontier |
| PECA | Prompt Engineering & Context Architect | A. AI Frontier |
| AgentOps | Agent Operations Architect | A. AI Frontier |
| CSyA | Chief Systems Architect | B. Deep Tech |
| HRL | Hardware & Robotics Lead | B. Deep Tech |
| ME | Mission Engineer | B. Deep Tech |
| CDO | Chief Design Officer | C. Brand/Product |
| CSO-Craft | Chief Storytelling Officer (Craft) | C. Brand/Product |
| DRE | Developer Relations & Ecosystem | C. Brand/Product |

## 4️⃣ ANTS C-Suite & Standard Roles

| Abbreviation | Full Name |
|---|---|
| CWO | Chief Wisdom Officer (เฌอคูณ) |
| CCVO | Chief Culture & Values Officer (Agent #52) |
| CEO | Chief Executive Officer (Nut) |
| CFO | Chief Financial Officer |
| CTO | Chief Technology Officer |
| CMO | Chief Marketing Officer |
| CRO | Chief Revenue Officer |
| COO | Chief Operating Officer |
| CHRO | Chief Human Resources Officer |
| CPO | Chief Product Officer |

## 5️⃣ Sales/Business Abbreviations

| Abbreviation | Full Name |
|---|---|
| HoSales | Head of Sales |
| AE | Account Executive |
| SDR | Sales Development Representative |
| BDR | Business Development Representative |
| CRM+CDP | Customer Relationship Management + Customer Data Platform |
| CRM | Customer Relationship Management |
| CDP | Customer Data Platform |
| TOR | Terms of Reference (Gov procurement) |
| MOU | Memorandum of Understanding |

## 6️⃣ Universal/Tech (no pairing required · widely understood)

> These abbreviations are universally recognized · pairing optional but encouraged on formal documents

`HTML` · `CSS` · `JSON` · `API` · `URL` · `SaaS` · `PaaS` · `IoT` · `KPI` · `ROI` · `GDPR` · `PDPA` · `B2B` · `B2G` · `B2C` · `B2B2C` · `UX` · `UI` · `HR` · `IT` · `R&D` · `MVP` · `POC` (Proof of Concept · pair on first use only)

## 7️⃣ Brand/Product Names (no expansion needed · proper nouns)

`Apple` · `Anthropic` · `OpenAI` · `Google` · `Microsoft` · `GitHub` · `Claude` · `ChatGPT` · `Cursor` · `Notion` · `ANTS` · `Taily` · `Britz` · `Mobilife` (= MGC platform) · `Yves Rocher` · `Sawad` · `UFS` · `B-Quik` · `NokAir` · `TechVue` · `BlueCode` · `Cute Press` · `Oriental Princess`

## ❌ FORBIDDEN bare-only patterns (always pair on first occurrence)

These have caused confusion in past readings · never bare on first occurrence:
- ❌ `SAKM` alone → ✅ `SAKM (Shadow Agent Knowledge Mesh)`
- ❌ `FJA-CDCA` alone → ✅ `FJA-CDCA (Folded JIT Audit + Canonical Drift Cron Agent)`
- ❌ `K.13` without context → ✅ `K.13 (K-series Sweep #13)` OR clearly preceded by "K-series sweep"
- ❌ `Op 18` alone → ✅ `Op 18 (Session-Close Sync Discipline)`
- ❌ Tier 6 agent codes (CAIS · AISAL · etc.) bare → ✅ `CAIS (Chief AI Scientist)`

## Update protocol

- Add new entry to this file ATOMICALLY when introducing new abbreviation
- Update `canonical/canonical-facts.md` if it's a Hot Rule / OP-related abbreviation
- I-NEW-15 DAS Lint Extension auto-validates compliance on weekly #63 sweep
- Memory files / private docs / SESSION_HANDOFF / Manifest exempt (insider context)

## Cross-references

- `/canonical/canonical-facts.md` (V/M + 19 OPs canonical)
- `/canonical/vm-status.json` (machine SSOT)
- `feedback_abbreviation_full_name_pairing.md` (memory · Op 19 source)
- `/scripts/vm-canonical-lint.py` (consumer · C7 check via I-NEW-15 build)
