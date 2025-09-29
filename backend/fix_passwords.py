#!/usr/bin/env python
"""
Fix password hashing for users
"""
import os
import sys
import sqlite3
from hashlib import pbkdf2_hmac
import base64
import secrets

def make_password(password, salt=None):
    """Create Django-compatible password hash"""
    if salt is None:
        salt = base64.b64encode(secrets.token_bytes(12)).decode()[:16]

    iterations = 600000
    hash_obj = pbkdf2_hmac('sha256', password.encode(), salt.encode(), iterations)
    hash_b64 = base64.b64encode(hash_obj).decode()

    return f'pbkdf2_sha256${iterations}${salt}${hash_b64}'

def fix_passwords():
    """Fix user passwords in database"""
    db_path = 'db.sqlite3'

    if not os.path.exists(db_path):
        print("❌ Database not found!")
        return

    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Password updates
    users_data = [
        ('admin@test.com', 'admin123'),
        ('test@test.com', 'test123'),
        ('premium@test.com', 'premium123')
    ]

    print("🔐 Updating password hashes...")

    for email, password in users_data:
        hashed_password = make_password(password)
        cursor.execute(
            'UPDATE users SET password = ? WHERE email = ?',
            (hashed_password, email)
        )
        print(f"✅ Updated password for {email}")

    # Commit changes
    conn.commit()
    conn.close()

    print("\n✅ Password hashes updated successfully!")
    print("\n📋 Login credentials:")
    print("  Admin: admin@test.com / admin123")
    print("  User:  test@test.com / test123")
    print("  Premium: premium@test.com / premium123")

if __name__ == '__main__':
    os.chdir('backend')
    fix_passwords()