# PLAN.md — ปรับใช้ UI skills ภายนอกกับ Skill-Agents

> **Status:** Phase 1 เสร็จ 2026-11-22 (Step 0–6) — ยังไม่ commit, ยังไม่ sync, ยังไม่ได้ทดลองรีวิวหน้าจริงด้วย Playwright; Phase 2 เลื่อนไว้
> **Note Step 6:** `validate-all.ps1` ใช้ไม่ได้ในรีโปนี้ (ต้องมีโฟลเดอร์ `mcp-tools` ของรีโปคู่หู) จึงรัน `validate-skills.ps1` (55 skills ผ่าน) และ `validate-skills-index.ps1` แทน; index เก่ามาก่อนแล้วเพราะ `deep-planning` ยังไม่อยู่ใน index → สร้างใหม่ ทำให้มี 59 entries
> **Created:** 2026-11-22 · **Owner agent:** `architect` (วางแผน) → `implementer` (หลังอนุมัติเท่านั้น)
> **Revision note (2026-11-22):** หลังทำ Step 0 พบว่า uizze anti-ui-slop เป็น adaptation ของ Impeccable (Apache-2.0) + บริการอ้างอิงแบบเสียเงิน ไม่มีเนื้อหาใหม่ที่ซ้ำกับ Hallmark/ของเรา → **ตัด uizze ออกจากแหล่งเนื้อหาและเครดิต** ที่เหลือไม่เปลี่ยน

## Step 0 result — ข้อที่ขาดจริง (อ่าน upstream แล้ว)

อ่านครบ: make-interfaces-feel-better (5 ไฟล์ย่อย), emil `emil-design-eng` / `review-animations` / `animation-performance`, Hallmark `SKILL.md` (Floor), uizze `anti-ui-slop` + NOTICE/MODIFICATIONS, และ `ui-audit.md` + `SKILL.md` ของเรา (ไม่ได้อ่านกฎ lint ลึกของ Hallmark ไม่ได้ตรวจ Taste Skill — อยู่ Phase 2)

**ของเรามีแล้ว (ไม่เขียนซ้ำ):** ห้าม card ซ้อน card, tabular numerals, motion ใช้ transform/opacity, `will-change` เฉพาะที่, reduced motion, ไม่ใช้ gradient/glow เกินเหตุ, โหมด Polish (มีแต่ชื่อ), finish-gate ใน browser

**ขาดจริง → Step 1 (`interaction-craft.md`):** ตัดสินว่าควร animate ไหมตามความถี่ใช้งาน, easing (ห้าม ease-in กับ UI), งบเวลา, transform-origin ของ popover และการเริ่มจาก scale(0), transition ที่ interrupt ได้ vs keyframes, enter/exit ไม่สมมาตร, gate hover ด้วย `(hover: hover)`, ห้าม `transition: all`, concentric radius, optical alignment, shadow vs border, image outline, hit area, `text-wrap`, font smoothing, icon (stroke/`currentColor`/outline→fill/RTL), เทคนิคเล่นซ้ำ 10%

**ขาดจริง → Step 2 (`anti-slop.md`):** เกต 3 ระดับ, อาการเฉพาะ (eyebrow, ป้ายตัวพิมพ์ใหญ่ขยายระยะ, คำเดียวใน heading ที่ใส่สี/เอียง, meta คั่นด้วย middle dot, จุดสถานะประดับ, emoji เป็นไอคอน, หน้าต่าง browser วาดเอง, ตัวเลข/คำรับรองที่แต่งขึ้น), สี/ฟอนต์ผ่าน token, hero เห็นครบใน 1280×800, reviewer ที่ไม่มี context ผู้สร้าง

## Goal

เติมช่องว่างด้านงาน polish/ตรวจ "AI slop" ใน `skills/engineering/ui-design-engineering` โดยเขียนใหม่ตามแนวคิดของ skill ภายนอกที่คัดแล้ว ไม่ใช่ติดตั้งทั้ง 10 ตัวหรือคัดลอกไฟล์มา

## Assumptions

- รีโปนี้เป็น "skill layer" ที่เน้นเขียนใหม่ตามแบบแผนของตัวเอง (ดู `NOTICE.md` หัวข้อ What Was Reused) ไม่ vendor ไฟล์ upstream
- งาน UI ของผู้ใช้ส่วนใหญ่คือ dashboard/SaaS/admin ตามที่ `ui-design-engineering` ระบุ ไม่ใช่ landing page อย่างเดียว
- ใช้กับ local LLM ได้ด้วย จึงต้องคุมขนาด `SKILL.md` (ปัจจุบัน 171 บรรทัด) และโหลดรายละเอียดผ่าน `references/` เมื่อจำเป็น
- ยังไม่ได้อ่านเนื้อ `SKILL.md` ของ upstream ส่วนใหญ่ ข้อมูลด้านล่างมาจาก README, รายชื่อไฟล์ และ `SKILL.md` ของ make-interfaces-feel-better เท่านั้น → Step 0 จึงเป็นการอ่านก่อนลงมือ
- Skill ระดับผู้ใช้ `unslop` (อยู่นอกรีโปนี้) มีเป้าหมายใกล้เคียงกับส่วน anti-slop ต้องไม่ซ้ำกัน

## สถานะของ 10 skill ที่ผู้ใช้ส่งมา

| # | Skill | License | ที่เรามีแล้ว | การตัดสินใจ |
|---|---|---|---|---|
| 1 | Anti UI Slop (uizze) | MIT / Apache-2.0 (ตรวจไฟล์ LICENSE ของ skill) | แนวคิด "ต้านความ generic" กว้างๆ | **ใช้แนวคิด** → anti-slop (Phase 1) |
| 2 | Impeccable | Apache-2.0 | ใช้เป็นโครง enhancement modes แล้ว | **ไม่ทำเพิ่ม** (ตรวจเฉพาะว่า `polish` ยังเป็นแค่ชื่อโหมด) |
| 3 | Taste Skill | MIT | ไม่มี | **เลื่อน** → Phase 2 หลังอ่านเนื้อ |
| 4 | Frontend Design (Anthropic) | ไม่ระบุ (ต้องตรวจในโฟลเดอร์ skill) | ใช้เป็นแรงบันดาลใจแล้ว | **ไม่ทำเพิ่ม** |
| 5 | UI UX Pro Max | MIT | ดัดแปลงใน `ux-ui-design-assessment` แล้ว | **ข้าม** (ซ้ำ + ต้องใช้ Python scripts) |
| 6 | Hallmark | MIT | ไม่มี | **ใช้แนวคิด** → anti-slop (Phase 1) |
| 7 | Vercel Web Design Guidelines | repo `license: null` | ดัดแปลงใน `ux-ui-design-assessment` แล้ว | **ข้าม** — อ้างอิงเท่านั้น ห้ามคัดลอก |
| 8 | Emil Design Engineering | MIT | อ้างชื่อใน credits แต่ไม่มีเนื้อหา | **ใช้แนวคิด** → interaction-craft (Phase 1) |
| 9 | Make Interfaces Feel Better | MIT | อ้างชื่อใน credits แต่ไม่มีเนื้อหา | **ใช้แนวคิด** → interaction-craft (Phase 1) |
| 10 | Stageshow | ไม่ระบุ | ไม่มี | **ข้าม** (ทำภาพ UI จำลอง ไม่ตรงงานของรีโป) |

## Options considered

1. **เพิ่มเป็น reference ใต้ `ui-design-engineering`** — optimizes for: แก้น้อย, ไม่เพิ่ม routing/index, โหลดตามต้องการ; tradeoff: skill เดียวใหญ่ขึ้น และ trigger แยกเฉพาะ "polish" ไม่ได้; cost: **small–medium**
2. **แยกเป็น skill ใหม่** (`ui-polish`, `ui-anti-slop`) — optimizes for: trigger ตรงเป้า, เรียกใช้เดี่ยวได้; tradeoff: ต้องแก้ `data/skills-index.json`, toolsets, validators, sync ไปทุก provider และเพิ่มความเสี่ยงซ้ำกับ `ui-design-engineering`; cost: **medium**
3. **ติดตั้ง/คัดลอก upstream ทั้งชุด** — optimizes for: เร็วที่สุด; tradeoff: ขัดหลัก "reuse ideas not files" ใน `NOTICE.md`, ต้องตามดู license ทีละตัว (บางตัว `null`), ดูแล drift เอง, ใช้ context เปลืองกับ local LLM; cost: **small แต่หนี้สูง**

## Chosen approach

**Option 1** — เพราะ `ui-design-engineering` มีโครง modes และ `credits.md` อ้างทั้งสองแนวคิดนี้อยู่แล้ว การเพิ่ม reference คือการทำให้คำอ้างนั้นเป็นจริงด้วยการแก้น้อยที่สุด ถ้าภายหลังใช้งานจริงแล้ว polish/anti-slop ถูกเรียกแยกบ่อย ค่อยแยกเป็น skill (Option 2)

## Steps

### Step 0 — อ่านก่อนเขียน (ไม่แก้ไฟล์)
- อ่านเนื้อ `SKILL.md` และ license ของ: `emilkowalski/skills` (`emil-design-eng`, `review-animations`, `animation-performance`, `animation-vocabulary`), `Nutlope/hallmark` (`skills/hallmark`, กฎ lint), `uizze/uizze` (`skills/anti-ui-slop` + `LICENSE`/`NOTICE`/`MODIFICATIONS.md`), และ `make-interfaces-feel-better` ไฟล์ย่อย (typography, surfaces, animations, icons, performance)
- ตรวจ license ของ `anthropics/skills/skills/frontend-design` (ใช้แค่ยืนยัน ไม่ได้จะเขียนเพิ่ม)
- อ่าน `ui-design-engineering/references/ui-audit.md` (93 บรรทัด) เพื่อจดว่าอะไรครอบคลุมแล้ว
- **ผลลัพธ์:** รายการ "ข้อที่ขาดจริง" สั้นๆ แนบท้ายแผนนี้ ก่อนเริ่ม Step 1

### Step 1 — `references/interaction-craft.md` (ใหม่)
เนื้อหาที่เขียนใหม่เป็นภาษาของรีโป: concentric border radius, optical alignment, shadow vs border, transition ที่ interrupt ได้, easing สำหรับ enter/exit, hit area, tabular numerals/text wrapping, icon states, ความยับยั้งของ motion, เทคนิครีวิว motion ที่ความเร็ว 10% ใน Animations panel
- เขียนเป็นหลักการ + เหตุผล + วิธีตรวจ ไม่ล็อกค่าตัวเลขตายตัวนอกจากที่ตรวจสอบแล้ว
- ต้องบอกให้ "แสดงผลในระบบ styling ที่โปรเจกต์ใช้อยู่ ห้ามเพิ่มระบบ styling ใหม่" (หลักข้อนี้จาก make-interfaces-feel-better ตรงกับ Framework Awareness ที่เรามี)

### Step 2 — `references/anti-slop.md` (ใหม่)
- แบ่งเกต 3 ระดับ: **Floor** (ห้ามปล่อย: contrast, focus, reduced motion, ข้อมูลที่แต่งขึ้น, เลย์เอาต์มือถือพัง) / **Reflex** (ค่าเริ่มต้นที่โมเดลมักทำ ยกเว้นได้ถ้าบันทึกเหตุผล) / **Finish** (รายละเอียดงานฝีมือ ไม่บล็อกการส่ง)
- รายการอาการ (tells) เขียนเอง แยกตามชนิดหน้า: **marketing/landing** vs **product/dashboard** เพื่อไม่ให้กฎของ landing page ไปบังคับ dashboard
- ขั้นตอนตรวจใน browser จริงโดยใช้ toolset เดิม (`browser`, `playwright`) พร้อมสั่งให้ใช้ reviewer ที่ไม่มี context ของผู้สร้างตามแนว Hallmark
- ตัดการกำหนดธีม 50 แบบของ Hallmark ออก (ไม่ใช่งานของ skill นี้)

### Step 3 — เชื่อมเข้า `SKILL.md`
- ใน **Enhancement Modes** เพิ่มชี้ไป `interaction-craft.md` ที่โหมด `polish` และ `anti-slop.md` ที่ Review mode
- ใน **Final Quality Checks** เพิ่ม 1–2 บรรทัดให้รัน Floor gate
- เป้าหมายขนาด `SKILL.md` ไม่เกิน ~190 บรรทัด และอัปเดตส่วน Source And Attribution

### Step 4 — `ui-audit.md`
เพิ่มลิงก์/แถว checklist สั้นๆ ที่ชี้ไป reference ใหม่ ไม่คัดลอกเนื้อซ้ำ

### Step 5 — เครดิตและ license
- `ui-design-engineering/references/credits.md` และ `NOTICE.md`: เพิ่มรายการ Emil Kowalski, Jakub Krehel, Hallmark (Nutlope / Together AI), uizze พร้อม license ที่ตรวจแล้ว และข้อความว่า "ไม่ได้คัดลอกข้อความ/โค้ด"
- ถ้าขั้นใดยกข้อความจาก upstream มาตรงๆ ต้องใส่หมายเหตุระดับไฟล์ตามที่ `NOTICE.md` กำหนด (หลีกเลี่ยงไว้ก่อน)

### Step 6 — ทะเบียนและตรวจสอบ
- รัน `scripts/generate-skills-index.ps1` เพื่ออัปเดต `data/skills-index.json` (ถ้ามีการเปลี่ยน description)
- รัน `scripts/validate-all.ps1`
- **ไม่รัน `sync.ps1` เอง** เพราะจะเขียนไปยัง provider อื่นนอกรีโป → ถามผู้ใช้ก่อน

### Phase 2 (แยกอนุมัติ — ไม่รวมในรอบนี้)
- อ่าน Taste Skill เพื่อดูว่าแนว "art direction + reference image + browser check" เพิ่มอะไรเกินกว่า Step 2 ถ้าซ้ำให้ตัดทิ้ง
- ประเมินว่าควรแยก `ui-polish` เป็น skill ของตัวเองไหม หลังใช้ Phase 1 จริง

## Risks / edge cases

- **ข้อมูลไม่ครบ:** ยังไม่ได้อ่านเนื้อ upstream ส่วนใหญ่ → Step 0 เป็นด่านบังคับ ถ้าพบว่าส่วนใดซ้ำกับของเรามาก ให้ลดขอบเขต Step 1–2 ลง
- **License:** vercel-labs/agent-skills และ benjitaylor/skills ขึ้น `license: null` → ห้ามคัดลอก ใช้เป็นแนวคิดทั่วไปเท่านั้น; uizze ระบุสองใบอนุญาต ต้องดูว่า skill ย่อยใช้ใบไหน
- **Context บวม:** local LLM โหลด `SKILL.md` ทั้งไฟล์ → ต้องคุมขนาด และให้ reference ถูกโหลดตามต้องการ
- **กฎ landing page ไปลง dashboard:** อาการอย่าง "eyebrow เหนือ heading" ไม่ใช่ข้อผิดพลาดใน admin tool → แยกตามชนิดหน้าและให้ Reflex ยกเว้นได้
- **ซ้ำกับ `unslop`:** ถ้าผู้ใช้เรียกทั้งสอง คำแนะนำอาจขัดกัน → ระบุขอบเขตใน reference ว่านี่คือ checklist ตรวจ ไม่ใช่ขั้นตอน redesign
- **ค่าตัวเลขตายตัวจาก upstream** (เช่นสเกล/blur ของ icon animation) อาจไม่เหมาะกับทุก design system → ใช้เป็นค่าแนะนำพร้อมเหตุผล ไม่ใช่กฎ
- **Upstream เปลี่ยนเร็ว** (repo เหล่านี้ push เกือบทุกสัปดาห์) → บันทึกวันที่อ่านใน credits
- **ผลข้างเคียงต่อ provider อื่น:** การ sync ไปหลาย provider ย้อนกลับยาก → ถามก่อน

## Verification

- `scripts/validate-all.ps1` ผ่านทั้งหมด และ `data/skills-index.json` ตรงกับ frontmatter ใหม่
- `SKILL.md` ไม่เกินเป้าหมายบรรทัด และลิงก์ทุกอันใน skill เปิดไฟล์จริงได้
- ค้นหาข้อความยาวซ้ำกับ upstream: ไม่มีประโยคที่คัดลอกมาตรงๆ เกินสั้นๆ
- ทดลองจริง 1 ครั้ง: ให้ skill รีวิวหน้าเว็บตัวอย่างหนึ่งหน้าผ่าน Playwright แล้วดูว่า findings อ้างอิง reference ใหม่ และแยกชนิดหน้าถูก
- `NOTICE.md` และ `credits.md` ระบุ license ครบทุก upstream ที่ใช้

## Open questions (มีค่าเริ่มต้นแล้ว ตอบเมื่อไม่เห็นด้วย)

1. ภาษาของ reference ใหม่: **อังกฤษ** (ตามไฟล์เดิมในรีโป) — เปลี่ยนเป็นไทยได้
2. ให้รัน `sync.ps1` หลังจบไหม: **ไม่** จนกว่าจะสั่ง
3. Phase 2 (Taste Skill / แยก skill): **เลื่อน** ตัดสินหลัง Phase 1

## Handoff

หลังอนุมัติ: `architect` ทำ Step 0 และสรุป "ข้อที่ขาดจริง" → ขอยืนยันอีกครั้งถ้าขอบเขตเปลี่ยนมาก → `implementer` ทำ Step 1–6 ตามที่อนุมัติเท่านั้น
