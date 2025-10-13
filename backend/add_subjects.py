import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.learning.models import Subject, SubjectGroup

# ABCグループの科目リスト
subjects_data = [
    # Aグループ
    "人間の尊厳と自立",
    "介護の基本",
    "社会の理解",
    "人間関係とコミュニケーション",
    "コミュニケーション技術",
    "生活支援技術",
    # Bグループ
    "こころとからだのしくみ",
    "発達と老化の理解",
    "認知症の理解",
    "障害の理解",
    "医療的ケア（基礎）",
    # Cグループ
    "介護過程",
    "喀痰吸引",
    "経管栄養",
]

# 既存の科目を確認
print("=== 既存の科目 ===")
existing_subjects = Subject.objects.all()
for subj in existing_subjects:
    print(f"- {subj.name}")

print("\n=== 科目を追加中 ===")
for subject_name in subjects_data:
    subject, created = Subject.objects.get_or_create(name=subject_name)
    if created:
        print(f"[追加] {subject_name}")
    else:
        print(f"[既存] {subject_name}")

print("\n=== 追加後の全科目 ===")
all_subjects = Subject.objects.all().order_by('id')
for subj in all_subjects:
    print(f"ID {subj.id}: {subj.name}")
