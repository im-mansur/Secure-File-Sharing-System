import os
import secrets

class Config:
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    
    # File Storage Configuration
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    ENCRYPTED_FILES_DIR = os.path.join(BASE_DIR, 'encrypted_files')
    
    # Database Configuration (SQLite)
    DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'database.db')
    
    # Ensure the storage directory exists
    os.makedirs(ENCRYPTED_FILES_DIR, exist_ok=True)
