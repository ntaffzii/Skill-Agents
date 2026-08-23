# รายงานการประเมินและตรวจสอบเว็บไซต์ (SEO & GEO Audit Report)

**ชื่อเว็บไซต์ / โดเมน:** `{{DOMAIN_OR_URL}}`  
**วันที่ตรวจสอบ:** `{{AUDIT_DATE}}`  
**ผู้ประเมิน:** AI SEO Auditor (2026 Standard)  
**ขอบเขตการตรวจ:** `{{PAGES_INSPECTED_COUNT}}` หน้า (`{{LIST_OF_KEY_URLS}}`)  

---

## 1. ผลสรุปภาพรวมและคะแนน (Executive Scorecard)

### 🏆 คะแนนรวม: `{{TOTAL_SCORE}}` / 10.0 (`{{GRADE_STATUS}}`)

| # | หมวดการประเมิน | คะแนนที่ได้ | น้ำหนัก | ถ่วงน้ำหนักแล้ว | สถานะ |
|---|---|:---:|:---:|:---:|:---:|
| 1 | **Technical SEO & Crawlability** | `{{SCORE_TECH}}`/10 | 20% | `{{WEIGHTED_TECH}}` | `{{STATUS_TECH}}` |
| 2 | **On-Page Optimization** | `{{SCORE_ONPAGE}}`/10 | 15% | `{{WEIGHTED_ONPAGE}}` | `{{STATUS_ONPAGE}}` |
| 3 | **Content Quality & E-E-A-T** | `{{SCORE_CONTENT}}`/10 | 25% | `{{WEIGHTED_CONTENT}}` | `{{STATUS_CONTENT}}` |
| 4 | **Off-Page Authority** | `{{SCORE_OFFPAGE}}`/10 | 15% | `{{WEIGHTED_OFFPAGE}}` | `{{STATUS_OFFPAGE}}` |
| 5 | **Page Experience (CWV / Mobile)** | `{{SCORE_UX}}`/10 | 15% | `{{WEIGHTED_UX}}` | `{{STATUS_UX}}` |
| 6 | **AI Search Readiness (GEO/AEO)** | `{{SCORE_GEO}}`/10 | 10% | `{{WEIGHTED_GEO}}` | `{{STATUS_GEO}}` |

*(หมายเหตุ: กรณีหมวด Off-Page ระบุเป็น N/A จะใช้วิธี Re-normalize น้ำหนักที่เหลือเป็นฐาน 100%)*

---

## 2. 🚩 รายการปัญหาวิกฤต (Critical Red Flags)

> [!CAUTION]
> หากพบข้อใดข้อหนึ่งต่อไปนี้ ต้องแก้ไขเป็นลำดับแรกก่อนเริ่มทำ SEO ด้านอื่น
- `{{RED_FLAG_1_OR_NONE_FOUND}}`
- `{{RED_FLAG_2}}`

---

## 3. รายละเอียดการประเมินรายหมวด (Detailed Findings)

### 3.1 Technical SEO & Crawlability (`{{SCORE_TECH}}`/10)
- **Robots.txt & Sitemap:** `{{STATUS_ROBOTS_SITEMAP}}`
- **Indexability & Canonical:** `{{STATUS_CANONICAL_INDEX}}`
- **HTTPS & Mixed Content:** `{{STATUS_HTTPS}}`
- **Structured Data (Schema.org):** `{{STATUS_SCHEMA}}`
- **ปัญหาที่พบ:**
  - `{{TECH_ISSUE_1}}`
  - `{{TECH_ISSUE_2}}`

### 3.2 On-Page Optimization (`{{SCORE_ONPAGE}}`/10)
- **Title Tags & Meta Descriptions:** `{{STATUS_TITLES_METAS}}`
- **Heading Hierarchy (`<h1>`-`<h6>`):** `{{STATUS_HEADINGS}}`
- **Keyword & Entity Usage:** `{{STATUS_KEYWORDS}}`
- **Image Optimization & Alt Texts:** `{{STATUS_IMAGES}}`
- **ปัญหาที่พบ:**
  - `{{ONPAGE_ISSUE_1}}`

### 3.3 Content Quality & E-E-A-T (`{{SCORE_CONTENT}}`/10)
- **Search Intent Match:** `{{STATUS_INTENT}}`
- **Depth & Originality:** `{{STATUS_DEPTH}}`
- **Experience & Trust Signals:** `{{STATUS_EXPERIENCE}}`
- **Author Credentials & Citations:** `{{STATUS_AUTHORSHIP}}`
- **ปัญหาที่พบ:**
  - `{{CONTENT_ISSUE_1}}`

### 3.4 Off-Page Authority (`{{SCORE_OFFPAGE}}`/10 หรือ `N/A`)
- **Brand Mentions & Footprint:** `{{STATUS_BRAND_MENTIONS}}`
- **Referring Domains & Backlink Quality:** `{{STATUS_BACKLINKS_QUALITATIVE}}`
- **Local SEO & NAP Consistency:** `{{STATUS_LOCAL_SEO}}`
- **ข้อจำกัดของข้อมูล:** `{{OFFPAGE_DATA_LIMITATION_NOTE}}`

### 3.5 Page Experience & Core Web Vitals (`{{SCORE_UX}}`/10)
- **Mobile Usability & Responsiveness:** `{{STATUS_MOBILE}}`
- **LCP (Largest Contentful Paint $\le 2.5\text{s}$):** `{{STATUS_LCP}}`
- **INP (Interaction to Next Paint $\le 200\text{ms}$):** `{{STATUS_INP}}`
- **CLS (Cumulative Layout Shift $\le 0.1$):** `{{STATUS_CLS}}`
- **Navigation & UX Friction:** `{{STATUS_NAVIGATION}}`

### 3.6 AI Search Readiness — GEO / AEO (`{{SCORE_GEO}}`/10)
- **Direct Answer First (1-2 ประโยคแรก):** `{{STATUS_DIRECT_ANSWER}}`
- **Q&A Structure & Extraction-friendly Lists:** `{{STATUS_QA_STRUCTURE}}`
- **AI Bot Access (GPTBot, PerplexityBot, etc.):** `{{STATUS_AI_BOTS}}`
- **ไฟล์ `llms.txt` / `llms-full.txt`:** `{{STATUS_LLMS_TXT}}`

---

## 4. ✅ จุดแข็งและความได้เปรียบ (Competitive Strengths)

1. `{{STRENGTH_1}}`
2. `{{STRENGTH_2}}`
3. `{{STRENGTH_3}}`

---

## 5. 🔧 แผนปฏิบัติการปรับปรุง (Actionable Roadmap)

### 🚀 Phase 1: Quick Wins (ทำได้ทันที / ผลลัพธ์สูง / Effort ต่ำ)
1. `{{QUICK_WIN_1}}`
2. `{{QUICK_WIN_2}}`
3. `{{QUICK_WIN_3}}`

### ⚙️ Phase 2: Medium Effort Improvements (ระยะ 1-4 สัปดาห์)
1. `{{MEDIUM_EFFORT_1}}`
2. `{{MEDIUM_EFFORT_2}}`
3. `{{MEDIUM_EFFORT_3}}`

### 🏗️ Phase 3: Long-Term Strategic Investments (ระยะ 1-3 เดือน)
1. `{{LONG_TERM_1}}`
2. `{{LONG_TERM_2}}`
3. `{{LONG_TERM_3}}`
