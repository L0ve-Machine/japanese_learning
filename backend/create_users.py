#!/usr/bin/env python
"""
Create test users for the application
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.users.models import User

def create_users():
    """Create test users"""
    print("🔐 Creating test users...")

    # Admin user
    admin, created = User.objects.get_or_create(
        email='admin@test.com',
        defaults={
            'is_superuser': True,
            'is_staff': True,
            'native_language': 'id',
            'first_name': 'Admin',
            'last_name': 'User'
        }
    )
    if created:
        admin.set_password('admin123')
        admin.save()
        print("✅ Created admin user: admin@test.com / admin123")
    else:
        print("✅ Admin user already exists: admin@test.com")

    # Test user
    test_user, created = User.objects.get_or_create(
        email='test@test.com',
        defaults={
            'is_superuser': False,
            'is_staff': False,
            'native_language': 'id',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    if created:
        test_user.set_password('test123')
        test_user.save()
        print("✅ Created test user: test@test.com / test123")
    else:
        print("✅ Test user already exists: test@test.com")

    # Premium user
    premium_user, created = User.objects.get_or_create(
        email='premium@test.com',
        defaults={
            'is_superuser': False,
            'is_staff': False,
            'native_language': 'id',
            'is_premium': True,
            'first_name': 'Premium',
            'last_name': 'User'
        }
    )
    if created:
        premium_user.set_password('premium123')
        premium_user.save()
        print("✅ Created premium user: premium@test.com / premium123")
    else:
        print("✅ Premium user already exists: premium@test.com")

    print("\n✅ All users created successfully!")
    print("\n📋 Login credentials:")
    print("  Admin: admin@test.com / admin123")
    print("  User:  test@test.com / test123")
    print("  Premium: premium@test.com / premium123")

if __name__ == '__main__':
    create_users()