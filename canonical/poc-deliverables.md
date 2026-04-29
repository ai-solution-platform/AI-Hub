---
title: ANTS 2.0 — POC (Proof-of-Concept) Deliverables Directory
version: 1.1
created: 2026-04-27
last_updated: 2026-04-27
update_history:
  - "v1.0 (2026-04-27 K.16): Initial directory built from Nut's K.16 brain-dump · 8 categories · 30+ deliverables"
  - "v1.1 (2026-04-27 K.17): URL verification round · MGC /app + /admin sub-paths confirmed 404 (single-page React app · only root + proposal.html valid) · Taily admin added (https://ai-solution-platform.github.io/Taily/admin/ HTTP 200) · Marketing/Content category populated (7 AI Production videos from ~/Desktop/Start Up/AI Production/) · all 11 known live URLs HTTP 200 verified · status flags added (live/local/method/confidential/video)"
owner: Senior Knowledge Management #51 + CCVO #52 + Senior Solution Architect #29
purpose: SSOT registry of all real POC outputs that Nut + 63 Agents have built · used as Training Curriculum case studies + portfolio reference
---

# 📦 ANTS 2.0 POC Deliverables Directory

> **Purpose:** ทุก POC ที่ทำเสร็จแล้ว → list ที่นี่ · ใช้เป็น case study + portfolio + training material
> **Source priority:** GitHub Pages public URL > local Mac file:// > internal-only memory reference
> **Status legend:** 🌐 = GitHub Pages live · 💻 = local Mac (not published) · 📝 = methodology only (no live demo)

---

## 1. Application Development (8 deliverables)

> ผลงาน app/web จริงที่มี UI + functionality ครบ · ใช้เป็น product showcase

### 1.1 Taily — Pet Operation System Super App
- **Live URL (Web App):** 🌐 https://ai-solution-platform.github.io/Taily/app/ (HTTP 200 verified K.17)
- **Live URL (Admin Backoffice):** 🌐 https://ai-solution-platform.github.io/Taily/admin/ (HTTP 200 · K.17 NEW · per Nut feedback)
- **Stack:** Web app + admin backoffice · Pet OS · Buddy · Pet Passport · Taily Pay · Book Now · Vet Clinics
- **Workshop ref:** W-02 Taily v3
- **Training value:** end-to-end app architecture · pet economy domain · multi-feature integration · admin/user dual interface

### 1.2 Retail Space Leasing — Web App
- **Live URL:** 🌐 https://ai-solution-platform.github.io/RSL/discover/
- **Live URL (admin):** 🌐 https://ai-solution-platform.github.io/RSL/admin/
- **Stack:** Web app + admin backoffice · 7,700+ verified listings · 77 provinces · 5-layer moat
- **Workshop ref:** W-07 Retail Space Leasing DB
- **Training value:** data verification methodology · admin/user dual interface · zero fabricated data discipline

### 1.3 AI Assistance — Auto Pilot
- **Live URL:** 🌐 https://ai-solution-platform.github.io/autopilot/poc-v2.html
- **Stack:** AI Assistant POC · v2 · workflow automation
- **Workshop ref:** new entry — propose W-11 (or fold into Pitching workshop)
- **Training value:** AI assistant architecture · prompt orchestration

### 1.4 MGC Asia — Loyalty CRM (Mobilife platform)
- **Live URL (Main app · single-page React):** 🌐 https://ai-solution-platform.github.io/mgc-asia-loyalty-poc/ (HTTP 200 · K.17 verified)
- **Live URL (Commercial Proposal):** 🌐 https://ai-solution-platform.github.io/mgc-asia-loyalty-poc/proposal.html (HTTP 200 · K.17 verified · cross-listed in Category 5)
- **K.17 fix:** Original `/app` and `/admin` paths return HTTP 404 — repo is single-page React app (Mobilife), not multi-route. Mobile + Admin views are SPA routes accessed via in-app navigation, not direct URL.
- **Stack:** Mobilife — MGC-Asia Loyalty Platform · React SPA · CRM + Loyalty
- **Workshop ref:** W-12 (App) + W-16 (Proposal)
- **Training value:** Loyalty engine design · mobile UX · single-page app architecture

### 1.5 Smart Website
- **Live URL (Web):** 🌐 https://ai-solution-platform.github.io/smart-website/
- **Live URL (Admin):** 🌐 https://ai-solution-platform.github.io/smart-website/admin/dashboard/
- **Stack:** Smart website builder · admin dashboard
- **Workshop ref:** new entry — propose W-13 Smart Website Builder
- **Training value:** website-as-product methodology · CMS + AI content

### 1.6 Chat Center — AI Customer Service
- **Local files (8 HTML):** 💻 ~/Desktop/AI Chat/{chat,channels,backoffice,knowledge,reports,segmentation,token-management,notifications}.html
- **Status:** Not yet on GitHub Pages — recommend migrate to ai-solution-platform/chat-center/
- **Workshop ref:** new entry — propose W-14 Chat Center (could fold into Application Dev hub)
- **Training value:** multi-channel chat · knowledge management · segmentation · token management

---

## 2. Marketing Agency — AEO/SEO Audit (6 deliverables)

> ผลงาน audit dashboard 10-tab format · ใช้เป็น template หลักสำหรับลูกค้า marketing

### 2.1 Yves Rocher (Thailand) — SEO/AEO Audit
- **Local file:** 💻 ~/Desktop/AI/SEO-Audit/YvesRocher-SEO-AEO-Audit-Dashboard.html
- **Status:** Not on GitHub Pages — propose migrate to ai-solution-platform/seo-audit-yvesrocher/
- **Workshop ref:** W-01 SEO/AEO Audit Dashboard (current case study)
- **Training value:** 10-tab template structure · 32+ year brand audit · multi-dimensional scoring

### 2.2 ANTS — SEO Audit
- **Local file:** 💻 ~/Desktop/AI/SEO-Audit/ANTS-SEO-Audit-Dashboard.html
- **Status:** Internal · self-audit
- **Training value:** dogfooding · self-improvement

### 2.3 PostcatSavings — SEO Audit
- **Local file:** 💻 ~/Desktop/AI/SEO-Audit/PostcatSavings-SEO-Audit-Dashboard.html
- **Training value:** B2C savings/financial sector audit

### 2.4 Sawad — SEO/AEO Audit
- **Local file:** 💻 ~/Desktop/AI/SEO-Audit/Sawad-SEO-AEO-Audit-Dashboard.html
- **Training value:** Financial services brand audit · also see TechVue_SAWAD pitching deliverables

### 2.5 UFS Thailand — SEO Audit
- **Local file:** 💻 ~/Desktop/AI/SEO-Audit/UFS-Thailand-SEO-Audit-Dashboard.html
- **Training value:** F&B sector audit

### 2.6 B-Quik — SEO Audit
- **Local file:** 💻 ~/Desktop/AI/SEO-Audit/B-Quik-SEO-Audit-Dashboard.html
- **Training value:** Auto service sector audit

> **Migration recommendation:** Bulk-migrate all 6 SEO audits to `ai-solution-platform/seo-audit-portfolio/` GitHub Pages — clients can browse portfolio · prevents file:// dependency

---

## 3. Marketing Agency — AI Content & Production (7 deliverables · K.17 NEW)

> K.17: Populated from Nut's K.17 feedback — folder `/Users/thanakanpermthong/Desktop/Start Up/AI Production/`

### 3.1 ANTS song 90s
- **Local file:** 💻 `~/Desktop/Start Up/AI Production/ANTS song 90s.mp4` (115 MB · 16 Apr 2026)
- **Type:** Brand anthem · 90-second song-format video
- **Training value:** AI music + video production · brand storytelling

### 3.2 ANTS — AI First Company
- **Local file:** 💻 `~/Desktop/Start Up/AI Production/ANTS-AI_First_Company.mp4` (70 MB · 16 Apr 2026)
- **Type:** Company brand film · "AI-First" positioning
- **Training value:** Company narrative + AI-native positioning

### 3.3 BlueCode Global
- **Local file:** 💻 `~/Desktop/Start Up/AI Production/BlueCode Global.mp4` (44 MB · 8 Apr 2026)
- **Type:** Client commercial production
- **Training value:** Client-commissioned brand video · enterprise tech

### 3.4 Cute Press
- **Local file:** 💻 `~/Desktop/Start Up/AI Production/Cute Press.mp4` (40 MB · 8 Apr 2026)
- **Type:** Beauty/cosmetics brand commercial
- **Training value:** Consumer brand · product-focused video

### 3.5 New DNA · จะปรับตัวหรือสูญพันธุ์
- **Local file:** 💻 `~/Desktop/Start Up/AI Production/New DNA จะปรับตัว หรือสูญพันธ์ุ.mp4` (346 MB · 16 Apr 2026)
- **Type:** Long-form thought leadership / change-management narrative
- **Training value:** Long-form storytelling · transformation themes (relevant to internal Transformation Plan)

### 3.6 Songkran 2026
- **Local file:** 💻 `~/Desktop/Start Up/AI Production/Songkran-2026.mp4` (4 MB · 13 Apr 2026)
- **Type:** Seasonal/cultural campaign · short form
- **Training value:** Cultural campaign + seasonal marketing

### 3.7 Oriental Princess · ครีมกันแดด
- **Local file:** 💻 `~/Desktop/Start Up/AI Production/ครีมกันเเดด oriental princess .mp4` (48 MB · 8 Apr 2026)
- **Type:** Beauty/cosmetics product commercial · sunscreen
- **Training value:** Product-specific commercial work

> **Migration recommendation:** Bulk-upload all 7 videos to `ai-solution-platform/ai-production-showcase/` GitHub Pages or YouTube unlisted (size constraints) — clients can browse video portfolio · prevents file:// dependency · ~720 MB total (ZIP-then-upload OR YouTube embed via README).

> **Cross-reference candidates from ANTS 2.0 memory:**
> - Post-Songkran Welcome AI-First Trailers (archived K.14 · originally 20 Apr launch)
> - Thumbnail Survey Panel Results (Apr 20 · 50-voter × 5-dim methodology · also see Agent Orchestration §8.6)

---

## 4. Network Operation Center (1 deliverable)

### 4.1 ANTS SMS Error Code NOC Dashboard
- **Local file:** 💻 ~/Desktop/AI/NOC Monitoring/NOC Monitoring/ANTS_SMS_Error_Code_NOC_Dashboard.html
- **Status:** Not on GitHub Pages — propose migrate to ai-solution-platform/noc-dashboard/
- **Workshop ref:** W-03 NOC Dashboard · Network Operations
- **Training value:** real-time monitoring · alert flow · escalation matrix · 24/7 uptime SLA tracking

---

## 5. Pitching & Proposal Deck (10 deliverables)

> Sales-facing decks + commercial proposals + investor summaries

### 5.1 AI Chat Center — Pitching Index
- **Local file:** 💻 ~/Desktop/AI Chat/index.html

### 5.2 NokAir — Investor Summary A4
- **Local file:** 💻 ~/Library/CloudStorage/OneDrive-AdvanceNetworkTechnology&ServiceCo.,Ltd/ANTS/Clients & Projects/NokAir/NokAir_Investor_Summary_A4.pdf
- **Stack:** PDF · A4 print-ready
- **Sensitivity:** ⚠️ client-specific · OneDrive only · do NOT publish to GitHub Pages

### 5.3 Taily — Overview 2026
- **Local file:** 💻 ~/Desktop/Taily/Taily_Overview_2026.html
- **Training value:** product overview deck format

### 5.4 Auto Pilot — Pitching v2
- **Live URL:** 🌐 https://ai-solution-platform.github.io/autopilot/pitching-v2.html
- **Stack:** Pitching deck published · GitHub Pages

### 5.5 Auto Pilot — Proposal v2
- **Live URL:** 🌐 https://ai-solution-platform.github.io/autopilot/proposal-v2.html

### 5.6 MGC Asia — Loyalty Proposal
- **Live URL:** 🌐 https://ai-solution-platform.github.io/mgc-asia-loyalty-poc/proposal.html

### 5.7 TechVue SAWAD — Commercial Model (xlsx)
- **Local file:** 💻 TechVue_SAWAD_Commercial_Model.xlsx (path TBD)
- **Sensitivity:** ⚠️ client-specific commercial model · do NOT publish

### 5.8 TechVue SAWAD — Solution Proposal (pptx)
- **Local file:** 💻 TechVue_SAWAD_Solution_Proposal.pptx (path TBD)
- **Sensitivity:** ⚠️ client-specific · do NOT publish

### 5.9 AI Smart Package Builder
- **Status:** 📝 methodology + sample outputs · not single artifact
- **Workshop ref:** W-04 AI Smart Package Builder
- **Training value:** Product bundling · pricing strategy · enterprise quote generation

### 5.10 AI Smart Contract Review
- **Status:** 📝 methodology + Consulting Agreement v2 sample
- **Workshop ref:** W-05 AI Smart Contract Review
- **Training value:** Legal doc analysis · red-flag detection · zero-human-lawyer model

---

## 6. Analytic (2 deliverables)

### 6.1 สหกรณ์ออมทรัพย์การสื่อสารแห่งประเทศไทย — Co-Op PostSaving Result Folder
- **Local folder:** 💻 ~/Desktop/WrokShop/Co-Op PostSaving Result/
- **Status:** Multi-file analytical deliverable
- **Workshop ref:** W-06 สหกรณ์ออมทรัพย์ B2G (current case study)
- **Sensitivity:** ⚠️ government client · check before publishing · likely needs consent
- **Training value:** B2G analytical work · stakeholder mapping · TOR analysis

### 6.2 Taily — Product Engineering Overview
- **Local file:** 💻 ~/Desktop/Taily/Taily_Product_Engineering_Overview.html
- **Training value:** product engineering documentation format

---

## 7. Research & Data Gathering (3 deliverables)

### 7.1 Retail Space Leasing Thailand 7,700 (xlsx)
- **Local file:** 💻 Retail_Space_Leasing_Thailand_7700.xlsx (path TBD)
- **Workshop ref:** W-07 Retail Space Leasing DB (companion data file)
- **Training value:** verifiable data collection methodology · 5-layer moat · 0 fabricated rows

### 7.2 Taily PetFriendly DataHub Global v20 (xlsx)
- **Local file:** 💻 ~/Desktop/Taily/Pet Friendly DB/Taily_PetFriendly_DataHub_Global_v20.xlsx
- **Stack:** 20,000+ records · multi-country
- **Training value:** large-scale data collection · multi-source merging · v1→v20 evolution

### 7.3 Taily DataHub v20 FROZEN Report
- **Local file:** 💻 ~/Desktop/Taily/Taily_DataHub_v20_FROZEN_Report.html
- **Training value:** data freezing/snapshot methodology · v20 final state report

---

## 8. Agent Orchestration (7 deliverables)

> Methodology + frameworks (not artifact apps) · ใช้เป็น operating practice

### 8.1 3C-E Expert Review Panel
- **Workshop ref:** existing CC tab "3C-E Expert Panel"
- **Status:** 📝 methodology + Op 12 enforcement
- **Training value:** Layer-1 panel + Layer-2 CWO review process

### 8.2 Cross-Channel Launch Playbook
- **Workshop ref:** W-08 Cross-Channel Launch (current case study · Post-Songkran archived)
- **Status:** 📝 3-channel broadcast playbook · T-minus 15-min protocol
- **Training value:** All-staff launch coordination

### 8.3 Agent Activation
- **Workshop ref:** B-03 Agent Activation System v1
- **Status:** 📝 Daily 7 / Weekly 12 / On-Demand 32 · activation syntax
- **Training value:** when/how to invoke 63 agents

### 8.4 Morning Brief
- **Workshop ref:** B-01 Morning Brief Reliability Plan v0.6
- **Status:** 📝 daily 6-section brief · "honesty over completeness" rule
- **Training value:** Founder-aligned daily orchestration

### 8.5 Parallel Play · Two-Track Structure
- **Workshop ref:** B-04 Parallel Play Legal Structure
- **Status:** 📝 Nominee Invoicing + IP license model · two-track ANTS + Personal entity
- **Training value:** Legal/financial structure for solo-founder dual-track operation

### 8.6 50-Voter Panel · 5 Dimensions
- **Workshop ref:** B-02 Visual Differentiation Panel Voting
- **Status:** 📝 50-voter × 5-dim scoring + differentiation constraint
- **Training value:** Multi-asset selection methodology (thumbnails/posters/hero images)

### 8.7 ARAI Output Standard (บังคับทุกคน)
- **Workshop ref:** W-09 ARAI Output Standard
- **Status:** 📝 Actions · Results · Idea Improvement standard format
- **Training value:** Universal output discipline · enforced via Op 11+12

---

## Summary Statistics

| Category | Count | Live URLs (🌐) | Local files (💻) | Methodology (📝) | Video (🎬) |
|---|---|---|---|---|---|
| 1. Application Development | 8 | 8 (incl Taily admin K.17 NEW) | 8 (Chat Center) | 0 | 0 |
| 2. Marketing Agency · SEO/AEO | 6 | 0 | 6 | 0 | 0 |
| 3. Marketing Agency · Content (K.17 NEW) | 7 | 0 | 0 | 0 | 7 |
| 4. Network Operation Center | 1 | 0 | 1 | 0 | 0 |
| 5. Pitching & Proposal Deck | 10 | 3 | 5 | 2 | 0 |
| 6. Analytic | 2 | 0 | 2 | 0 | 0 |
| 7. Research & Data Gathering | 3 | 0 | 3 | 0 | 0 |
| 8. Agent Orchestration | 7 | 0 | 0 | 7 | 0 |
| **TOTAL** | **44** | **11** | **25** | **9** | **7** |

Note: some deliverables span multiple categories (e.g., Taily has Application + Pitching + Analytic + Research entries). Counts are intentional duplicates per Workshop linkage logic.

---

## Migration Priority (for GitHub Pages publishing)

### Tier 1 (publish ASAP · low sensitivity · high training value)
1. **All 6 SEO Audits** → `ai-solution-platform/seo-audit-portfolio/` (Yves Rocher · ANTS · PostcatSavings · Sawad · UFS · B-Quik)
2. **NOC Dashboard** → `ai-solution-platform/noc-dashboard/`
3. **Chat Center** (8 HTMLs) → `ai-solution-platform/chat-center/`
4. **Taily Overview + Product Engineering** → `ai-solution-platform/taily-docs/`

### Tier 2 (require sensitivity check first)
5. NokAir Investor Summary — confirm with NokAir before publishing
6. TechVue SAWAD Commercial Model + Solution Proposal — client-confidential · likely keep private
7. Co-Op PostSaving Result — government client · check consent

### Tier 3 (already published · just link)
8. Taily app · RSL · Auto Pilot · MGC Asia · Smart Website (already on GitHub Pages)

---

## Cross-references

- **I-NEW-13 Workshop Output Registry** (memory file `project_idea_improvements_I_NEW_11_to_15.md`) — formal spec for consuming this directory
- **Workshop & Training Program** CC tab — uses these as case study examples in the 4-Phase Journey + 5 Pillars Method
- **10 POC Outputs** CC tab — visual showcase using `WORKSHOPS` array which references this directory
- **GITHUB-SETUP.md** — guide to publish migration Tier 1 items

---

## Action Items (queued · build sprint cycles)

| # | Action | Owner | Effort |
|---|---|---|---|
| A1 | Migrate 6 SEO audits → ai-solution-platform/seo-audit-portfolio/ | Senior Marketing Strategist #26 + Head of Engineering #21 | ~1 hr |
| A2 | Migrate Chat Center 8 HTMLs → ai-solution-platform/chat-center/ | Head of Engineering #21 | ~30 min |
| A3 | Migrate NOC Dashboard → ai-solution-platform/noc-dashboard/ | Head of Engineering #21 | ~10 min |
| A4 | Update Workshop card URLs after migration (replace TBD with new GitHub Pages URLs) | Head of Engineering #21 | ~20 min |
| A5 | Confirm sensitivity for NokAir + TechVue SAWAD + Co-Op (do NOT publish without consent) | Nut + CCVO #52 | varies |
| A6 | Add categories 3 (AI Content) + missing items as Nut completes | Senior Marketing Strategist #26 + CCVO #52 | ongoing |

_Generated K.16 (27 Apr 2026 LATE-PM) by เฌอคูณ + Senior KM #51 + CCVO #52 + Senior Solution Architect #29_
