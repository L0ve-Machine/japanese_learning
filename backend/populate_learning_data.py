#!/usr/bin/env python
"""
Populate learning data from CSV files
"""
import os
import csv
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.learning.models import ExamYear, ExamSession, SubjectGroup, Subject

def populate_data():
    """Populate all learning data"""
    print("📚 Populating learning data...")

    # Create subject groups
    print("\n📁 Creating subject groups...")
    groups_data = [
        ('A', 'Aグループ', '人間と社会領域', 1),
        ('B', 'Bグループ', 'こころとからだのしくみ領域', 2),
        ('C', 'Cグループ', '介護過程・総合問題', 3)
    ]

    for group_key, name, description, order in groups_data:
        group, created = SubjectGroup.objects.get_or_create(
            group_key=group_key,
            defaults={
                'name': name,
                'description': description,
                'order': order
            }
        )
        if created:
            print(f"  ✅ Created group: {name}")
        else:
            print(f"  ⚠️  Group already exists: {name}")

    # Create exam years
    print("\n📅 Creating exam years...")
    years_data = [
        (2025, '2025年度介護福祉士国家試験'),
        (2024, '2024年度介護福祉士国家試験'),
        (2023, '2023年度介護福祉士国家試験')
    ]

    for year, description in years_data:
        exam_year, created = ExamYear.objects.get_or_create(
            year=year,
            defaults={'description': description}
        )
        if created:
            print(f"  ✅ Created year: {year}")
        else:
            print(f"  ⚠️  Year already exists: {year}")

    # Create exam sessions
    print("\n📋 Creating exam sessions...")
    sessions_data = [
        (2025, 37, '2025年度第37回介護福祉士国家試験'),
        (2024, 36, '2024年度第36回介護福祉士国家試験'),
        (2023, 35, '2023年度第35回介護福祉士国家試験')
    ]

    for year, session_number, name in sessions_data:
        try:
            exam_year = ExamYear.objects.get(year=year)
            session, created = ExamSession.objects.get_or_create(
                year=exam_year,
                session_number=session_number,
                defaults={'name': name}
            )
            if created:
                print(f"  ✅ Created session: {name}")
            else:
                print(f"  ⚠️  Session already exists: {name}")
        except ExamYear.DoesNotExist:
            print(f"  ❌ Year {year} not found for session {session_number}")

    # Create subjects
    print("\n📖 Creating subjects...")
    subjects_data = [
        ('human_dignity_independence', 'A', '人間の尊厳と自立', 'Martabat dan Kemandirian Manusia', 1),
        ('care_basics', 'A', '介護の基本', 'Dasar-dasar Perawatan', 2),
        ('social_understanding', 'A', '社会の理解', 'Pemahaman Sosial', 3),
        ('human_relations_communication', 'A', '人間関係とコミュニケーション', 'Hubungan Manusia dan Komunikasi', 4),
        ('communication_technology', 'A', 'コミュニケーション技術', 'Teknologi Komunikasi', 5),
        ('life_support_technology', 'A', '生活支援技術', 'Teknologi Dukungan Kehidupan', 6),
        ('mind_body_mechanism', 'B', 'こころとからだのしくみ', 'Mekanisme Pikiran dan Tubuh', 7),
        ('development_aging', 'B', '発達と老化の理解', 'Pemahaman Perkembangan dan Penuaan', 8),
        ('dementia_understanding', 'B', '認知症の理解', 'Pemahaman Demensia', 9),
        ('disability_understanding', 'B', '障害の理解', 'Pemahaman Disabilitas', 10),
        ('medical_care', 'B', '医療的ケア', 'Perawatan Medis', 11),
        ('care_process', 'C', '介護過程', 'Proses Perawatan', 12),
        ('comprehensive_problems', 'C', '総合問題', 'Masalah Komprehensif', 13)
    ]

    for subject_key, group_key, name, indonesian_name, order in subjects_data:
        try:
            group = SubjectGroup.objects.get(group_key=group_key)
            subject, created = Subject.objects.get_or_create(
                subject_key=subject_key,
                defaults={
                    'group': group,
                    'name': name,
                    'indonesian_name': indonesian_name,
                    'order': order
                }
            )
            if created:
                print(f"  ✅ Created subject: {name}")
            else:
                print(f"  ⚠️  Subject already exists: {name}")
        except SubjectGroup.DoesNotExist:
            print(f"  ❌ Group {group_key} not found for subject {subject_key}")

    print("\n✅ Learning data population completed!")

    # Show summary
    print(f"\n📊 Summary:")
    print(f"  Subject Groups: {SubjectGroup.objects.count()}")
    print(f"  Exam Years: {ExamYear.objects.count()}")
    print(f"  Exam Sessions: {ExamSession.objects.count()}")
    print(f"  Subjects: {Subject.objects.count()}")

if __name__ == '__main__':
    populate_data()