---
title: K.21 Phase 1 Discovery Report — Able AI Folder
generated: 2026-04-29 (Day 1 of 30-day sprint)
owner: KM #51 + Senior Research #25
review: CWO #5 (Layer-2)
status: DAY-1 INITIAL CRAWL COMPLETE — pending sensitivity sign-off
---

# Phase 1 Discovery Report — Able AI Folder

## TL;DR
- **Scope verified:** `/Shared Documents/New Business/Able AI/` accessible via SharePoint MCP ✅
- **13 files** mapped in-scope (3 root · 2 Chat Center · 3 CRM+CDP · 2 Data Center · 3 Training)
- **8 Tier-1 files** ready for Wisdom Card synthesis (Phase 2)
- **3 high-value out-of-scope items** identified for expansion (Q1/APR Management decks · กยศ POC)
- **5 of 12 categories** covered in Able AI alone — Phase 2 expansion needed for full coverage
- **0 SECRET-tag misclassifications** flagged in Day-1 pass (Senior Legal #34 final review pending)

## Folder Structure (Verified)

```
/Shared Documents/New Business/Able AI/
├── 20260421 AI_Able_Strategy.html               [Tier 1 · strategy]
├── AI_Sales_Intelligence_2026.xlsx              [Tier 1 · sales · 760 accounts]
├── Strategic_Marketing_Plan 2.html              [Tier 1 · marketing]
├── Chat Center/
│   ├── 20260421 AIAble_ChatSME.pptx             [Tier 1 · product]
│   └── replybot-landing.html                    [Tier 2 · marketing]
├── CRM + CDP/
│   ├── 20260421 AIAble_CRM_CDP.pptx             [Tier 1 · product]
│   ├── ANTS Sale_crm cdp.html                   [Tier 2 · sales]
│   └── 20260402 AIAble_CRM_CDP_Concept.html     [Tier 2 · product]
├── Data Center/
│   ├── 20260402 [S-Curve] AI_Admin_24hr_Strategy.pptx  [Tier 1 · strategy]
│   └── 20260401 AI_Ecosystem_Strategy_2026.pptx        [Tier 1 · strategy]
└── Training/
    └── [01] CMS/
        ├── 20260327 สคริปต์พูด_AI_สหกรณ์.docx        [Tier 2 · founder_story]
        ├── 20260327 AI กับการยกระดับสหกรณ์.pdf      [Tier 2 · founder_story]
        └── 20260327 สคริปต์พูด_AI_สหกรณ์.md          [Tier 2 · founder_story]
```

## Initial Wisdom Signals (Day-1 surface read)

These signals are extracted from search summaries — full deep-read happens in Phase 2.

### Strategy Layer
- **AI Ecosystem Strategy 2026** — Value Chain: Data → Execution → SME → Education · 4-product architecture
- **AI Able Product Strategy** — Thailand-first → global · "AI ที่ทำงานแทนได้จริง"
- **AI Admin 24hr S-Curve** — "พนักงานขาย+แอดมินที่ไม่ต้องจ้าง" positioning · GTM funnel mapped

### Sales Layer
- **AI Sales Intelligence 2026** — 760 customer accounts analyzed · Grade A/B/C tiered (file requires Excel deep-read)
- **CRM CDP Backoffice** — 360° customer view · Next Best Action engine

### Marketing Layer
- **Strategic Marketing Plan AI Chatbot for SME** — Facebook + LINE focus channel
- **ReplyBot landing** — 1,240+ businesses claimed · ฿40,000/month admin savings positioning

### Product Layer
- **4-Product Portfolio confirmed:** Chat Center · CRM+CDP · Data Center · Training
- Mapping aligns with 5 Product Shadow Agents (already in SAKM v2 from K.15)

### Founder Story Layer
- **AI สหกรณ์ training script** — Nut as AI Specialist speaker · cooperative-sector positioning · 3 file formats (docx · pdf · md) — sets pattern for Founder Wisdom Library

## High-Value Expansion Targets (out of Able AI scope)

These were surfaced during search and recommend folding into Phase 2:

| File | Path | Why fold in |
|------|------|-------------|
| 20260325 Management quarter.pptx | `/Business Development/[08] Management/` | **Q1 2026 Revenue 35.97M THB** (Jan 10.52M · Feb 11.81M · Mar 13.64M) — finance category gold |
| 20260428 Management APR.pptx | `/Business Development/[08] Management/` | **APR YTD 51M THB** · Apr month 13.81M · 100M target 21.8% progress — finance + strategy gold |
| 20260312 POC Presentation.pdf (กยศ) | `/Microsoft Teams Chat Files/` | Government POC (กยศ) using ABLE positioning — historical_decisions + sales (B2G) |

## Sensitivity Classification (Proposed — pending Legal #34 sign-off)

| Tag | Count | Examples |
|-----|-------|----------|
| SECRET | 1 | AI_Sales_Intelligence_2026.xlsx (760 customer records) |
| CONFIDENTIAL | 6 | Strategy decks · ChatSME pptx · CRM+CDP product pptx |
| INTERNAL | 6 | Concept docs · landing page · training scripts |
| PUBLIC | 0 | (none in Able AI scope yet) |

**Senior Legal #34 must finalize before Phase 2 starts.**

## Day-1 Health Check

| Check | Status | Note |
|-------|--------|------|
| SharePoint MCP credentials | ✅ Working | Folder + search both functional |
| Folder access permissions | ✅ Granted | All Able AI subfolders visible |
| Folder-search children semantics | ⚠️ Limitation found | `folder_search` matches by name globally · use `sharepoint_search` with broad query for in-scope listing |
| Inventory schema | ✅ Stable | `sharepoint-ableai-index.json` v1 written |
| Tooling alignment with I-NEW-27 | ✅ Aligned | Inventory schema matches sharepoint-wisdom-sync.py expected input |

## Day-2 to Day-7 Plan (Phase 1 remainder)

1. **Day 2** — Senior Legal #34 finalizes sensitivity tags + PDPA gate (esp. Sales Intelligence xlsx with 760 records)
2. **Day 3** — Deep-read Tier-1 .pptx files via PowerPoint MCP (+ .html via Word/text MCP) · extract structured wisdom
3. **Day 4** — Decide expansion: Phase 2 should include Management Q1/APR + กยศ POC? (Recommend: yes)
4. **Day 5** — KM #51 finalizes Wisdom Card schema v2 with field reviews from Senior Content #27
5. **Day 6** — Run wisdom-card-scaffold.py (I-NEW-28) on first 5 Tier-1 files as pilot batch
6. **Day 7** — Phase 1 closeout review — CWO + #65 CDA Layer-2 sign-off · gate to Phase 2

## Risks Surfaced

1. **Sales Intelligence xlsx is SECRET-tier** — needs encryption-at-rest decision before any agent federation. Recommend: never expose raw xlsx to agent mesh; only synthesized aggregate wisdom.
2. **Founder Story script in 3 formats** — risk of drift between docx/pdf/md versions. Recommend: declare .md as canonical, deprecate other two.
3. **Out-of-scope finance data is critical** — without Management Q1/APR folded in, finance category remains empty. Strong recommendation to expand scope.

## ARAI

- **Actions:** SharePoint MCP verified · 13 files inventoried · 8 Tier-1 identified · 3 expansion targets surfaced · Sensitivity proposals drafted
- **Results:** Phase 1 Day 1/7 complete · 14% sprint progress · zero blocking issues
- **Improvements:**
  - I-NEW-27 sharepoint-wisdom-sync.py shipped ✅
  - I-NEW-28 wisdom-card-scaffold.py shipped ✅
  - **NEW I-NEW-29 candidate** — Excel deep-reader script for AI_Sales_Intelligence_2026.xlsx (extract aggregate wisdom · respect SECRET tag · output redacted summary)

---

*Generated under K.21 SAKM v2 SharePoint Bootstrap charter · Op 11 QA Layer-1 by Senior Content #27 (pending) · Op 12 Layer-2 by CWO + #65 CDA (pending Day 7).*
