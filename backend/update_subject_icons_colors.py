"""
Update script to set icons and colors for all subjects
Based on SUBJECT_ICON_COLOR_SETUP.md recommendations
"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.learning.models import Subject

# Subject icon and color mapping based on recommendations
SUBJECT_CONFIG = {
    '介護試験対策': {
        'icon': 'medical_services',
        'color': '#4caf50'
    },
    '介護の実務会話': {
        'icon': 'chat',
        'color': '#2196f3'
    },
    '日本人と会話': {
        'icon': 'people',
        'color': '#ff9800'
    },
    '特定技能評価試験': {
        'icon': 'assignment',
        'color': '#9c27b0'
    },
    '日本の生活マナー': {
        'icon': 'home',
        'color': '#795548'
    },
    'testing': {
        'icon': 'quiz',
        'color': '#ffc107'
    }
}

def update_subjects():
    """Update icon and color for all subjects"""
    updated_count = 0
    not_found = []

    for subject_name, config in SUBJECT_CONFIG.items():
        try:
            subject = Subject.objects.get(name=subject_name)
            subject.icon = config['icon']
            subject.color = config['color']
            subject.save()
            print(f"[OK] Updated: {subject_name} - {config['icon']} ({config['color']})")
            updated_count += 1
        except Subject.DoesNotExist:
            print(f"[SKIP] Not found: {subject_name}")
            not_found.append(subject_name)

    print(f"\n{'='*50}")
    print(f"Updated: {updated_count} subjects")
    if not_found:
        print(f"Not found: {', '.join(not_found)}")
    print(f"{'='*50}")

if __name__ == '__main__':
    print("Updating subject icons and colors...\n")
    update_subjects()
    print("\nDone!")
