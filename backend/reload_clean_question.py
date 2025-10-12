import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.learning.models import ExamYear, ExamSession, Question, Subject, Choice

# 2025年度 第37回試験を取得
exam_year = ExamYear.objects.get(year=2025)
exam_session = ExamSession.objects.get(year=exam_year, session_number=37)

# 科目を取得
subject = exam_session.subjects.first()
if not subject:
    subject = Subject.objects.first()

print(f"=== HTMLタグなしの問題データに更新 ===")
print(f"試験: {exam_session}")
print(f"科目: {subject.name if subject else 'なし'}")

# 既存の問題を削除
existing_questions = Question.objects.filter(exam_session=exam_session)
if existing_questions.exists():
    print(f"\n既存の問題を削除: {existing_questions.count()}問")
    existing_questions.delete()

# 純粋なテキストの問題データ（HTMLタグなし）
question = Question.objects.create(
    subject=subject,
    exam_session=exam_session,
    question_type='past_exam',
    year=2025,
    question_number=1,
    question_text="次の記述のうち、介護福祉職がアドボカシー（advocacy）の視点から行う対応として、最も適切なものを1つ選びなさい。",
    explanation="アドボカシーとは、利用者の権利を擁護し、代弁することです。選択肢1が正解で、利用者の最善の利益を代弁する役割を果たします。",
    translations={
        "indonesian": "Dari deskripsi berikut pilihlah satu tindakan yang paling tepat yang dilakukan oleh pekerja perawatan dari sudut pandang advokasi (advocacy)."
    },
    vocabulary={
        "次": {"reading": "つぎ", "translation": "berikut"},
        "記述": {"reading": "きじゅつ", "translation": "deskripsi"},
        "介護福祉職": {"reading": "かいごふくししょく", "translation": "pekerja perawatan"},
        "アドボカシー": {"reading": "アドボカシー", "translation": "advokasi"},
        "視点": {"reading": "してん", "translation": "sudut pandang"},
        "行う": {"reading": "おこなう", "translation": "melakukan"},
        "対応": {"reading": "たいおう", "translation": "tindakan"},
        "最も": {"reading": "もっとも", "translation": "paling"},
        "適切": {"reading": "てきせつ", "translation": "tepat"},
        "選ぶ": {"reading": "えらぶ", "translation": "memilih"}
    }
)

print(f"\n[作成] 問題{question.question_number}")
print(f"  問題文（プレーンテキスト）: {question.question_text}")

# 純粋なテキストの選択肢データ（HTMLタグなし）
choices_data = [
    {
        "choice_number": 1,
        "choice_text": "利用者の最善の利益を代弁する。",
        "is_correct": True
    },
    {
        "choice_number": 2,
        "choice_text": "家族が希望する介護サービスを提供する。",
        "is_correct": False
    },
    {
        "choice_number": 3,
        "choice_text": "施設の規則に従って介護を提供する。",
        "is_correct": False
    },
    {
        "choice_number": 4,
        "choice_text": "利用者個人の趣味を生かして、レクリエーション活動を行う。",
        "is_correct": False
    },
    {
        "choice_number": 5,
        "choice_text": "視覚障害者が必要とする情報を、利用しやすいようにする。",
        "is_correct": False
    }
]

for choice_data in choices_data:
    choice = Choice.objects.create(question=question, **choice_data)
    status = "[正解]" if choice.is_correct else "[選択肢]"
    print(f"{status} {choice.choice_number}. {choice.choice_text}")

# 選択肢でも使われる単語を追加
question.vocabulary.update({
    "利用者": {"reading": "りようしゃ", "translation": "pengguna"},
    "最善": {"reading": "さいぜん", "translation": "terbaik"},
    "利益": {"reading": "りえき", "translation": "kepentingan"},
    "代弁": {"reading": "だいべん", "translation": "mewakili"},
    "家族": {"reading": "かぞく", "translation": "keluarga"},
    "希望": {"reading": "きぼう", "translation": "keinginan"},
    "介護": {"reading": "かいご", "translation": "perawatan"},
    "サービス": {"reading": "サービス", "translation": "layanan"},
    "提供": {"reading": "ていきょう", "translation": "menyediakan"},
    "施設": {"reading": "しせつ", "translation": "fasilitas"},
    "規則": {"reading": "きそく", "translation": "aturan"},
    "従う": {"reading": "したがう", "translation": "mengikuti"},
    "個人": {"reading": "こじん", "translation": "individu"},
    "趣味": {"reading": "しゅみ", "translation": "hobi"},
    "生かす": {"reading": "いかす", "translation": "memanfaatkan"},
    "レクリエーション": {"reading": "レクリエーション", "translation": "rekreasi"},
    "活動": {"reading": "かつどう", "translation": "kegiatan"},
    "視覚障害者": {"reading": "しかくしょうがいしゃ", "translation": "penyandang disabilitas netra"},
    "必要": {"reading": "ひつよう", "translation": "membutuhkan"},
    "情報": {"reading": "じょうほう", "translation": "informasi"},
    "利用": {"reading": "りよう", "translation": "menggunakan"}
})
question.save()

print("\n=== 完了 ===")
print(f"登録された問題数: {Question.objects.filter(exam_session=exam_session).count()}問")
print(f"登録された選択肢数: {Choice.objects.filter(question__exam_session=exam_session).count()}個")
print(f"語彙数: {len(question.vocabulary)}個")
print("\n✓ 問題文と選択肢はプレーンテキスト")
print("✓ 表示時にvocabularyから自動的にHTMLタグを付与")
