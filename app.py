from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt
import sqlite3
import os
import secrets
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

from config import Config
from utils.db import get_db_connection
from utils.encryption import generate_key, encrypt_file_data, decrypt_file_data

app = Flask(__name__)
app.config.from_object(Config)

# --- Background Task for Auto-Deletion ---
def delete_expired_files():
    """Scheduled task to delete expired files from DB and filesystem."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Find expired files
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("SELECT id, stored_name FROM files WHERE expiry_time <= ?", (now,))
        expired_files = cursor.fetchall()
        
        for f in expired_files:
            file_path = os.path.join(app.config['ENCRYPTED_FILES_DIR'], f['stored_name'])
            # Delete from filesystem
            if os.path.exists(file_path):
                os.remove(file_path)
            
            # Delete from DB
            cursor.execute("DELETE FROM files WHERE id = ?", (f['id'],))
            
        conn.commit()
    except Exception as e:
        print(f"Error in background task: {e}")
    finally:
        if conn:
            conn.close()

# Scheduler setup
scheduler = BackgroundScheduler()
scheduler.add_job(func=delete_expired_files, trigger="interval", minutes=60)
scheduler.start()

# Stop scheduler during shutdown
import atexit
atexit.register(lambda: scheduler.shutdown())

from functools import wraps

# --- Authentication Middleware ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# --- Routes ---

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Hash password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                           (username, email, hashed_password))
            conn.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username or email already exists.', 'danger')
        except sqlite3.Error as e:
            flash(f'Database error: {e}', 'danger')
            print(f"Error: {e}")
        except Exception as e:
            flash('System error. Please try again later.', 'danger')
            print(f"Error: {e}")
        finally:
            if conn:
                conn.close()
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, password_hash FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            
            if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
                session['user_id'] = user['id']
                session['username'] = user['username']
                flash('Logged in successfully.', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password.', 'danger')
        except sqlite3.Error as e:
            flash(f'Database error during login: {e}', 'danger')
            print(f"DB Error: {e}")
        except Exception as e:
            flash('System error during login.', 'danger')
            print(f"Login Error: {e}")
        finally:
            if conn:
                conn.close()
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    user_id = session['user_id']
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('No file part', 'danger')
                return redirect(request.url)
                
            file = request.files['file']
            if file.filename == '':
                flash('No selected file', 'danger')
                return redirect(request.url)
                
            try:
                max_downloads = int(request.form.get('max_downloads', 1))
                expiry_time_str = request.form.get('expiry_time')
                # Parse the datetime-local format: 'YYYY-MM-DDTHH:MM'
                expiry_time = datetime.strptime(expiry_time_str, '%Y-%m-%dT%H:%M')
            except ValueError:
                flash('Invalid max downloads or expiry date format', 'danger')
                return redirect(request.url)

            if file:
                original_name = file.filename
                file_data = file.read()
                
                # Generate Fernet Key and Encrypt
                encryption_key = generate_key()
                encrypted_data = encrypt_file_data(file_data, encryption_key)
                
                # Generate Storage Name and Token
                stored_name = secrets.token_hex(16) + '.enc'
                token = secrets.token_urlsafe(32)
                # expiry_time is already parsed from the form above
                
                # Save Encrypted File
                file_path = os.path.join(app.config['ENCRYPTED_FILES_DIR'], stored_name)
                with open(file_path, 'wb') as f:
                    f.write(encrypted_data)
                    
                # Database Insertion
                cursor.execute('''
                    INSERT INTO files (user_id, original_name, stored_name, encryption_key, token, expiry_time, max_downloads)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (user_id, original_name, stored_name, encryption_key, token, expiry_time.strftime('%Y-%m-%d %H:%M:%S'), max_downloads))
                conn.commit()
                
                flash('File encrypted and uploaded successfully!', 'success')
                return redirect(url_for('dashboard'))

        # Fetch User Files
        cursor.execute("SELECT * FROM files WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
        files = [dict(row) for row in cursor.fetchall()]
        
        # Normalize data for templates (SQLite stores timestamps as strings)
        for f in files:
            if isinstance(f['expiry_time'], str):
                f['expiry_time'] = datetime.strptime(f['expiry_time'], '%Y-%m-%d %H:%M:%S')

        return render_template('dashboard.html', files=files)
    finally:
        if conn:
            conn.close()

@app.route('/download/<token>')
def download(token):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check Token Existence and active status
        cursor.execute("SELECT * FROM files WHERE token = ?", (token,))
        file_record = cursor.fetchone()
        
        if not file_record:
            return render_template('download_error.html', message="Invalid link or file has been deleted.")
            
        # Validate Expiry Time
        # SQLite stored timestamps as strings, convert for comparison
        expiry_time = datetime.strptime(file_record['expiry_time'], '%Y-%m-%d %H:%M:%S')
        if datetime.now() > expiry_time:
            return render_template('download_error.html', message="This download link has expired.")
            
        # Validate Max Downloads
        if file_record['download_count'] >= file_record['max_downloads']:
            return render_template('download_error.html', message="Maximum download limit reached for this file.")
            
        # Validations passed. Log access and Decrypt file.
        ip_address = request.remote_addr
        cursor.execute("INSERT INTO file_access_logs (file_id, ip_address) VALUES (?, ?)", (file_record['id'], ip_address))
        
        # Update download count
        cursor.execute("UPDATE files SET download_count = download_count + 1 WHERE id = ?", (file_record['id'],))
        conn.commit()
        
        file_path = os.path.join(app.config['ENCRYPTED_FILES_DIR'], file_record['stored_name'])
        if not os.path.exists(file_path):
             return render_template('download_error.html', message="File missing from storage.")
             
        with open(file_path, 'rb') as f:
            encrypted_data = f.read()
            
        try:
            decrypted_data = decrypt_file_data(encrypted_data, file_record['encryption_key'])
        except Exception as e:
            print(f"Decryption error: {e}")
            return render_template('download_error.html', message="Error decrypting the file.")
            
        from io import BytesIO
        return send_file(
            BytesIO(decrypted_data),
            download_name=file_record['original_name'],
            as_attachment=True
        )
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)
