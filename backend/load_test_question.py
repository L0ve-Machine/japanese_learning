import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.learning.models import ExamYear, ExamSession, Question, Subject, Choice

# 2025年度 第37回試験を取得
exam_year = ExamYear.objects.get(year=2025)
exam_session = ExamSession.objects.get(year=exam_year, session_number=37)

# 科目を取得（なければ最初の科目）
subject = exam_session.subjects.first()
if not subject:
    subject = Subject.objects.first()

print(f"=== 問題データをDBに登録 ===")
print(f"試験: {exam_session}")
print(f"科目: {subject.name if subject else 'なし'}")

# 既存の問題を確認
existing_questions = Question.objects.filter(exam_session=exam_session)
if existing_questions.exists():
    print(f"\n既存の問題を削除: {existing_questions.count()}問")
    existing_questions.delete()

# テスト用問題データ（問題1）
question = Question.objects.create(
    subject=subject,
    exam_session=exam_session,
    question_type='past_exam',
    year=2025,
    question_number=1,
    question_text="<span class='vocab-word' data-translation='berikut' data-reading='つぎ'>次</span>の<span class='vocab-word' data-translation='deskripsi' data-reading='きじゅつ'>記述</span>のうち、<span class='vocab-word' data-translation='pekerja perawatan' data-reading='かいごふくししょく'>介護福祉職</span>が<span class='vocab-word' data-translation='advocacy|advokasi' data-reading='アド・ボ・カ・シー'>アドボカシー</span>（advocacy）の<span class='vocab-word' data-translation='sudut pandang' data-reading='してん'>視点</span>から<span class='vocab-word' data-translation='melakukan' data-reading='おこな'>行う</span><span class='vocab-word' data-translation='tindakan' data-reading='たいおう'>対応</span>として、<span class='vocab-word' data-translation='paling' data-reading='もっとも'>最も</span><span class='vocab-word' data-translation='tepat' data-reading='てきせつ'>適切</span>なものを1つ<span class='vocab-word' data-translation='memilih' data-reading='えら'>選</span>びなさい。",
    explanation="アドボカシーとは、利用者の権利を擁護し、代弁することです。選択肢1が正解で、利用者の最善の利益を代弁する役割を果たします。",
    translations={
        "indonesian": "Dari deskripsi berikut pilihlah satu tindakan yang paling tepat yang dilakukan oleh pekerja perawatan dari sudut pandang advokasi (advocacy)."
    },
    vocabulary={
        "次": {"reading": "つぎ", "translation": "berikut"},
        "記述": {"reading": "きじゅつ", "translation": "deskripsi"},
        "介護福祉職": {"reading": "かいごふくししょく", "translation": "pekerja perawatan"},
        "視点": {"reading": "してん", "translation": "sudut pandang"},
        "行": {"reading": "おこな", "translation": "melakukan"},
        "対応": {"reading": "たいおう", "translation": "tindakan"},
        "最も": {"reading": "もっとも", "translation": "paling"},
        "適切": {"reading": "てきせつ", "translation": "tepat"},
        "選": {"reading": "えら", "translation": "memilih"},
        "歳": {"reading": "さい", "translation": "tahun"},
        "女性": {"reading": "じょせい", "translation": "wanita"},
        "要介護": {"reading": "ようかいご", "translation": "membutuhkan perawatan"},
        "脳梗塞": {"reading": "のうこうそく", "translation": "infark serebral"},
        "後遺症": {"reading": "こういしょう", "translation": "gejala sisa"},
        "左片麻痺": {"reading": "ひだりかたまひ", "translation": "hemiplegia kiri"},
        "介護老人福祉施設": {"reading": "かいごろうじんふくししせつ", "translation": "panti jompo"},
        "生活": {"reading": "せいかつ", "translation": "tinggal"},
        "アドボカシー": {"reading": "アドボカシー", "translation": "advocacy|advokasi"}
    }
)

print(f"\n[作成] 問題{question.question_number}: {question.question_text[:50]}...")

# 選択肢データ
choices_data = [
    {
        "choice_number": 1,
        "choice_text": "<span class='vocab-word' data-translation='user|pengguna' data-reading='り・よう・しゃ'>利用者</span>の<span class='vocab-word' data-translation='best interests|kepentingan terbaik' data-reading='さい・ぜん・の・り・えき'>最善の利益</span>を<span class='vocab-word' data-translation='represent|mewakili' data-reading='だい・べん'>代弁</span>する。",
        "is_correct": True
    },
    {
        "choice_number": 2,
        "choice_text": "<span class='vocab-word' data-translation='family|keluarga' data-reading='か・ぞく'>家族</span>が<span class='vocab-word' data-translation='desire|keinginan' data-reading='き・ぼう'>希望</span>する<span class='vocab-word' data-translation='care|perawatan' data-reading='かい・ご'>介護</span>サービスを<span class='vocab-word' data-translation='provide|menyediakan' data-reading='てい・きょう'>提供</span>する。",
        "is_correct": False
    },
    {
        "choice_number": 3,
        "choice_text": "<span class='vocab-word' data-translation='institution|institusi' data-reading='し・せつ'>施設</span>の<span class='vocab-word' data-translation='rules|aturan' data-reading='き・そく'>規則</span>に<span class='vocab-word' data-translation='according to|sesuai dengan' data-reading='した・が'>従って</span><span class='vocab-word' data-translation='care|perawatan' data-reading='かい・ご'>介護</span>を<span class='vocab-word' data-translation='provide|menyediakan' data-reading='てい・きょう'>提供</span>する。",
        "is_correct": False
    },
    {
        "choice_number": 4,
        "choice_text": "<span class='vocab-word' data-translation='individual user|pengguna individu' data-reading='り・よう・しゃ・こ・じん'>利用者個人</span>の<span class='vocab-word' data-translation='hobby|hobi' data-reading='しゅ・み'>趣味</span>を<span class='vocab-word' data-translation='utilize|memanfaatkan' data-reading='い'>生かして</span>、<span class='vocab-word' data-translation='recreation activities|kegiatan rekreasi' data-reading='レク・リ・エー・ション・かつ・どう'>レクリエーション活動</span>を<span class='vocab-word' data-translation='conduct|melakukan' data-reading='おこな'>行う</span>。",
        "is_correct": False
    },
    {
        "choice_number": 5,
        "choice_text": "<span class='vocab-word' data-translation='visually impaired|penyandang disabilitas netra' data-reading='し・かく・しょう・がい・しゃ'>視覚障害者</span>が<span class='vocab-word' data-translation='need|membutuhkan' data-reading='ひつ・よう'>必要</span>とする<span class='vocab-word' data-translation='information|informasi' data-reading='じょう・ほう'>情報</span>を、<span class='vocab-word' data-translation='easy to use|mudah digunakan' data-reading='り・よう'>利用</span>しやすいようにする。",
        "is_correct": False
    }
]

for choice_data in choices_data:
    choice = Choice.objects.create(question=question, **choice_data)
    status = "[正解]" if choice.is_correct else "[選択肢]"
    print(f"{status} {choice.choice_number}. {choice.choice_text[:40]}...")

print("\n=== 完了 ===")
print(f"登録された問題数: {Question.objects.filter(exam_session=exam_session).count()}問")
print(f"登録された選択肢数: {Choice.objects.filter(question__exam_session=exam_session).count()}個")
