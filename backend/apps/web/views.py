from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms
from .decorators import allow_free_access

User = get_user_model()

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'example@email.com'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'パスワード'})
    )

class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'example@email.com'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': '8文字以上で設定'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'パスワードを再入力'})
    )

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("パスワードが一致しません")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class LandingPageView(TemplateView):
    template_name = 'landing.html'

def landing_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'ようこそ、{username}さん！')
                return redirect('dashboard')
            else:
                messages.error(request, 'メールアドレスまたはパスワードが正しくありません。')
        else:
            messages.error(request, 'メールアドレスまたはパスワードが正しくありません。')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'アカウントが作成されました！')
            return redirect('dashboard')
        else:
            messages.error(request, '登録に失敗しました。入力内容を確認してください。')
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'ログアウトしました。')
    return redirect('landing')

@login_required
@allow_free_access
def dashboard_view(request):
    """ダッシュボードは無料ユーザーもアクセス可能"""
    # ユーザーのサブスクリプション状態を取得
    from apps.subscriptions.models import Subscription
    active_subscription = Subscription.get_user_active_subscription(request.user)

    return render(request, 'dashboard.html', {
        'user': request.user,
        'has_subscription': active_subscription is not None,
        'subscription': active_subscription
    })

@login_required
@allow_free_access
def past_exams_view(request):
    """過去問題一覧ページ"""
    from apps.learning.models import ExamYear, ExamSession, SubjectGroup

    # 年度別に試験セッションを取得
    exam_years = ExamYear.objects.filter(is_active=True).prefetch_related('sessions')

    # 科目グループと科目を取得
    subject_groups = SubjectGroup.objects.filter(is_active=True).prefetch_related('subjects')

    return render(request, 'past_exams.html', {
        'exam_years': exam_years,
        'subject_groups': subject_groups,
        'user': request.user
    })

@login_required
@allow_free_access
def past_exam_detail_view(request, year, session_number):
    """特定年度・回の過去問題詳細ページ"""
    from apps.learning.models import ExamYear, ExamSession, SubjectGroup
    from django.shortcuts import get_object_or_404

    exam_year = get_object_or_404(ExamYear, year=year, is_active=True)
    exam_session = get_object_or_404(ExamSession, year=exam_year, session_number=session_number, is_active=True)

    # 科目グループ別に科目を整理
    subject_groups = SubjectGroup.objects.filter(
        is_active=True,
        subjects__exam_sessions=exam_session
    ).prefetch_related('subjects').distinct()

    return render(request, 'past_exam_detail.html', {
        'exam_year': exam_year,
        'exam_session': exam_session,
        'subject_groups': subject_groups,
        'user': request.user
    })

@login_required
@allow_free_access
def quiz_view(request, year, session_number):
    """クイズページ"""
    from apps.learning.models import ExamYear, ExamSession, Question, Subject, Choice
    from django.shortcuts import get_object_or_404, redirect

    exam_year = get_object_or_404(ExamYear, year=year, is_active=True)

    # セッション番号1の場合は適切なセッション番号にリダイレクト
    if session_number == 1:
        # 2025年度は37回、その他は利用可能なセッションを探す
        if year == 2025:
            return redirect('quiz', year=2025, session_number=37)
        else:
            # その他の年度の場合は最初の利用可能なセッションを探す
            available_session = ExamSession.objects.filter(year=exam_year, is_active=True).first()
            if available_session:
                return redirect('quiz', year=year, session_number=available_session.session_number)

    exam_session = get_object_or_404(ExamSession, year=exam_year, session_number=session_number, is_active=True)

    # Get question number from URL parameter, default to 1
    question_number = int(request.GET.get('q', 1))

    # Get questions for this exam session
    questions = Question.objects.filter(
        exam_session=exam_session
    ).prefetch_related('choices').order_by('question_number')

    if questions.exists():
        # Delete existing questions for this session to update with new data
        questions.delete()

    # Get first subject for this session
    subject = exam_session.subjects.first()
    if not subject:
        subject = Subject.objects.first()

    # Create sample question based on your provided data (q_37_2025_1)
    question = Question.objects.create(
        subject=subject,
        exam_session=exam_session,
        question_type='past_exam',
        year=year,
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

    # Create choices based on your provided data
    choices_data = [
        {"choice_number": 1, "choice_text": "<span class='vocab-word' data-translation='user|pengguna' data-reading='り・よう・しゃ'>利用者</span>の<span class='vocab-word' data-translation='best interests|kepentingan terbaik' data-reading='さい・ぜん・の・り・えき'>最善の利益</span>を<span class='vocab-word' data-translation='represent|mewakili' data-reading='だい・べん'>代弁</span>する。", "is_correct": True},
        {"choice_number": 2, "choice_text": "<span class='vocab-word' data-translation='family|keluarga' data-reading='か・ぞく'>家族</span>が<span class='vocab-word' data-translation='desire|keinginan' data-reading='き・ぼう'>希望</span>する<span class='vocab-word' data-translation='care|perawatan' data-reading='かい・ご'>介護</span>サービスを<span class='vocab-word' data-translation='provide|menyediakan' data-reading='てい・きょう'>提供</span>する。", "is_correct": False},
        {"choice_number": 3, "choice_text": "<span class='vocab-word' data-translation='institution|institusi' data-reading='し・せつ'>施設</span>の<span class='vocab-word' data-translation='rules|aturan' data-reading='き・そく'>規則</span>に<span class='vocab-word' data-translation='according to|sesuai dengan' data-reading='した・が'>従って</span><span class='vocab-word' data-translation='care|perawatan' data-reading='かい・ご'>介護</span>を<span class='vocab-word' data-translation='provide|menyediakan' data-reading='てい・きょう'>提供</span>する。", "is_correct": False},
        {"choice_number": 4, "choice_text": "<span class='vocab-word' data-translation='individual user|pengguna individu' data-reading='り・よう・しゃ・こ・じん'>利用者個人</span>の<span class='vocab-word' data-translation='hobby|hobi' data-reading='しゅ・み'>趣味</span>を<span class='vocab-word' data-translation='utilize|memanfaatkan' data-reading='い'>生かして</span>、<span class='vocab-word' data-translation='recreation activities|kegiatan rekreasi' data-reading='レク・リ・エー・ション・かつ・どう'>レクリエーション活動</span>を<span class='vocab-word' data-translation='conduct|melakukan' data-reading='おこな'>行う</span>。", "is_correct": False},
        {"choice_number": 5, "choice_text": "<span class='vocab-word' data-translation='visually impaired|penyandang disabilitas netra' data-reading='し・かく・しょう・がい・しゃ'>視覚障害者</span>が<span class='vocab-word' data-translation='need|membutuhkan' data-reading='ひつ・よう'>必要</span>とする<span class='vocab-word' data-translation='information|informasi' data-reading='じょう・ほう'>情報</span>を、<span class='vocab-word' data-translation='easy to use|mudah digunakan' data-reading='り・よう'>利用</span>しやすいようにする。", "is_correct": False}
    ]

    for choice_data in choices_data:
        Choice.objects.create(
            question=question,
            **choice_data
        )

    questions = Question.objects.filter(exam_session=exam_session).prefetch_related('choices').order_by('question_number')

    try:
        current_question = questions[question_number - 1]
    except IndexError:
        current_question = questions.first()
        question_number = 1

    # Calculate progress
    total_questions = questions.count()
    progress_percentage = (question_number / total_questions) * 100

    return render(request, 'quiz.html', {
        'exam_year': exam_year,
        'exam_session': exam_session,
        'current_question': current_question,
        'question_number': question_number,
        'total_questions': total_questions,
        'progress_percentage': progress_percentage,
        'user': request.user
    })

def redirect_to_correct_session(request):
    """古いセッション番号を正しいセッション番号にリダイレクト"""
    from django.shortcuts import redirect
    return redirect('quiz', year=2025, session_number=37)