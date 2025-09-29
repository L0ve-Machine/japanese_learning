#!/usr/bin/env python
"""
Create sample users for the Japanese learning application
"""
import os
import sys
import django
from django.conf import settings

# Setup Django environment
sys.path.append('/mnt/c/Users/genki/Projects/web/japanese_learning/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.core.management import call_command

User = get_user_model()

def create_sample_users():
    """Create sample users for testing"""

    # Create superuser
    if not User.objects.filter(email='admin@test.com').exists():
        print("Creating superuser account...")
        superuser = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin123',
            first_name='Admin',
            last_name='User'
        )
        print(f"✅ Superuser created: {superuser.email}")
    else:
        print("✅ Superuser already exists: admin@test.com")

    # Create sample test users
    sample_users = [
        {
            'email': 'tanaka@test.com',
            'password': 'test123',
            'first_name': '田中',
            'last_name': '太郎',
            'native_language': 'vi',  # Vietnamese
        },
        {
            'email': 'nguyen@test.com',
            'password': 'test123',
            'first_name': 'Nguyen',
            'last_name': 'Van A',
            'native_language': 'vi',  # Vietnamese
        },
        {
            'email': 'chen@test.com',
            'password': 'test123',
            'first_name': 'Chen',
            'last_name': 'Wei',
            'native_language': 'zh',  # Chinese
        },
        {
            'email': 'sari@test.com',
            'password': 'test123',
            'first_name': 'Sari',
            'last_name': 'Dewi',
            'native_language': 'id',  # Indonesian
        }
    ]

    for user_data in sample_users:
        if not User.objects.filter(email=user_data['email']).exists():
            user = User(
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                native_language=user_data.get('native_language', 'en')
            )
            user.set_password(user_data['password'])
            user.save()
            print(f"✅ Test user created: {user.email} ({user.first_name} {user.last_name})")
        else:
            print(f"✅ User already exists: {user_data['email']}")

    print("\n📋 Sample Account Summary:")
    print("=" * 50)
    print("🔑 Admin Account:")
    print("   Email: admin@test.com")
    print("   Password: admin123")
    print("   Access: Full admin access")
    print("\n👥 Test User Accounts:")
    print("   Email: tanaka@test.com | Password: test123 | Language: Vietnamese")
    print("   Email: nguyen@test.com | Password: test123 | Language: Vietnamese")
    print("   Email: chen@test.com   | Password: test123 | Language: Chinese")
    print("   Email: sari@test.com   | Password: test123 | Language: Indonesian")
    print("\n🌐 You can now login at: http://localhost:8000/login/")

if __name__ == '__main__':
    create_sample_users()