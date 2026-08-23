# เช็คลิสต์การตรวจสอบ Technical SEO & Performance (Technical Checklist)

เอกสารนี้รวบรวมรายการตรวจสอบทางเทคนิคเชิงลึก เพื่อใช้ประเมินสุขภาพของเว็บไซต์และระบุปัญหาทางเทคนิคที่ขัดขวางการทำงานของ Crawler และการจัดอันดับ

---

## 1. การเข้าถึงและการทำดัชนี (Crawlability & Indexability)

### 1.1 Robots.txt
- [ ] ไฟล์อยู่ที่ Root domain (`/robots.txt`) และส่งคืน HTTP 200 OK
- [ ] ไม่มีคำสั่ง `Disallow: /` บล็อกทั้งเว็บ (เว้นแต่เป็น staging environment)
- [ ] ไม่อนุญาตให้บอทเข้าถึงโฟลเดอร์ที่ไม่จำเป็น (เช่น `/wp-admin/`, `/cart/`, `/checkout/`, `/api/`)
- [ ] มีการระบุตำแหน่งของ XML Sitemap: `Sitemap: https://example.com/sitemap.xml`
- [ ] มีการกำหนดนโยบายสำหรับ AI Crawlers ตามความประสงค์ของธุรกิจ (`GPTBot`, `ClaudeBot`, `PerplexityBot`, `Google-Extended`)

### 1.2 XML Sitemap
- [ ] ไฟล์ Sitemap มีอยู่จริงและผ่านการ Validate ตามมาตรฐาน sitemaps.org
- [ ] ประกอบด้วย URL ที่มีสถานะ 200 OK เท่านั้น (ไม่มี 301, 404, หรือ 500)
- [ ] ไม่มี URL ที่ติดแท็ก `noindex` หรือถูก `Disallow` ใน robots.txt
- [ ] มีระบุ `<lastmod>` ที่เป็นวันที่จริงเมื่อมีการอัปเดต
- [ ] หากมี URL เกิน 50,000 รายการ มีการแยกเป็น Sitemap Index

### 1.3 Meta Robots & Canonicalization
- [ ] หน้าสำคัญไม่มี `<meta name="robots" content="noindex, nofollow">`
- [ ] ทุกหน้ามี `<link rel="canonical" href="...">` ชี้ไปยัง Canonical URL ที่ถูกต้อง
- [ ] Self-referencing canonical มีการใช้งานอย่างถูกต้องในหน้าที่เป็นต้นฉบับ
- [ ] ป้องกันปัญหา Duplicate Content จาก trailing slashes (`/` vs non-slash) และ HTTP/HTTPS หรือ www/non-www

---

## 2. โครงสร้างเว็บและ HTTP Status Hygiene

### 2.1 HTTP Status Codes & Redirects
- [ ] ทุกหน้าเว็บหลักตอบกลับด้วย `200 OK`
- [ ] ลิงก์ที่ย้ายถาวรใช้ `301 Permanent Redirect` (ไม่ใช่ 302 ชั่วคราว)
- [ ] ไม่มี Redirect Chains เกิน 2 hops (A -> B -> C -> D)
- [ ] ไม่มี Redirect Loops (A -> B -> A)
- [ ] หน้า 404 มี Custom Error Page ที่แนะนำผู้ใช้และมี Navigation Bar

### 2.2 โครงสร้าง URL & สถาปัตยกรรมเว็บไซต์ (Architecture)
- [ ] โครงสร้าง URL สั้น อ่านง่าย ใช้ขีดกลาง (`-`) คั่นคำ ไม่ใช้ขีดล่าง (`_`)
- [ ] ไม่มี Parameter ซ้ำซ้อนที่ทำให้เกิด Index Bloat
- [ ] หน้าย่อยสำคัญสามารถเข้าถึงได้ภายใน 3 คลิกจากหน้าแรก (Flat Hierarchy)
- [ ] มีระบบ Breadcrumb Navigation เพื่อช่วยให้ทั้งผู้ใช้และ Search Engine เข้าใจโครงสร้าง

---

## 3. ข้อมูลเชิงโครงสร้าง (Structured Data / Schema.org)

- [ ] ใช้ฟอร์แมต **JSON-LD** (`<script type="application/ld+json">`)
- [ ] ข้อมูลใน Schema ตรงกับสิ่งที่แสดงอยู่บนหน้าเว็บจริง (ไม่หลอกลวงหรือซ่อนข้อมูล)
- [ ] มีการติดตั้ง Schema ประเภทที่เหมาะสม:
  - `Organization` หรือ `LocalBusiness` บนหน้าแรกและหน้า About
  - `WebSite` พร้อม `SearchAction` (Sitelinks Searchbox)
  - `BreadcrumbList` ในทุกหน้าย่อย
  - `Article` / `BlogPosting` ในหน้าบทความ พร้อม `author` และ `datePublished`
  - `Product` พร้อม `offers`, `aggregateRating`, `priceCurrency` ในหน้าสินค้า
  - `FAQPage` ในหน้าที่มีคำถามที่พบบ่อย
- [ ] ทดสอบผ่าน Google Rich Results Test โดยไม่มี Warning หรือ Error ในฟิลด์จำเป็น

---

## 4. Core Web Vitals & ประสบการณ์หน้าเว็บ (Page Experience)

### 4.1 เกณฑ์มาตรฐาน Core Web Vitals (2026 Edition)
- [ ] **LCP (Largest Contentful Paint)**: โหลดองค์ประกอบหลักเสร็จสิ้นภายใน **$\le 2.5$ วินาที**
  - มีการ Preload LCP Image
  - มีการใช้ CDN และ Cache อย่างมีประสิทธิภาพ
  - รูปภาพบีบอัดเป็น WebP หรือ AVIF
- [ ] **INP (Interaction to Next Paint)**: ความหน่วงในการตอบสนองการโต้ตอบ **$\le 200$ มิลลิวินาที**
  - ลดการบล็อก Main Thread จาก JavaScript ที่ทำงานหนัก
  - หลีกเลี่ยง Long Tasks บน Client-side
  - Defer / Async สคริปต์บุคคลที่สาม (Third-party tracking scripts)
- [ ] **CLS (Cumulative Layout Shift)**: ความเสถียรของเลย์เอาต์ **$\le 0.1$**
  - กำหนด `width` และ `height` บนแท็ก `<img>` และ `<video>` ทุกตัว
  - จองพื้นที่สำหรับ Ads / Dynamic Content ล่วงหน้า
  - โหลดฟอนต์ด้วย `font-display: swap` หรือ Preload Webfonts

### 4.2 Mobile Usability & Security
- [ ] มี `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
- [ ] ขนาดปุ่มและลิงก์มี Touch Target อย่างน้อย $44 \times 44$ พิกเซล
- [ ] ใช้งาน HTTPS ทั้งเว็บไซต์ 100% ปราศจาก Mixed Content
- [ ] ไม่มี Pop-up หรือ Intrusive Interstitial ที่บดบังเนื้อหาสำคัญบนหน้าจอมือถือ
