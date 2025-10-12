import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.learning.models import Subject, SubjectGroup

# A、B、Cグループを作成
group_a, _ = SubjectGroup.objects.get_or_create(
    group_key='A',
    defaults={
        'name': 'Aグループ',
        'description': '人間と社会の領域',
        'order': 1
    }
)

group_b, _ = SubjectGroup.objects.get_or_create(
    group_key='B',
    defaults={
        'name': 'Bグループ',
        'description': 'こころとからだのしくみ',
        'order': 2
    }
)

group_c, _ = SubjectGroup.objects.get_or_create(
    group_key='C',
    defaults={
        'name': 'Cグループ',
        'description': '医療的ケアと総合問題',
        'order': 3
    }
)

print("=== グループ作成完了 ===")
print(f"A: {group_a.name}")
print(f"B: {group_b.name}")
print(f"C: {group_c.name}")

# 各科目をグループに関連付け
group_a_subjects = [
    "人間の尊厳と自立",
    "介護の基本",
    "社会の理解",
    "人間関係とコミュニケーション",
    "コミュニケーション技術",
    "生活支援技術"
]

group_b_subjects = [
    "こころとからだのしくみ",
    "発達と老化の理解",
    "認知症の理解",
    "障害の理解",
    "医療的ケア（基礎）"
]

group_c_subjects = [
    "介護過程",
    "喀痰吸引",
    "経管栄養"
]

print("\n=== 科目をグループに関連付け中 ===")

# Aグループ
for name in group_a_subjects:
    subject = Subject.objects.filter(name=name).first()
    if subject:
        subject.group = group_a
        subject.save()
        print(f"[A] {name}")

# Bグループ
for name in group_b_subjects:
    subject = Subject.objects.filter(name=name).first()
    if subject:
        subject.group = group_b
        subject.save()
        print(f"[B] {name}")

# Cグループ
for name in group_c_subjects:
    subject = Subject.objects.filter(name=name).first()
    if subject:
        subject.group = group_c
        subject.save()
        print(f"[C] {name}")

print("\n=== 完了後の状態 ===")
for group in SubjectGroup.objects.all().order_by('order'):
    print(f"\n{group.name} ({group.subjects.count()}件):")
    for s in group.subjects.all():
        print(f"  - {s.name}")
