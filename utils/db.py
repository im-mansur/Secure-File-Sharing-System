import sqlite3
import os
from config import Config

def get_db_connection():
    """Establishes and returns a connection to the SQLite database with concurrency optimizations."""
    conn = sqlite3.connect(Config.DATABASE_PATH, timeout=20)
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    
    # Enable WAL mode for better concurrency
    conn.execute('PRAGMA journal_mode=WAL')
    conn.execute('PRAGMA synchronous=NORMAL')
    
    return conn

def init_db():
    """Initializes the database by running the schema.sql file."""
    db_path = Config.DATABASE_PATH
    
    # Ensure the database directory exists if path is deeper
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    with open('database/schema.sql', 'r') as f:
        schema = f.read()

    # SQLite can execute multiple statements at once with executescript
    cursor.executescript(schema)
            
    conn.commit()
    cursor.close()
    conn.close()
    print(f"SQLite Database initialized at {db_path}")

if __name__ == '__main__':
    init_db()
