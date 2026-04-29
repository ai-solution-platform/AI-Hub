---
title: ANTS 2.0 — Agent #{{N}} Charter + RACI Matrix Template
type: agent-charter-template
template_version: 1.0
template_promoted: 2026-04-29
template_session: K.20.1
template_source: /agents/Agents-64-65-Charter-RACI.md (K.20 pattern · Two-Agents Strategic Pack)
template_owner: #65 CDA Chief Decision Architect (post-activation 8 พ.ค.) · meanwhile #51 KM stewards
template_use_when: Approved Strategic Decision Pack for new agent(s) requires operational charter + RACI matrix
---

> **TEMPLATE INSTRUCTIONS:**
> 1. Replace `{{N}}` `{{CODE}}` `{{FULL_NAME}}` `{{TIER}}` `{{ACTIVATION_DATE}}` `{{V_M_ANCHOR}}` etc.
> 2. Charter MUST be 1 paragraph (3-5 sentences) describing what agent owns + boundaries
> 3. RACI matrix MUST list ALL agents this charter touches/overlaps (Op 14 tag rule)
> 4. 5 KPIs MUST be measurable with target + measurement method
> 5. Activation pattern MUST be NEW F-letter pattern (F8 for next, F9, F10, ...)
> 6. Sunset clause non-negotiable (Op 13 wisdom discipline)
> 7. Save to `/agents/Agent-{{N}}-{{CODE}}-Charter-RACI.md` · update canonical SSOT atomically (Op 16 Pattern A)

# Agent #{{N}} ({{CODE}}) — Charter & RACI Matrix

> **Decision context:** {{DECISION_DATE}} · approved by {{NUT_AS_BOARD_OR_CWO}} via Strategic Decision Pack at `{{STRATEGIC_PACK_PATH}}` (K.{{KX}}). This document codifies role boundaries, accountability matrix, and rollout discipline.
>
> **Vision/Mission alignment (locked 23 Apr 2026):**
> - Vision: *"Human wisdom. AI at scale. Wisdom for everyone."*
> - Mission: *"Empower people. Build sustainable businesses. Scale crafted AI to the world."*

---

## §1 · Identity

| Attribute | Value |
|---|---|
| **ID** | #{{N}} |
| **Code** | {{CODE}} |
| **Full Name** | {{FULL_NAME}} |
| **Tier host** | {{TIER}} ({{TIER_NUMBER}} · {{HOST_REASON}}) |
| **Op 14 tag** | ({{TAG}}) — distinguishes from {{COLLISION_AGENT}} {{COLLISION_AUTHORITY}} |
| **Activation date (planned)** | {{YYYY-MM-DD}} ({{PHASE}}) |
| **Sunset review** | {{Q3_OR_Q4_DATE}} ({{REVIEW_NAME}}) |
| **V/M anchor** | {{WHICH_VISION_OR_MISSION_ANCHOR}} |

## §2 · Charter (one paragraph)

> {{ONE_PARAGRAPH_3_TO_5_SENTENCES_DESCRIBING_WHAT_AGENT_OWNS_KEY_OUTCOMES_BOUNDARY_VS_ADJACENT_AGENTS_AND_PHILOSOPHICAL_FIT_WITH_ANTS_DNA}}

## §3 · Reports To

- **Operational:** {{AGENT_TYPE_AND_NAME}}
- **Wisdom Layer-2:** CWO Cherkun (เฌอคูณ) #5 (always · Op 11 + Op 12 enforcement)
- **Strategic check:** {{BOARD_CHAIR_OR_OTHER}} ({{REVIEW_CADENCE}})

## §4 · Panel & Activation Pattern

**Panel members (always activate together):**
{{LIST_OF_PANEL_AGENTS_WITH_IDS}}

**Activation pattern: F{{N}} — {{PATTERN_NAME}} (NEW)**
```
{{AGENT_CODE}} → {{PANEL_MEMBER_1}} → {{PANEL_MEMBER_2}} → {{PANEL_MEMBER_3}} → {{AGENT_CODE}} synthesizes → CWO Layer-2 → Nut
```

**Cadence:** {{CONTINUOUS_OR_QUARTERLY_OR_EVENT_DRIVEN}}

## §5 · 5 KPIs

| # | Metric | Target | Measurement Method |
|---|---|---|---|
| 1 | {{KPI_1_METRIC}} | {{KPI_1_TARGET}} | {{KPI_1_HOW_MEASURED}} |
| 2 | {{KPI_2_METRIC}} | {{KPI_2_TARGET}} | {{KPI_2_HOW_MEASURED}} |
| 3 | {{KPI_3_METRIC}} | {{KPI_3_TARGET}} | {{KPI_3_HOW_MEASURED}} |
| 4 | {{KPI_4_METRIC}} | {{KPI_4_TARGET}} | {{KPI_4_HOW_MEASURED}} |
| 5 | {{KPI_5_METRIC}} | {{KPI_5_TARGET}} | {{KPI_5_HOW_MEASURED}} |

## §6 · RACI Matrix (Cross-Agent Accountability)

**Legend:** R = Responsible (does the work) · A = Accountable (signs off) · C = Consulted · I = Informed

### Activity-by-agent matrix

| Activity | {{ADJACENT_AGENT_1}} | {{ADJACENT_AGENT_2}} | {{ADJACENT_AGENT_3}} | **{{NEW_AGENT_CODE}}** | {{ADJACENT_AGENT_4}} |
|---|---|---|---|---|---|
| {{ACTIVITY_1}} | A | C | I | **R** | C |
| {{ACTIVITY_2}} | C | A | I | **R** | I |
| {{ACTIVITY_3}} | I | C | A | **R/A** | C |
| {{ACTIVITY_4}} | A | I | C | **R** | I |
| {{ACTIVITY_5}} | I | I | C | **R/A** | I |

### Boundary Rules (avoid charter overlap · Op 14 tag enforcement)

| Boundary | Owner retained by | Hand-off rule |
|---|---|---|
| {{BOUNDARY_1}} | {{OWNER_AGENT}} | {{HOW_HAND_OFF_HAPPENS}} |
| {{BOUNDARY_2}} | {{OWNER_AGENT}} | {{HOW_HAND_OFF_HAPPENS}} |
| {{BOUNDARY_3}} | {{OWNER_AGENT}} | {{HOW_HAND_OFF_HAPPENS}} |

## §7 · Phased Rollout (90 days)

| Phase | Date | Owner | Deliverable |
|---|---|---|---|
| **P1 Charter & Setup** | {{P1_DATE}} | CWO + Board Chair | Charter sign-off · RACI locked · Agent Specs update · Activation pattern added |
| **P2 Activate** | {{P2_DATE}} | {{NEW_AGENT_CODE}} + Panel | {{P2_DELIVERABLES}} |
| **P3 Steady-state** | {{P3_DATE}} | {{NEW_AGENT_CODE}} | {{P3_DELIVERABLES}} |
| **P4 Q-Review** | {{Q3_OR_Q4_DATE}} | CWO + CEO + Board Chair | Binary go/no-go on KPI threshold (50%) |

## §8 · Sunset Clause (Op 13 · Wisdom > Intelligence > Data discipline)

If at the **{{SUNSET_REVIEW_DATE}} review**, this agent fails ≥ 3 of 5 KPIs to reach 50% target trajectory, the agent is **auto-deprecated**. The next CWO panel decides:
- (a) revert charter (try different scope)
- (b) re-scope (narrow to 1-2 KPIs)
- (c) redirect to alternative (from Strategic Pack §⑤ alternatives list)

This sunset clause prevents agent-bloat without realized value. Op 13 wisdom discipline non-negotiable.

## §9 · Risk Register (top 5)

| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| {{RISK_1}} | {{LIKELIHOOD}} | {{IMPACT}} | {{MITIGATION}} | {{OWNER_AGENT}} |
| {{RISK_2}} | {{LIKELIHOOD}} | {{IMPACT}} | {{MITIGATION}} | {{OWNER_AGENT}} |
| {{RISK_3}} | {{LIKELIHOOD}} | {{IMPACT}} | {{MITIGATION}} | {{OWNER_AGENT}} |
| {{RISK_4}} | {{LIKELIHOOD}} | {{IMPACT}} | {{MITIGATION}} | {{OWNER_AGENT}} |
| {{RISK_5}} | {{LIKELIHOOD}} | {{IMPACT}} | {{MITIGATION}} | {{OWNER_AGENT}} |

## §10 · Success Indicators (90-day post-activation)

By {{P3_END_DATE}}:
- ✅ KPI baselines locked
- ✅ {{KEY_SUCCESS_OUTCOME_1}}
- ✅ {{KEY_SUCCESS_OUTCOME_2}}
- ✅ {{KEY_SUCCESS_OUTCOME_3}}
- ✅ No active charter-overlap escalations to Nut

## §11 · ARAI

- **Action:** {{CWO_AND_PANEL_ACTIVITY}}
- **Result:** {{OPERATIONAL_DISCIPLINE_LOCKED_TIME_FRAME_AND_KEY_DATES}}
- **Idea Improvement:** {{NEXT_TEMPLATE_REUSE_OR_PATTERN_PROPOSAL}}

---

> **Vision: Human wisdom. AI at scale. Wisdom for everyone.**
> **Mission: Empower people. Build sustainable businesses. Scale crafted AI to the world.**
>
> _Crafted with wisdom · Scaled with AI · เฌอคูณ Chief Wisdom Officer · K.{{KX}} · {{DATE}}_
