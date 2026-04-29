---
title: SAKM v2 Sensitivity Classification Rubric v1.0
locked: 2026-04-29 (K.21 Day 2)
owner: Senior Legal & Compliance #34 (independent gatekeeper)
review: CWO #5 + #65 CDA (Layer-2)
sunset_review: 2026-07-29 (quarterly)
---

# SAKM v2 Sensitivity Classification Rubric

**Mandate:** This rubric is the SSOT for classifying every SharePoint source artifact and every derived Wisdom Card before federation to the 65-agent mesh. Senior Legal #34 acts as INDEPENDENT gatekeeper — Layer-2 review by CWO + #65 CDA cannot override #34 toward more permissive tier (only toward more restrictive).

## 4-Tier Schema

### PUBLIC
- **Definition:** Already disclosed externally. Marketing pages · published proposals · press releases · cleared logos.
- **Federation:** ✅ All 65 agents · external sharing OK
- **PDPA risk:** None
- **Examples in K.21 scope:** *(none yet — replybot-landing.html is INTERNAL because it claims unverified usage stats)*

### INTERNAL
- **Definition:** Operational documents · concept drafts · internal-only positioning · training scripts · normalized historical proposals where customer identity is generic.
- **Federation:** ✅ All 65 agents · ❌ external sharing
- **PDPA risk:** Low — no PII / customer identifiers
- **Required scrubbing before federation:** Replace specific employee names with role labels (e.g., "ธนกาญ" → "AI Specialist"); remove draft watermarks
- **Examples in K.21 scope:** ANTS Sale_crm cdp.html · 20260402 AIAble_CRM_CDP_Concept.html · replybot-landing.html · 20260327 สคริปต์พูด_AI_สหกรณ์ (.docx · .pdf · .md)

### CONFIDENTIAL
- **Definition:** Strategic decks revealing competitive positioning · pricing strategy · product roadmap · founder thesis · financial dashboards · government POC details.
- **Federation:** ✅ All 65 agents — but flagged "do not externalize" in Wisdom Card metadata · ❌ external sharing without H1 Nut sign-off
- **PDPA risk:** Low to medium — may name specific clients in case-study form
- **Required scrubbing:** Mask deal sizes >THB 1M to ranges (e.g., "5M" → "1-10M tier"); aggregate quarterly numbers OK in Wisdom Card form
- **Examples in K.21 scope:**
  - 20260421 AI_Able_Strategy.html
  - 20260421 AIAble_ChatSME.pptx
  - 20260421 AIAble_CRM_CDP.pptx
  - 20260402 [S-Curve] AI_Admin_24hr_Strategy.pptx
  - 20260401 AI_Ecosystem_Strategy_2026.pptx
  - Strategic_Marketing_Plan 2.html
  - 20260325 Management quarter.pptx (Q1 Revenue 35.97M)
  - 20260428 Management APR.pptx (APR YTD 51M)
  - ANTS 20260312 กยศ POC Presentation.pdf

### SECRET
- **Definition:** Customer-identifying records · PII at row level · raw financial data with concentration risk · partnership term sheets pre-signature · personnel records.
- **Federation:** ❌ NEVER federate raw to agent mesh
- **Allowed flow:** Source → I-NEW-29 excel-wisdom-extractor.py with `--gatekeeper-approved` → CONFIDENTIAL aggregate Wisdom Cards
- **Storage:** Only on H5 Finance/Legal Controller's secured volume + #34's gate
- **PDPA risk:** HIGH — direct PII exposure
- **Examples in K.21 scope:**
  - **AI_Sales_Intelligence_2026.xlsx** (760 customer records · Grade A/B/C tiering · contains company names + likely contacts)

## PDPA Gate Criteria (Mechanical)

A source artifact is **automatically SECRET** if any of the following matches its content:

| Criterion | Pattern (TH + EN) | Source examples |
|-----------|-------------------|-----------------|
| Personal name with contact | `(name OR ชื่อ) + (email OR phone OR โทร)` co-occurring | Customer lists, salesperson logs |
| National ID | 13-digit Thai citizen ID, passport ID | HR files, KYC packets |
| Bank account / financial PII | account number patterns | Finance ops files |
| Health / sensitive personal data | Religion · health · sexual orientation · union | (none expected in Able AI scope) |
| Customer record at row level | >10 customer-identifying rows in single file | AI_Sales_Intelligence_2026.xlsx ✅ matches |

If any 1 matches → **SECRET tier · I-NEW-29 mandatory before any synthesis**

## Down-Classification Rules

Wisdom Cards derived from a higher-sensitivity source MAY be down-classified if and only if:
1. Senior Legal #34 explicitly approves via `--gatekeeper-approved` flag (mechanical) OR signed review (manual)
2. All PII patterns are either dropped or hashed (per I-NEW-29 default classifier)
3. Aggregation ≥10 records per dimension to prevent re-identification (k-anonymity baseline)
4. Audit log preserved alongside output

## Up-Classification Rules

Any of these triggers immediate up-classification (toward more restrictive):
- Discovery of unredacted PII in supposedly-INTERNAL output → escalate to CONFIDENTIAL or SECRET
- Litigation hold on related matter → SECRET
- Pending external publication (NDA risk) → SECRET until NDA cleared
- Government regulatory review → CONFIDENTIAL minimum

## K.21 Phase 1 Final Tag-Lock (16 items)

| # | File | Tier | Sensitivity | #34 Sign-off |
|---|------|------|-------------|--------------|
| 1 | 20260421 AI_Able_Strategy.html | 1 | CONFIDENTIAL | ✅ |
| 2 | AI_Sales_Intelligence_2026.xlsx | 1 | **SECRET** | ✅ — I-NEW-29 mandatory |
| 3 | Strategic_Marketing_Plan 2.html | 1 | CONFIDENTIAL | ✅ |
| 4 | 20260421 AIAble_ChatSME.pptx | 1 | CONFIDENTIAL | ✅ |
| 5 | replybot-landing.html | 2 | INTERNAL | ✅ — claims "1,240+ businesses" require verification before any external use |
| 6 | 20260421 AIAble_CRM_CDP.pptx | 1 | CONFIDENTIAL | ✅ |
| 7 | ANTS Sale_crm cdp.html | 2 | INTERNAL | ✅ |
| 8 | 20260402 AIAble_CRM_CDP_Concept.html | 2 | INTERNAL | ✅ |
| 9 | 20260402 [S-Curve] AI_Admin_24hr_Strategy.pptx | 1 | CONFIDENTIAL | ✅ |
| 10 | 20260401 AI_Ecosystem_Strategy_2026.pptx | 1 | CONFIDENTIAL | ✅ |
| 11 | 20260327 สคริปต์พูด_AI_สหกรณ์.docx | 2 | INTERNAL | ✅ — name "ธนกาญ" → role-label scrub before federation |
| 12 | 20260327 AI กับการยกระดับสหกรณ์.pdf | 2 | INTERNAL | ✅ |
| 13 | 20260327 สคริปต์พูด_AI_สหกรณ์.md | 2 | INTERNAL | ✅ — declared canonical (deprecates #11/#12) |
| 14 | 20260325 Management quarter.pptx | 1 | CONFIDENTIAL | ✅ — revenue numbers acceptable in Wisdom Card aggregate |
| 15 | 20260428 Management APR.pptx | 1 | CONFIDENTIAL | ✅ — same |
| 16 | ANTS 20260312 กยศ POC Presentation.pdf | 1 | CONFIDENTIAL | ✅ — government client; mask any specific deal value |

**Final tally:** 1 SECRET · 9 CONFIDENTIAL · 6 INTERNAL · 0 PUBLIC

## Layer-2 Review (CWO + #65 CDA)
Pending review at Day 7 closeout gate. Any Layer-2 disagreement → escalate to H1 Nut.

## ARAI
- **Actions:** Lock 16-item classification · ratify I-NEW-29 PDPA gate (matches mechanical rubric) · declare .md canonical for Founder Story trio
- **Results:** Phase 2 can begin Day 8 with 100% sensitivity locked · 1 SECRET item gated (must use I-NEW-29) · 0 ambiguous items
- **Improvement:** I-NEW-32 candidate — sensitivity-rubric-lint.py weekly cron under #63 (auto-flags Wisdom Cards whose sensitivity_tag drifts from rubric)
