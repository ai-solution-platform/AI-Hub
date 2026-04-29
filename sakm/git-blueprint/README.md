---
name: ants-shadow-agent-mesh — Phase 1 Git Repo Blueprint
version: 1.0
last_updated: 2026-04-27
type: blueprint
owner_lead: HoEng #21 (Engineering)
co_owners: KM #51 + #63 FJA-CDCA
status: BLUEPRINT · ready to bootstrap as private GitHub repo
philosophy: "Federated wisdom — every shadow agent is real authority within scope. Collective intelligence — every write-back makes the whole mesh smarter."
update_history:
  - 2026-04-27 K.15 · v1.0 · initial blueprint shipped (template + schema + scripts + workflow)
---

# ants-shadow-agent-mesh · Phase 1 Blueprint

> **One-line:** Single private Git repo that holds the canonical Master agent specs, every shadow's local version, the diff history between them, and the registry that ties it all together.

This is the **Phase 1** scaffold per SAKM v2 architecture. Phase 2 = web dashboard. Phase 3 = full SAKM platform (consider as ANTS IP play).

---

## 1. Why this exists

When Nut exports a plug-in agent to a dream-team member (SC, Growth Team, Sales pilot, etc.) the agent grows in two places at once: the Master (in CC) and the Shadow (in the holder's environment). Without a registry + diff engine, version drift is inevitable within 14 days.

This repo is the **forcing function** that prevents drift, captures write-backs, and keeps Master and Shadow on the same page — the operational layer beneath SAKM's federated wisdom × collective intelligence philosophy.

---

## 2. Repo Layout

```
ants-shadow-agent-mesh/
├── README.md                            (this file)
├── PHILOSOPHY.md                        (federated wisdom × collective intelligence — link)
├── /agents/{agent_id}/
│   ├── master.md                        (canonical spec · pulled from /agents/* in main workspace)
│   ├── boundary.yaml                    (Boundary Contract · per shadow holder)
│   └── /shadows/
│       ├── {holder_slug}.{YYYYMMDD}.md  (snapshot at export · immutable)
│       ├── {holder_slug}.current.md     (live shadow state · pulled at sync)
│       └── /writebacks/
│           ├── {YYYY-MM-DD}__{topic}.md (PR-style write-back proposals)
│           └── /merged/                 (accepted write-backs · audit trail)
├── /registry/
│   ├── shadow-agents.json               (canonical registry · SSOT)
│   ├── shadow-agents.schema.json        (JSON schema)
│   └── /diffs/{YYYY-MM-DD}/
│       ├── {shadow_id}.diff.json        (machine-readable diff)
│       └── {shadow_id}.diff.md          (human-readable diff with section map)
├── /scripts/
│   ├── diff-shadow.py                   (weekly cron · #63 FJA-CDCA)
│   ├── merge-ceremony.py                (run on monthly ceremony)
│   ├── shadow-cli.py                    (Nut's command-line: shadow: list/diff/sync)
│   └── README.md
├── /ceremonies/
│   └── /{YYYY-MM-DD}__{shadow_id}/
│       ├── agenda.md
│       ├── decisions.md
│       └── arai-block.md
├── /templates/
│   ├── Boundary-Contract-Template.yaml
│   ├── Sync-Ceremony-Agenda.md
│   └── Write-Back-Proposal.md
└── /docs/
    ├── ARCHITECTURE.md                  (SAKM v2 5-layer + federated/collective thread)
    ├── ONBOARDING.md                    (I-NEW-12 — Onboarding Kit)
    └── CROSS-POLLINATION.md             (I-NEW-13 — anonymization rules)
```

---

## 3. Bootstrap Plan (Phase 1 · target 14–30 days)

| Step | Owner | Time | Dependencies |
|---|---|---|---|
| 1. Create private GitHub repo `ants-shadow-agent-mesh` | HoEng #21 + Nut | 30 min | GitHub Free private |
| 2. Copy `/sakm/templates/`, `/sakm/registry/` from main workspace | KM #51 | 30 min | sakm/ folder shipped K.15 |
| 3. Bootstrap `agents/` folder with first Master spec (SC's compliance agent) | KM #51 + Nut | 1 hr | identify SC's agent first |
| 4. Sign first Boundary Contract (SC ↔ Nut) | Nut + SC | 30 min | template + 30-min session |
| 5. Register first shadow in `registry/shadow-agents.json` | KM #51 | 15 min | contract signed |
| 6. Wire `diff-shadow.py` into #63 weekly cron | HoEng #21 | 2 hr | script ready (K.15) |
| 7. Run first weekly diff (Mon 4 May or 11 May) | #63 FJA-CDCA | auto | cron wired |
| 8. First merge ceremony (1 Jun 2026) | Nut + SC + KM #51 | 30 min | one month of diffs |

**Total HoEng #21 effort: ~5 hours over 30 days.** Largely setup + automation; ongoing cost ≈ 10 min/week of cron review.

---

## 4. Federated Wisdom × Collective Intelligence — How This Repo Embodies Both

| Concept | How the repo realizes it |
|---|---|
| **Federated wisdom** | Each `/agents/{id}/shadows/` directory is a sovereign branch of authority. Shadow holders (SC, Growth, etc.) make real decisions in their scope · the Boundary Contract makes that authority legible and defensible. |
| **Collective intelligence** | `/writebacks/` is the upstream river. Every learning a shadow earns flows back through PR-style proposals → merged into Master → re-published to all other shadows on next ceremony. The mesh gets smarter every cycle. |
| **The bridge** | `/registry/shadow-agents.json` is the ledger. `/scripts/diff-shadow.py` is the heartbeat. Together they keep Master and Shadow on the same page without forcing either to surrender their own growth. |

---

## 5. Migration Path to Phase 2 (Web Dashboard · 30–90 days)

When Phase 1 has 3+ shadows registered and 2+ write-back cycles complete:

- Static site (Vercel/GitHub Pages) reads `/registry/shadow-agents.json`
- Drift heatmap visualization (per agent · color-coded by `divergence_status`)
- Web-triggered merge ceremony scheduler
- Pattern: identical to Hub-Index portal · same design system

## 6. Migration Path to Phase 3 (SAKM Platform · 90d+)

When Phase 2 has 10+ shadows + auto-merge handling 80%+ of write-backs:

- API-driven sync (replace Git pull/push with REST/webhook)
- Cross-team knowledge graph (visualize cross-pollination edges)
- Integrate with `/scripts/hub-index-sync-check.py` (I-NEW-9) + `vm-canonical-lint.py` (I-NEW-1)
- **Strategic option:** open-source as ANTS IP play (Britz adjacent product · "shadow agent infrastructure for AI-native companies")

---

## 7. Hot Rules + Op Principles This Repo Enforces

- **Op 16 (SSOT):** `/registry/shadow-agents.json` is THE source of truth · every claim about a shadow's state must reconcile to here
- **Op 18 (Session-Close Sync):** every diff/merge must update `last_updated` in registry + write to update_history
- **Op 17 (Naming):** filenames clean · version + date inside content
- **Hot Rule #3 (AI-native first):** scripts run autonomously via #63 cron · human ceremonies are exceptions, not the rule
- **Hot Rule #30 (SAKM cultural framing):** README + docs use "federated wisdom × collective intelligence" framing · NEVER "AI replaces"

---

## 8. Linked Specs (read these before bootstrapping)

- `/sakm/templates/Boundary-Contract-Template.yaml` — contract template (K.15)
- `/sakm/registry/shadow-agents.schema.json` — JSON schema (K.15)
- `/sakm/registry/shadow-agents.json` — initial registry with SC placeholder (K.15)
- `/sakm/git-blueprint/scripts/diff-shadow.py` — weekly diff script (K.15)
- `/sakm/git-blueprint/scripts/merge-ceremony.py` — ceremony runner (K.15)
- `/internal-transformation/ANTS-SAKM-MasterSpec.md` — v1 5-layer architecture (28 Apr)
- `/reports/I-NEW-11-shadow-command-spec.md` — `shadow:` CLI command (K.15)
- `/reports/I-NEW-12-shadow-agent-onboarding-kit.md` — repeatable export process (K.15)
- `/reports/I-NEW-13-cross-shadow-cross-pollination.md` — anonymization rules (K.15)

---

_Crafted with wisdom, scaled with AI · เฌอคูณ · 27 Apr 2026 K.15_
