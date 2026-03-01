# 🔐 SecureShare (Premium File Sharing System)

A high-performance, secure web application for encrypting and sharing files with exact calendar-based time-limited access.

## ✨ Key Features
- **Zero-Install Database**: Uses SQLite for a portable, serverless experience.
- **AES-128 Encryption**: Files are encrypted using the Fernet (Symmetric Encryption) standard.
- **Secure Authentication**: User passwords are securely hashed using `bcrypt`.
- **Premium UI**: Modern Glassmorphism design with a dark-themed aesthetic.
- **Auto-Cleanup**: Background task automatically deletes expired files and records.
- **Secure Links**: URL-safe tokens with configurable download limits and exact calendar-based expiry dates/times.

## 📂 Project Structure
```text
secure_file_share/
├── app.py                 # Core Flask Application & Scheduler
├── config.py              # Configuration & Path Management
├── database.db            # SQLite Database (Auto-created in /database)
├── requirements.txt       # Project Dependencies
├── database/
│   ├── schema.sql         # Database Table definitions
│   └── database.db        # Live Database file
├── static/
│   └── css/
│       └── premium.css    # Custom Premium Design System
├── templates/             # HTML Templates (Gradients & Glassmorphism)
└── utils/
    ├── db.py              # Database initialization & connection logic
    └── encryption.py      # AES Encryption/Decryption utilities
```

## 🚀 Quick Start

### 1. Install Requirements
```bash
pip install -r requirements.txt
```

### 2. Run the App
```bash
python app.py
```

### 3. Use the System
Open **[http://127.0.0.1:5000](http://127.0.0.1:5000)** to:
- **Register/Login**: Access your private vault.
- **Upload**: Select a file, set "Max Downloads" and a specific calendar "Expiry Date & Time", then Encrypt.
- **Share**: Copy the generated link and send it securely.

## 🛡️ Security Note
All files are stored as `.enc` binaries in the `encrypted_files/` directory. They cannot be opened without the unique database-stored encryption keys.

---
*Created with focus on privacy and user experience.*
