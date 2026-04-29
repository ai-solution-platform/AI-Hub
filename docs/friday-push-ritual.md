---
name: Friday Push Ritual — ANTS 2.0 Weekly Discipline
description: Mandatory 4-step Friday 16:00 ICT cadence to push K.x cumulative deltas to GitHub Pages with sensitivity gate · canonical lint · Hub-Index sync verification. Owned by EA #40 + CCVO #52 + #63 FJA-CDCA.
type: reference
i_new: I-NEW-23
locked_date: 2026-04-29
locked_by: Nut (Wise Sprint K.22 · Type-1 approval)
first_run_options: ["2026-05-01 (พรุ่งนี้)", "2026-05-08 (W2-Friday · พร้อม #65 CDA activation)"]
---

# Friday Push Ritual — ANTS 2.0

> **Why:** ป้องกัน workspace drift จาก GitHub Pages · บังคับให้มี audit trail แบบ atomic · ทุกครั้งที่ push ต้องผ่าน 3 gates (sensitivity · canonical · sync) ก่อนจริง
>
> **Cadence:** ทุก **วันศุกร์ 16:00 ICT** (ก่อนปิด week · หลัง mid-session health check รอบสุดท้าย)
> **Time budget:** 15 นาที discipline + 30 นาที automation buffer
> **Ownership chain:** **EA #40** (calendar reminder) → **CCVO #52** (discipline enforcement) → **#63 FJA-CDCA** (audit log)
> **Founder action:** Nut paste 1 command · ตรวจ output · acknowledge

---

## 4-Step Ritual (in order)

### Step 1 · DAS Lint (~3 min)

```bash
cd "/Users/thanakanpermthong/Desktop/AI/ANTS 2.0 - AI Command Center/ANTS 2.0 - AI Command Center"
python3 scripts/vm-canonical-lint.py
```

**Expected output:** `Total: P0=0 · P1=N` (P1 acceptable · P0 blocks push)
**If P0 > 0:** STOP · run `python3 scripts/das-bulk-fix.py --apply` first · re-run Step 1 until P0=0

### Step 2 · Hub-Index Sync Check (~1 min)

```bash
python3 scripts/hub-index-sync-check.py
```

**Expected output:** `ALL CLEAN` across C1–C5 checks (frontmatter version · update_history · primary dashboard refs · body-content diff · path consistency)
**If any check fails:** read finding · fix root file · re-run Step 2

### Step 3 · Publish to GitHub (~2 min · with sensitivity gate)

```bash
./scripts/publish-to-github.sh
```

**The script auto-blocks if it detects:**
- Cash figures (THB \d+M, USD)
- Email addresses (closures@gmail.com etc.)
- PAT tokens (ghp_, sk-)
- Stale "63 agents" / "62 agents" / "52 agents" patterns

**On block:** read the violating file:line · fix · re-run Step 3
**On success:** Pages auto-rebuild 30–60 sec

### Step 4 · Verify URL HTTP 200 (~1 min)

```bash
curl -sI "https://ai-solution-platform.github.io/AI-Hub/ANTS-2.0-Hub-Index.html" | head -1
```

**Expected:** `HTTP/2 200`
**If 404 or 5xx:** wait 60 sec · retry · if still failing → check repo Settings → Pages → Build status

---

## Friday Stop Tape (mandatory before logging off)

Reply in conversation with this 1-line confirmation:

```
✅ Friday Push K.<x> · DAS clean · sync clean · Pages 200 · audit log appended
```

Or, if blocked:

```
🟡 Friday Push K.<x> BLOCKED at Step <N> · reason: <one-line> · next attempt <date>
```

---

## Skip conditions (allowed)

- **Holiday:** ระบุใน EA #40 calendar · skip without penalty · resume next non-holiday Friday
- **Mid-incident:** ถ้ามี P1 incident running → defer push until incident closeout · attach reason in `/reports/Friday-Push-Skip-Log.md`
- **Sensitivity hot-block:** ถ้ามีไฟล์ confidential ที่ตั้งใจห้าม push (กยศ POC · NokAir · TechVue SAWAD · Co-Op สหกรณ์) → already in `.gitignore` · safe to skip

---

## Failure escalation

| Symptom | Action |
|---|---|
| Step 1 P0 > 5 for 2 weeks consecutive | EA #40 + #63 escalate to CWO Layer-2 · Op 13 retro |
| Step 3 sensitivity gate hits 3+ times in a quarter | CCVO #52 + #63 review for cultural drift · update gate regex |
| Step 4 HTTP fails after 3 retries | HoEng #21 + Lead Engineer (H4) Mac terminal debug |
| Stop Tape missing 2 Fridays consecutive | EA #40 ping Nut + line agents · culture audit |

---

## Ownership Matrix (RACI)

| Activity | Responsible | Accountable | Consulted | Informed |
|---|---|---|---|---|
| Calendar reminder Fri 15:45 | EA #40 | CCVO #52 | — | All agents |
| Pre-push sweep (Steps 1+2) | #63 FJA-CDCA | HoEng #21 | KM #51 | — |
| Push command (Step 3) | Nut | Nut | HoEng #21 | EA #40 |
| URL verify (Step 4) | EA #40 | HoEng #21 | — | All agents |
| Audit log append | #63 FJA-CDCA | KM #51 | — | CWO Layer-2 |

---

## Linked

- **Spec:** `project_idea_improvements_I_NEW_21_to_23.md` (memory · I-NEW-23 origin)
- **Sub-spec:** I-NEW-23.1 sensitivity gate · already SHIPPED in `scripts/publish-to-github.sh` (K.18)
- **Related:** Op Principle 18 (Session-Close Sync Discipline) · Op Principle 16 (Cross-Doc SSOT)
- **Decision pending (Type-1):** First push date = **1 พ.ค. 2026** หรือ **8 พ.ค. 2026**?

---

_K.22 Wise Sprint · 29 Apr 2026 · prepared by EA #40 + CCVO #52 + #63 FJA-CDCA · Layer-2 review CWO เฌอคูณ_
