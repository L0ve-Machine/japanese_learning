import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.learning.models import ExamYear, ExamSession

# 2025年度を作成
exam_year, created = ExamYear.objects.get_or_create(
    year=2025,
    defaults={
        'description': '令和7年度（第37回）介護福祉士国家試験',
        'is_active': True
    }
)

if created:
    print(f"[作成] ExamYear: {exam_year.year}年度")
else:
    print(f"[既存] ExamYear: {exam_year.year}年度")

# 第37回試験セッションを作成
exam_session, created = ExamSession.objects.get_or_create(
    year=exam_year,
    session_number=37,
    defaults={
        'name': '第37回介護福祉士国家試験',
        'is_active': True
    }
)

if created:
    print(f"[作成] ExamSession: {exam_session}")
else:
    print(f"[既存] ExamSession: {exam_session}")

print("\n=== 完了 ===")
print(f"URL: /quiz/{exam_year.year}/{exam_session.session_number}/")
