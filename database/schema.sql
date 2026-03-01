-- SQLite Schema for Secure File Sharing System

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Files table
CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    original_name TEXT NOT NULL,
    stored_name TEXT NOT NULL,
    token TEXT UNIQUE NOT NULL,
    encryption_key TEXT NOT NULL,
    expiry_time TIMESTAMP NOT NULL,
    max_downloads INTEGER DEFAULT 1,
    download_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- File access logs for security audit
CREATE TABLE IF NOT EXISTS file_access_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id INTEGER NOT NULL,
    ip_address TEXT,
    user_agent TEXT,
    access_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (file_id) REFERENCES files(id)
);

-- Performance Indexes
CREATE INDEX IF NOT EXISTS idx_token ON files(token);
CREATE INDEX IF NOT EXISTS idx_expiry ON files(expiry_time);
CREATE INDEX IF NOT EXISTS idx_user_files ON files(user_id);
CREATE INDEX IF NOT EXISTS idx_token_expiry ON files(token, expiry_time);
