#!/usr/bin/env python
"""
Simple database setup script for Japanese Learning Platform
"""
import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

try:
    django.setup()

    # Import after Django setup
    from django.core.management import execute_from_command_line
    from django.contrib.auth import get_user_model
    from django.db import transaction

    print("🗂️ Setting up Japanese Learning Database...")

    # Run migrations
    print("1. Running migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migrations completed successfully")
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        sys.exit(1)

    # Create users
    print("\n2. Creating user accounts...")
    User = get_user_model()

    users_to_create = [
        {
            'email': 'admin@test.com',
            'password': 'admin123',
            'is_staff': True,
            'is_superuser': True,
            'native_language': 'id'
        },
        {
            'email': 'test@test.com',
            'password': 'test123',
            'is_staff': False,
            'is_superuser': False,
            'native_language': 'id'
        },
        {
            'email': 'premium@test.com',
            'password': 'premium123',
            'is_staff': False,
            'is_superuser': False,
            'native_language': 'id',
            'is_premium': True
        }
    ]

    with transaction.atomic():
        for user_data in users_to_create:
            email = user_data['email']

            if User.objects.filter(email=email).exists():
                print(f"✅ User {email} already exists")
            else:
                password = user_data.pop('password')
                user = User(**user_data)
                user.set_password(password)
                user.save()
                print(f"✅ Created user: {email}")

    print("\n🎯 Database setup completed!")
    print("\n📋 Available accounts:")
    print("  Admin: admin@test.com / admin123")
    print("  User:  test@test.com / test123")
    print("  Premium: premium@test.com / premium123")
    print("\n🌐 Access your site at: http://localhost:8000/")

except Exception as e:
    print(f"❌ Setup failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)