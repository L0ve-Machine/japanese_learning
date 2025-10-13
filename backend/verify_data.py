import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.learning.models import ExamYear, ExamSession, Question, Choice

print("=== DB データ確認 ===\n")

# 試験データ確認
exam_year = ExamYear.objects.get(year=2025)
exam_session = ExamSession.objects.get(year=exam_year, session_number=37)

print(f"試験年度: {exam_year.year}年度")
print(f"試験セッション: 第{exam_session.session_number}回")
print(f"URL: /quiz/{exam_year.year}/{exam_session.session_number}/\n")

# 問題確認
questions = Question.objects.filter(exam_session=exam_session)
print(f"登録された問題数: {questions.count()}問\n")

for q in questions:
    print(f"問題{q.question_number}:")
    print(f"  科目: {q.subject.name if q.subject else 'なし'}")
    print(f"  問題文: {q.question_text[:60]}...")
    print(f"  説明: {q.explanation[:60]}...")
    print(f"  翻訳: {q.translations.get('indonesian', '')[:60] if q.translations else 'なし'}...")
    print(f"  語彙数: {len(q.vocabulary) if q.vocabulary else 0}個")

    # 選択肢確認
    choices = Choice.objects.filter(question=q)
    print(f"  選択肢数: {choices.count()}個")
    for c in choices:
        status = "[正解]" if c.is_correct else "      "
        print(f"    {status} {c.choice_number}. {c.choice_text[:50]}...")
    print()

print("\n=== 動的データ取得の流れ ===")
print("1. ユーザーが /quiz/2025/37/ にアクセス")
print("2. views.pyがDBから ExamSession(2025, 37) を取得")
print("3. その ExamSession に関連する Question を全て取得")
print("4. 各 Question の選択肢 (Choice) も取得")
print("5. テンプレートに渡して表示")
print("\n✓ 全て動的にDBから取得されます")
