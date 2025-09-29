#!/usr/bin/env python
"""
Create sample exam data for the Japanese care worker learning application
"""
import os
import sys
import django
from django.conf import settings

# Setup Django environment
sys.path.append('/mnt/c/Users/genki/Projects/web/japanese_learning/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.learning.models import SubjectGroup, Subject, ExamYear, ExamSession

def create_exam_data():
    """Create sample exam data for care worker exam preparation"""

    print("🗂️ Creating Subject Groups...")

    # Create Subject Groups for care worker exam
    subject_groups_data = [
        {
            'name': '人間と社会',
            'group_key': 'human_society',
            'description': '人間の尊厳と自立、人間関係とコミュニケーション、社会の理解',
            'order': 1
        },
        {
            'name': '介護',
            'group_key': 'care',
            'description': '介護の基本、コミュニケーション技術、生活支援技術、介護過程',
            'order': 2
        },
        {
            'name': 'こころとからだのしくみ',
            'group_key': 'mind_body',
            'description': '発達と老化の理解、認知症の理解、障害の理解、こころとからだのしくみ',
            'order': 3
        },
        {
            'name': '医療的ケア',
            'group_key': 'medical_care',
            'description': '医療的ケアの基礎、喀痰吸引、経管栄養',
            'order': 4
        }
    ]

    for group_data in subject_groups_data:
        group, created = SubjectGroup.objects.get_or_create(
            group_key=group_data['group_key'],
            defaults=group_data
        )
        if created:
            print(f"✅ Subject Group created: {group.name}")
        else:
            print(f"✅ Subject Group already exists: {group.name}")

    print("\n📚 Creating Subjects...")

    # Create Subjects
    subjects_data = [
        # Human and Society Group
        {
            'subject_key': 'human_dignity',
            'group_key': 'human_society',
            'name': '人間の尊厳と自立',
            'indonesian_name': 'Martabat dan Kemandirian Manusia',
            'description': '人間の尊厳の保持と自立生活支援の理念について学習',
            'order': 1
        },
        {
            'subject_key': 'human_relations',
            'group_key': 'human_society',
            'name': '人間関係とコミュニケーション',
            'indonesian_name': 'Hubungan Manusia dan Komunikasi',
            'description': 'コミュニケーションの基本と人間関係の形成について学習',
            'order': 2
        },
        {
            'subject_key': 'society_understanding',
            'group_key': 'human_society',
            'name': '社会の理解',
            'indonesian_name': 'Pemahaman Masyarakat',
            'description': '社会保障制度、介護保険制度等の理解',
            'order': 3
        },

        # Care Group
        {
            'subject_key': 'care_basics',
            'group_key': 'care',
            'name': '介護の基本',
            'indonesian_name': 'Dasar-dasar Perawatan',
            'description': '介護福祉士の役割と職業倫理について学習',
            'order': 1
        },
        {
            'subject_key': 'communication_tech',
            'group_key': 'care',
            'name': 'コミュニケーション技術',
            'indonesian_name': 'Teknik Komunikasi',
            'description': '介護におけるコミュニケーション技術の習得',
            'order': 2
        },
        {
            'subject_key': 'life_support_tech',
            'group_key': 'care',
            'name': '生活支援技術',
            'indonesian_name': 'Teknik Dukungan Kehidupan',
            'description': '日常生活における支援技術の習得',
            'order': 3
        },
        {
            'subject_key': 'care_process',
            'group_key': 'care',
            'name': '介護過程',
            'indonesian_name': 'Proses Perawatan',
            'description': '介護過程の展開方法について学習',
            'order': 4
        },

        # Mind and Body Group
        {
            'subject_key': 'development_aging',
            'group_key': 'mind_body',
            'name': '発達と老化の理解',
            'indonesian_name': 'Pemahaman Perkembangan dan Penuaan',
            'description': '人間の成長・発達と老化について学習',
            'order': 1
        },
        {
            'subject_key': 'dementia_understanding',
            'group_key': 'mind_body',
            'name': '認知症の理解',
            'indonesian_name': 'Pemahaman Demensia',
            'description': '認知症の症状、支援方法について学習',
            'order': 2
        },
        {
            'subject_key': 'disability_understanding',
            'group_key': 'mind_body',
            'name': '障害の理解',
            'indonesian_name': 'Pemahaman Disabilitas',
            'description': '障害の特性と支援方法について学習',
            'order': 3
        },
        {
            'subject_key': 'mind_body_mechanism',
            'group_key': 'mind_body',
            'name': 'こころとからだのしくみ',
            'indonesian_name': 'Mekanisme Jiwa dan Tubuh',
            'description': '身体機能と心理的側面について学習',
            'order': 4
        },

        # Medical Care Group
        {
            'subject_key': 'medical_care_basics',
            'group_key': 'medical_care',
            'name': '医療的ケア（基礎）',
            'indonesian_name': 'Perawatan Medis (Dasar)',
            'description': '医療的ケアの基礎知識について学習',
            'order': 1
        },
        {
            'subject_key': 'sputum_suction',
            'group_key': 'medical_care',
            'name': '喀痰吸引',
            'indonesian_name': 'Penyedotan Dahak',
            'description': '喀痰吸引の技術と注意点について学習',
            'order': 2
        },
        {
            'subject_key': 'tube_feeding',
            'group_key': 'medical_care',
            'name': '経管栄養',
            'indonesian_name': 'Nutrisi Enteral',
            'description': '経管栄養の技術と注意点について学習',
            'order': 3
        }
    ]

    for subject_data in subjects_data:
        # Get the subject group
        try:
            group = SubjectGroup.objects.get(group_key=subject_data['group_key'])
            subject_data['group'] = group
            del subject_data['group_key']  # Remove group_key from data

            subject, created = Subject.objects.get_or_create(
                subject_key=subject_data['subject_key'],
                defaults=subject_data
            )
            if created:
                print(f"✅ Subject created: {subject.name}")
            else:
                print(f"✅ Subject already exists: {subject.name}")
        except SubjectGroup.DoesNotExist:
            print(f"❌ Subject Group not found for key: {subject_data['group_key']}")

    print("\n📅 Creating Exam Years...")

    # Create Exam Years
    exam_years = [2025, 2024, 2023]
    for year in exam_years:
        exam_year, created = ExamYear.objects.get_or_create(
            year=year,
            defaults={
                'description': f'{year}年度介護福祉士国家試験',
                'is_active': True
            }
        )
        if created:
            print(f"✅ Exam Year created: {exam_year}")
        else:
            print(f"✅ Exam Year already exists: {exam_year}")

    print("\n📋 Creating Exam Sessions...")

    # Create Exam Sessions for each year
    for year in exam_years:
        try:
            exam_year = ExamYear.objects.get(year=year)

            # Create main exam session
            session, created = ExamSession.objects.get_or_create(
                year=exam_year,
                session_number=1,
                defaults={
                    'name': f'{year}年度第1回介護福祉士国家試験',
                    'is_active': True
                }
            )

            if created:
                # Add all subjects to this session
                all_subjects = Subject.objects.all()
                session.subjects.set(all_subjects)
                print(f"✅ Exam Session created: {session}")
            else:
                print(f"✅ Exam Session already exists: {session}")

        except ExamYear.DoesNotExist:
            print(f"❌ Exam Year not found: {year}")

    print("\n📊 Summary:")
    print("=" * 50)
    print(f"📂 Subject Groups: {SubjectGroup.objects.count()}")
    print(f"📚 Subjects: {Subject.objects.count()}")
    print(f"📅 Exam Years: {ExamYear.objects.count()}")
    print(f"📋 Exam Sessions: {ExamSession.objects.count()}")

    print("\n🎯 Data structure completed!")
    print("You can now manage this data via Django Admin at: http://localhost:8000/admin/")
    print("Navigate to Learning section to see:")
    print("  - Subject Groups")
    print("  - Subjects")
    print("  - Exam Years")
    print("  - Exam Sessions")

if __name__ == '__main__':
    create_exam_data()