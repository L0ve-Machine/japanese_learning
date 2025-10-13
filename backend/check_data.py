import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.learning.models import Subject, SubjectGroup

print("=== SubjectGroups ===")
groups = SubjectGroup.objects.all()
for g in groups:
    print(f"ID {g.id}: {g.name} (group_key: {g.group_key})")
    print(f"  関連科目: {g.subjects.count()}件")
    for s in g.subjects.all():
        print(f"    - {s.name}")
    print()

print("\n=== SubjectGroupに関連付けられていない科目 ===")
orphan_subjects = Subject.objects.filter(group__isnull=True)
for s in orphan_subjects:
    print(f"ID {s.id}: {s.name}")
