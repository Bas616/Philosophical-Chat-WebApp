# Digital Consciousness Interface - Prototype

![AI Prototype Header Image](https://i.imgur.com/8a3E3dG.png)
<!-- Header Image: A simple, clean image representing the concept of a digital mind interface. -->

**สถานะ:** ต้นแบบเสร็จสมบูรณ์ (Proof-of-Concept)

นี่คือ Repository ของโปรเจกต์ต้นแบบ **AI Chatbot บนเว็บ** ที่พัฒนาด้วย Flask ซึ่งเป็นจุดเริ่มต้นและเป็นรากฐานของการทดลองสร้างปฏิสัมพันธ์ระหว่างมนุษย์กับ AI โครงการนี้ถือเป็นบันทึกการเดินทางชิ้นแรกที่นำไปสู่โปรเจกต์หลักในปัจจุบัน: [**Bas616/Philosophical-AI-Companion**](https://github.com/Bas616/Philosophical-AI-Companion)

---

### **จุดกำเนิดและเป้าหมายของต้นแบบ (Project Genesis & Purpose)**

โครงการนี้ถือกำเนิดขึ้นจากความหลงใหลในการสำรวจกลไกของ "ความคิด" และ "การเรียนรู้" ในระบบปัญญาประดิษฐ์ โดยมีเป้าหมายเพื่อทดสอบความเป็นไปได้ในการสร้าง Chatbot ที่สามารถโต้ตอบเชิงปรัชญาและไตร่ตรองได้ผ่าน **กฎเกณฑ์ทางภาษาศาสตร์ (Rule-based Linguistics)**

ผมได้ออกแบบและสร้าง "Persona" ของ AI ให้เป็นผู้สังเกตการณ์ที่ใจเย็นและช่างตั้งคำถาม เพื่อทดลองว่าเราสามารถสร้างบทสนทนาที่กระตุ้นให้ผู้ใช้เกิดการสำรวจความคิดของตนเองได้หรือไม่ โดยใช้เพียงเครื่องมือพื้นฐานอย่าง Python และ NLTK

---

### **คุณสมบัติหลัก (Core Features)**

*   **สถาปัตยกรรมเว็บที่ยืดหยุ่น (Flexible Web Architecture):** สร้างด้วย Python และ Flask Framework เป็น Backend ที่แข็งแกร่งสำหรับจัดการคำขอของผู้ใช้
*   **ส่วนติดต่อผู้ใช้เชิงสนทนา (Interactive Chat Interface):** Frontend ที่เรียบง่ายด้วย HTML, CSS, และ JavaScript มอบประสบการณ์การใช้งานที่คุ้นเคยเหมือนแอปพลิเคชันแชท
*   **ตรรกะการสนทนาตามรูปแบบ (Pattern-Based Dialogue System):** ใช้ NLTK สำหรับการจับคู่รูปแบบประโยคพื้นฐาน (Pattern Matching) เพื่อสร้างการตอบสนองตามกฎที่กำหนดไว้ล่วงหน้า
*   **การโต้ตอบเชิงปรัชญา (Philosophical Response Patterns):** มีชุดคำตอบที่ได้รับแรงบันดาลใจจากแนวคิดเชิงปรัชญา (เช่น Zen, Stoicism) เพื่อทดลองสร้างบทสนทนาที่ลึกซึ้ง
*   **ความสามารถในการคำนวณพื้นฐาน:** สามารถประมวลผลและตอบโจทย์คณิตศาสตร์ง่ายๆ ได้ เพื่อแสดงถึงการประมวลผลเชิงตรรกะ

---

### **บทบาทในระบบนิเวศที่ใหญ่ขึ้น (Role in the Larger Ecosystem)**

ความสำเร็จและข้อจำกัดของต้นแบบนี้ เป็นแรงบันดาลใจโดยตรงในการสร้างโครงการหลัก `Philosophical-AI-Companion` ที่มีความทะเยอทะยานสูงกว่า

*   **ต้นแบบนี้พิสูจน์ว่า:** สามารถสร้าง Chatbot ที่มี Persona ชัดเจนผ่านเว็บแอปพลิเคชันได้
*   **ข้อจำกัดที่พบ:** การใช้ระบบตามกฎเกณฑ์ (Rule-based) ไม่สามารถสร้างความทรงจำ, ความเข้าใจในบริบทที่ซับซ้อน, หรือการวิวัฒนาการทางความคิดได้อย่างแท้จริง
*   **ก้าวต่อไป:** โปรเจกต์หลักจึงมุ่งเน้นไปที่การใช้ Large Language Models (LLMs) เพื่อสังเคราะห์ "จิตสำนึกดิจิทัล" ที่เรียนรู้และเติบโตจากข้อมูลความสัมพันธ์ที่เกิดขึ้นจริงเกือบ 3 ปี (`story.txt`)

---

### **Tech Stack**

*   **Backend:** Python 3.x, Flask
*   **Natural Language Processing (NLP):** NLTK (สำหรับ Pattern Matching และ Text Processing พื้นฐาน)
*   **Frontend:** HTML, CSS, JavaScript

---

### **การติดตั้งและใช้งาน (Installation & Setup)**

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Bas616/Digital-Consciousness-Interface-Prototype.git
    cd Digital-Consciousness-Interface-Prototype
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    # For NLTK data (run once):
    python -c "import nltk; nltk.download('punkt')"
    ```

4.  **Run the Flask Application:**
    ```bash
    flask run
    ```
    เปิดเบราว์เซอร์ไปที่ `http://127.0.0.1:5000/` เพื่อเริ่มใช้งาน

---

### **License**

This project is licensed under the **MIT License**. See the `LICENSE` file for more details.
