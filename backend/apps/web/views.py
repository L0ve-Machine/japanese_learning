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

@login_required
@allow_free_access
def kotoba_view(request):
    """ことば（語彙学習）メインページ"""
    from apps.learning.models import KotobaCategory
    from django.core.cache import cache
    from django.db.models import Count

    # Try to get from cache
    cache_key = 'kotoba_categories_all'
    categories = cache.get(cache_key)

    if not categories:
        # Load from database with word counts
        categories = list(KotobaCategory.objects.all().annotate(
            word_count=Count('words')
        ).values(
            'category_key', 'japanese_name', 'indonesian_translation', 'ruby_reading', 'order_number', 'word_count'
        ))
        # Transform to match template expectations
        categories = [{
            'key': cat['category_key'],
            'japanese': cat['japanese_name'],
            'indonesian': cat['indonesian_translation'],
            'ruby': cat['ruby_reading'],
            'order': cat['order_number'],
            'word_count': cat['word_count']
        } for cat in categories]
        # Cache for 1 hour
        cache.set(cache_key, categories, timeout=3600)

    return render(request, 'kotoba/main.html', {
        'categories': categories,
        'user': request.user
    })

@login_required
@allow_free_access
def kotoba_category_view(request, category_key):
    """ことば カテゴリー詳細ページ（サブカテゴリー一覧）"""
    from apps.learning.models import KotobaCategory, KotobaSubcategory, KotobaWord
    from django.http import Http404
    from django.core.cache import cache
    from django.db.models import Count

    # Get category with caching
    try:
        category = KotobaCategory.get_cached(category_key)
    except KotobaCategory.DoesNotExist:
        raise Http404("Category not found")

    # Try to get subcategories from cache
    cache_key = f'kotoba_subcategories_{category_key}'
    subcategories = cache.get(cache_key)

    if not subcategories:
        # Load from database with word counts
        subcategories = list(
            KotobaSubcategory.objects.filter(main_category=category)
            .annotate(word_count=Count('words'))
            .values('subcategory_key', 'japanese_name', 'indonesian_translation', 'ruby_reading', 'order_number', 'word_count')
        )
        # Transform to match template expectations
        subcategories = [{
            'key': sub['subcategory_key'],
            'japanese': sub['japanese_name'],
            'indonesian': sub['indonesian_translation'],
            'ruby': sub['ruby_reading'],
            'order': sub['order_number'],
            'word_count': sub['word_count']
        } for sub in subcategories]
        # Cache for 1 hour
        cache.set(cache_key, subcategories, timeout=3600)

    # Transform category to dict for template
    category_dict = {
        'key': category.category_key,
        'japanese': category.japanese_name,
        'indonesian': category.indonesian_translation,
        'ruby': category.ruby_reading
    }

    return render(request, 'kotoba/category.html', {
        'category': category_dict,
        'subcategories': subcategories,
        'user': request.user
    })

@login_required
@allow_free_access
def kotoba_subcategory_view(request, category_key, subcategory_key):
    """ことば サブカテゴリー詳細ページ（単語学習）"""
    from apps.learning.models import KotobaCategory, KotobaSubcategory, KotobaWord
    from django.http import Http404
    from django.core.cache import cache

    # Get category
    try:
        category = KotobaCategory.get_cached(category_key)
    except KotobaCategory.DoesNotExist:
        raise Http404("Category not found")

    # Get subcategory
    try:
        subcategory = KotobaSubcategory.objects.get(
            main_category=category,
            subcategory_key=subcategory_key
        )
    except KotobaSubcategory.DoesNotExist:
        raise Http404("Subcategory not found")

    # Try to get words from cache
    cache_key = f'kotoba_words_{category_key}_{subcategory_key}'
    words = cache.get(cache_key)

    if not words:
        # Load from database with related data
        word_objects = KotobaWord.objects.filter(
            main_category=category,
            subcategory=subcategory
        ).prefetch_related('examples__vocabulary').order_by('japanese_word')

        # Transform to dict for template
        words = []
        for word in word_objects:
            word_dict = {
                'id': word.word_id,
                'japanese': word.japanese_word,
                'ruby': word.ruby_reading,
                'indonesian': word.indonesian_translation,
                'examples': []
            }

            # Add examples
            for example in word.examples.all():
                example_dict = {
                    'id': example.example_id,
                    'japanese': example.japanese_example,
                    'indonesian': example.indonesian_example,
                    'order': example.order_number,
                    'vocabulary': []
                }

                # Add vocabulary
                for vocab in example.vocabulary.all():
                    example_dict['vocabulary'].append({
                        'japanese': vocab.japanese_word,
                        'ruby': vocab.ruby_reading,
                        'indonesian': vocab.indonesian_translation
                    })

                word_dict['examples'].append(example_dict)

            words.append(word_dict)

        # Cache for 1 hour
        cache.set(cache_key, words, timeout=3600)

    # Transform category and subcategory to dict for template
    category_dict = {
        'key': category.category_key,
        'japanese': category.japanese_name,
        'indonesian': category.indonesian_translation,
        'ruby': category.ruby_reading
    }

    subcategory_dict = {
        'key': subcategory.subcategory_key,
        'japanese': subcategory.japanese_name,
        'indonesian': subcategory.indonesian_translation,
        'ruby': subcategory.ruby_reading
    }

    return render(request, 'kotoba/subcategory.html', {
        'category': category_dict,
        'subcategory': subcategory_dict,
        'words': words,
        'user': request.user
    })

@login_required
@allow_free_access
def subject_learning_view(request):
    """科目学習メインページ"""
    import os
    from django.conf import settings

    # 利用可能な科目ファイル一覧を取得
    subjects_dir = os.path.join(settings.BASE_DIR, 'static', 'subjects')
    available_subjects = []

    if os.path.exists(subjects_dir):
        for filename in os.listdir(subjects_dir):
            if filename.endswith('.html'):
                subject_name = filename.replace('.html', '')
                available_subjects.append({
                    'name': subject_name,
                    'filename': filename,
                    'url': f'/static/subjects/{filename}'
                })

    return render(request, 'subjects/subject_learning.html', {
        'available_subjects': available_subjects,
        'user': request.user
    })

@login_required
@allow_free_access
def subject_detail_view(request, subject_name):
    """個別科目詳細ページ"""
    from django.shortcuts import get_object_or_404
    from django.http import Http404

    # セキュリティ: パストラバーサル攻撃を防ぐ
    if '..' in subject_name or '/' in subject_name:
        raise Http404("Invalid subject name")

    # 利用可能な科目リスト
    available_subjects = {
        '介護試験対策': {
            'title': '介護試験対策',
            'description': 'Persiapan Ujian Kaigo',
            'icon': 'medical_services',
            'color': '#4caf50'
        },
        '介護の実務会話': {
            'title': '介護の実務会話',
            'description': 'Percakapan Praktis Kaigo',
            'icon': 'chat',
            'color': '#2196f3'
        },
        '日本人と会話': {
            'title': '日本人と会話',
            'description': 'Percakapan dengan Orang Jepang',
            'icon': 'people',
            'color': '#ff9800'
        },
        '特定技能評価試験': {
            'title': '特定技能評価試験',
            'description': 'Ujian Evaluasi Keterampilan Khusus',
            'icon': 'assignment',
            'color': '#9c27b0'
        },
        '日本の生活マナー': {
            'title': '日本の生活マナー',
            'description': 'Etiket Kehidupan di Jepang',
            'icon': 'home',
            'color': '#795548'
        }
    }

    if subject_name not in available_subjects:
        raise Http404("Subject not found")

    subject = available_subjects[subject_name]

    return render(request, 'subjects/subject_detail.html', {
        'subject_name': subject_name,
        'subject': subject,
        'user': request.user
    })

@login_required
@allow_free_access
def chapter_learning_view(request, subject_name):
    """章学習ページ"""
    from django.http import Http404
    import csv
    import os
    from django.conf import settings

    # セキュリティ: パストラバーサル攻撃を防ぐ
    if '..' in subject_name or '/' in subject_name:
        raise Http404("Invalid subject name")

    # URLパラメータから章情報を取得
    chapter = request.GET.get('chapter', '第1章')
    title = request.GET.get('title', '章学習')
    item_key = request.GET.get('item', '介護保険')  # Get item key from URL

    # 利用可能な科目リスト
    available_subjects = {
        '介護試験対策': {
            'title': '介護試験対策',
            'description': 'Persiapan Ujian Kaigo',
            'icon': 'medical_services',
            'color': '#4caf50'
        },
        '介護の実務会話': {
            'title': '介護の実務会話',
            'description': 'Percakapan Praktis Kaigo',
            'icon': 'chat',
            'color': '#2196f3'
        },
        '日本人と会話': {
            'title': '日本人と会話',
            'description': 'Percakapan dengan Orang Jepang',
            'icon': 'people',
            'color': '#ff9800'
        },
        '特定技能評価試験': {
            'title': '特定技能評価試験',
            'description': 'Ujian Evaluasi Keterampilan Khusus',
            'icon': 'assignment',
            'color': '#9c27b0'
        },
        '日本の生活マナー': {
            'title': '日本の生活マナー',
            'description': 'Etiket Kehidupan di Jepang',
            'icon': 'home',
            'color': '#795548'
        }
    }

    if subject_name not in available_subjects:
        raise Http404("Subject not found")

    subject = available_subjects[subject_name]

    # Load data from CSV files
    data_dir = os.path.join(settings.BASE_DIR, 'data', 'テキスト')

    # Determine chapter_key from chapter (e.g., "第1章" -> "chapter_1")
    chapter_number = chapter.replace('第', '').replace('章', '')
    chapter_key = f'chapter_{chapter_number}'

    # Load text content
    texts = []
    content_file = os.path.join(data_dir, 'テキスト５．コンテンツテキスト.csv')
    if os.path.exists(content_file):
        with open(content_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if (row['subject_key'] == subject_name and
                    row['item_key'] == item_key and
                    row['chapter_key'] == chapter_key):
                    texts.append({
                        'order': int(row['text_order']),
                        'japanese': row['japanese'],
                        'indonesian': row['indonesian']
                    })

    # Sort texts by order
    texts.sort(key=lambda x: x['order'])

    # Load vocabulary
    vocabulary = {}
    vocab_file = os.path.join(data_dir, 'テキスト６．語彙データ.csv')
    if os.path.exists(vocab_file):
        with open(vocab_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if (row['subject_key'] == subject_name and
                    row['item_key'] == item_key and
                    row['chapter_key'] == chapter_key):
                    vocabulary[row['japanese_word']] = {
                        'translation': row['indonesian_translation'],
                        'context': row['usage_context']
                    }

    # Load quiz questions
    questions = []
    questions_file = os.path.join(data_dir, 'テキスト７．クイズ問題.csv')
    if os.path.exists(questions_file):
        with open(questions_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if (row['subject_key'] == subject_name and
                    row['item_key'] == item_key and
                    row['chapter_key'] == chapter_key):
                    questions.append({
                        'number': int(row['question_number']),
                        'japanese': row['japanese_question'],
                        'indonesian': row['indonesian_question'],
                        'options': []
                    })

    # Load quiz options
    options_file = os.path.join(data_dir, 'テキスト８．クイズ選択肢.csv')
    if os.path.exists(options_file):
        with open(options_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if (row['subject_key'] == subject_name and
                    row['item_key'] == item_key and
                    row['chapter_key'] == chapter_key):
                    question_num = int(row['question_number'])
                    # Find the matching question
                    for q in questions:
                        if q['number'] == question_num:
                            q['options'].append({
                                'number': int(row['option_number']),
                                'japanese': row['japanese_option'],
                                'indonesian': row['indonesian_option'],
                                'is_correct': row['is_correct'].lower() == 'true'
                            })
                            break

    # Load feedback
    feedback = {}
    feedback_file = os.path.join(data_dir, 'テキスト９．フィードバック.csv')
    if os.path.exists(feedback_file):
        with open(feedback_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if (row['subject_key'] == subject_name and
                    row['item_key'] == item_key and
                    row['chapter_key'] == chapter_key):
                    q_num = int(row['question_number'])
                    opt_num = int(row['option_number'])
                    if q_num not in feedback:
                        feedback[q_num] = {}
                    feedback[q_num][opt_num] = {
                        'japanese': row['japanese_feedback'],
                        'indonesian': row['indonesian_feedback']
                    }

    # Sort questions by number
    questions.sort(key=lambda x: x['number'])

    # Sort options within each question
    for q in questions:
        q['options'].sort(key=lambda x: x['number'])

    # Process text to add vocabulary word spans
    import re
    for text in texts:
        japanese = text['japanese']
        # Add vocabulary word spans
        for word, data in vocabulary.items():
            # Escape special regex characters
            escaped_word = re.escape(word)
            # Replace word with span containing translation
            replacement = f'<span class="vocabulary-word" data-translation="{data["translation"]}">{word}</span>'
            japanese = re.sub(escaped_word, replacement, japanese)
        text['japanese'] = japanese

    import json
    chapter_data = {
        'title': title,
        'texts': texts,
        'vocabulary': vocabulary,
        'questions': questions,
        'feedback': json.dumps(feedback)  # Convert to JSON string
    }

    return render(request, 'subjects/chapter_learning.html', {
        'subject_name': subject_name,
        'subject': subject,
        'chapter': chapter,
        'chapter_title': title,
        'chapter_data': chapter_data,
        'user': request.user
    })