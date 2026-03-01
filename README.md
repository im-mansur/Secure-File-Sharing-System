<!-- ================= Animated Header ================= -->
<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:0F2027,50:203A43,100:2C5364&height=220&section=header&text=SecureShare&fontSize=50&fontColor=ffffff&animation=fadeIn&fontAlignY=35&desc=Premium%20Encrypted%20File%20Sharing%20System&descAlignY=55&descAlign=50" />
</p>

<h1 align="center">🔐 SecureShare</h1>
<h3 align="center">Privacy-Focused • AES-128 Encrypted • Time-Limited Access</h3>

<!-- Typing Animation -->
<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?color=00C2FF&size=22&center=true&vCenter=true&width=700&lines=Encrypted+File+Storage;Secure+Token-Based+Sharing;Calendar-Based+Expiry;Auto-Cleanup+System;Cybersecurity+Focused+Architecture" />
</p>

---

# 🚀 Overview

SecureShare is a **high-performance encrypted file sharing web application** that allows users to securely upload, encrypt, and share files with exact calendar-based expiry time and download limits.

Designed for:

- 🔐 Maximum privacy  
- ⚡ Fast secure access  
- 🧠 Smart automated cleanup  
- 🎨 Premium UI experience  

---

# 🧱 Complete Tech Stack

<p align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite)
![MySQL](https://img.shields.io/badge/MySQL-00758F?style=for-the-badge&logo=mysql&logoColor=white)
![AES-128](https://img.shields.io/badge/Encryption-AES--128-blue?style=for-the-badge)
![Fernet](https://img.shields.io/badge/Fernet-Symmetric%20Encryption-success?style=for-the-badge)
![bcrypt](https://img.shields.io/badge/Auth-bcrypt-green?style=for-the-badge)
![APScheduler](https://img.shields.io/badge/Scheduler-APScheduler-orange?style=for-the-badge)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-000000?style=for-the-badge)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)

</p>

---

# ✨ Key Features

### 🔐 AES-128 File Encryption
- Fernet symmetric encryption
- Unique encryption key per file
- Encrypted at rest storage

### 🔑 Secure Authentication
- bcrypt password hashing
- Secure session handling
- Protected user vault

### ⏳ Calendar-Based Expiry
- Set exact expiry date & time
- Download limits
- Optional one-time download

### 🗑️ Auto Cleanup System
- Background scheduler
- Deletes expired files automatically
- Cleans database records

### ⚡ Optimized Database Indexing
- Token index for fast lookup
- Expiry index for cleanup efficiency
- User-based indexing for dashboard

---

# 🗄️ Database Architecture

### Users Table
- id  
- username  
- email  
- password_hash  
- created_at  

### Files Table
- id  
- user_id  
- original_name  
- stored_name  
- encryption_key  
- token  
- expiry_time  
- download_count  
- max_downloads  
- upload_time  

### Indexing Strategy
- INDEX on token  
- INDEX on expiry_time  
- INDEX on user_id  
- Composite INDEX (token, expiry_time)  

---

# 🔄 System Workflow

1️⃣ User uploads file  
2️⃣ File encrypted using AES-128  
3️⃣ Encrypted file stored in `/encrypted_files/`  
4️⃣ Metadata stored in SQLite  
5️⃣ Secure token generated  
6️⃣ On access → token + expiry validated  
7️⃣ File decrypted and served  
8️⃣ Background scheduler deletes expired files  

---

# 📂 Project Structure

```text
SecureShare/
│
├── app.py
├── config.py
├── database/
│   ├── schema.sql
│   └── database.db
├── encrypted_files/
├── static/
│   └── css/
├── templates/
└── utils/
```

---

# ▶️ Installation & Setup

```bash
git clone https://github.com/im-mansur/Secure-File-Sharing-System.git
cd Secure-File-Sharing-System
pip install -r requirements.txt
python app.py
```

Open:

```
http://127.0.0.1:5000
```

---

# 🛡️ Security Design

- 🔐 Encryption at Rest  
- 🔑 Unique File-Level Keys  
- ⏳ Expiry-Based Access Control  
- 📊 Download Count Enforcement  
- 🧹 Automated Expired Data Deletion  
- ⚡ Indexed Secure Lookup  

---

# 🔮 Future Enhancements

- ☁️ AWS S3 Cloud Storage  
- 📧 Secure Email Link Sharing  
- 📊 Admin Analytics Dashboard  
- 📱 Mobile Optimization  
- 🔐 Two-Factor Authentication  

---
## 📸 Screenshots

![Dashboard Preview](https://github.com/im-mansur/Secure-File-Sharing-System/blob/main/preview.png)
---

# 🎓 Project Type

Cybersecurity System  
Full Stack Web Application  
Portfolio + Production Prototype  

---

<p align="center">
  ⭐ If you like this project, give it a star!
</p>

<!-- ================= Footer Wave ================= -->
<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:2C5364,100:0F2027&height=150&section=footer"/>
</p>





