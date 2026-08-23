# คู่มือ Generative Engine Optimization (GEO) และ AI Search Readiness (2026 Edition)

Generative Engine Optimization (GEO) และ Answer Engine Optimization (AEO) คือกระบวนการปรับแต่งเว็บไซต์เพื่อให้ Large Language Models (เช่น Google AI Overviews, Perplexity, ChatGPT Search, Claude) สามารถดึงเนื้อหาไปประมวลผล สรุป และอ้างอิงเป็นแหล่งข้อมูลที่น่าเชื่อถือได้อย่างแม่นยำ

---

## 1. หลักการสำคัญของ GEO (Core GEO Principles)

1. **Direct Answer First (สรุปคำตอบตรงใน 1-2 ประโยคแรก)**:
   - บอท AI และ Search Overviews จะสแกนหาข้อความที่นิยามหรือตอบคำถามของผู้ใช้อย่างรวดเร็ว
   - ทุกหัวข้อ (`<h2>`/`<h3>`) ควรเริ่มต้นด้วยคำตอบที่กระชับและตรงประเด็นทันที ก่อนที่จะขยายความในเชิงลึก
2. **High Information Density & Extractable Format**:
   - ใช้ Bullet Points, Numbered Lists และตารางเปรียบเทียบข้อมูล
   - หลีกเลี่ยงบทนำที่ยาวเกินไป (No conversational fluff)
3. **Entity and Fact Richness**:
   - ระบุชื่อเฉพาะ ตัวเลข สถิติ หน่วยวัด และคำศัพท์เฉพาะทางอย่างแม่นยำ
   - AI ให้ความน่าเชื่อถือกับเนื้อหาที่มีตัวเลขยืนยันมากกว่าข้อความลอยๆ

---

## 2. มาตรฐานไฟล์ `llms.txt` และ `llms-full.txt`

ไฟล์ `llms.txt` เป็นมาตรฐานใหม่ที่วางไว้ที่ Root domain (`https://example.com/llms.txt`) เพื่อบอก LLMs และ AI Agents ว่าข้อมูลสำคัญของเว็บไซต์อยู่ที่ไหนและมีโครงสร้างอย่างไร

### โครงสร้างตัวอย่างของ `llms.txt`:
```markdown
# Example Brand / Product Name

> คำอธิบายสั้นๆ 1-2 ประโยคว่าเว็บไซต์หรือบริการนี้คืออะไรและให้บริการแก่ใคร

## Core Documentation & Articles
- [ภาพรวมบริการและโซลูชัน](https://example.com/services): รายละเอียดบริการหลักและขอบเขตการทำงาน
- [คู่มือการใช้งานและคำถามพบบ่อย](https://example.com/docs/faq): ตอบคำถามสำคัญและแนวทางแก้ปัญหา
- [งานวิจัยและกรณีศึกษา](https://example.com/case-studies): ผลลัพธ์และข้อมูลสถิติต้นฉบับจากการทดสอบจริง

## Optional
- [ข้อมูลเชิงลึกฉบับเต็ม](https://example.com/llms-full.txt): ไฟล์ Markdown รวบรวมเนื้อหาทั้งหมดสำหรับบริบทขนาดใหญ่
```

---

## 3. การจัดการ AI Crawlers ใน `robots.txt`

พิจารณานโยบายการอนุญาตหรือปฏิเสธ AI Crawlers ในไฟล์ `robots.txt`:

```text
# อนุญาต AI Search Crawlers เพื่อโอกาสในการถูกอ้างอิงในผลค้นหา
User-agent: Google-Extended
Allow: /

User-agent: GPTBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Amazonbot
Allow: /
```

> [!NOTE]
> หากองค์กรมีนโยบายสงวนสิทธิ์ข้อมูลจากการนำไป Train โมเดล แต่ยังต้องการให้ค้นหาเจอใน Search ต้องแยกแยะระหว่าง Search Crawler (เช่น Googlebot, Bingbot) กับ Training Crawlers (เช่น CCBot)

---

## 4. Structured Data สำคัญสำหรับ AI Engine

1. **`FAQPage` Schema**:
   - จับคู่คำถาม-คำตอบที่ตรงกับเนื้อหาบนหน้าจอ ช่วยให้ AI คัดลอกและอ้างอิง Quote ได้ง่าย
2. **`HowTo` Schema**:
   - แยกขั้นตอน (Step-by-step) ที่ชัดเจน ช่วยให้ AI แสดงขั้นตอนการทำงานได้ถูกต้อง
3. **`Person` & `Organization` Schema**:
   - สร้าง Entity Graph ให้ Search Engine เข้าใจว่าใครเป็นผู้เชี่ยวชาญ และองค์กรมีความเชี่ยวชาญในด้านใด (Knowledge Graph Linking)
