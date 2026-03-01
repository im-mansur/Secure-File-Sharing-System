from cryptography.fernet import Fernet
import os

def generate_key():
    """Generates a new Fernet key (AES-128 in CBC mode with HMAC)."""
    return Fernet.generate_key().decode('utf-8')

def encrypt_file_data(file_data, key_str):
    """
    Encrypts binary file data using the provided Fernet key.
    Returns the encrypted binary data.
    """
    f = Fernet(key_str.encode('utf-8'))
    encrypted_data = f.encrypt(file_data)
    return encrypted_data

def decrypt_file_data(encrypted_data, key_str):
    """
    Decrypts encrypted binary data using the provided Fernet key.
    Returns the original binary data.
    """
    f = Fernet(key_str.encode('utf-8'))
    decrypted_data = f.decrypt(encrypted_data)
    return decrypted_data
