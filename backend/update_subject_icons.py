#!/usr/bin/env python
"""
Script to update existing subjects with appropriate icons and colors
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.learning.models import Subject

def update_subjects():
    """Update all subjects with appropriate icons and colors"""

    updates = [
        # (id, icon, color, description)
        (1, 'medical_services', '#4caf50', 'Healthcare subject'),
        (2, 'chat', '#2196f3', 'Conversation subject'),
        (3, 'people', '#ff9800', 'Social interaction subject'),
        (4, 'assignment', '#9c27b0', 'Evaluation subject'),
        (5, 'home', '#795548', 'Lifestyle subject'),
        (7, 'quiz', '#ffc107', 'Testing subject'),
    ]

    updated_count = 0

    for subject_id, icon, color, desc in updates:
        try:
            subject = Subject.objects.get(id=subject_id)
            subject.icon = icon
            subject.color = color
            subject.save()
            print(f"[OK] Updated Subject {subject_id}: {icon} {color} ({desc})")
            updated_count += 1
        except Subject.DoesNotExist:
            print(f"[SKIP] Subject {subject_id} not found")

    print(f"\n[SUCCESS] Updated {updated_count}/{len(updates)} subjects successfully!")

    # Display all subjects
    print("\n" + "="*60)
    print("All Subjects:")
    print("="*60)
    for subject in Subject.objects.all().order_by('id'):
        print(f"ID {subject.id}: {subject.name}")
        print(f"  Icon: {subject.icon}")
        print(f"  Color: {subject.color}")
        print(f"  Items: {subject.items.count()}")
        print("-" * 60)

if __name__ == '__main__':
    update_subjects()
