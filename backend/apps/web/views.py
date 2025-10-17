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

    # Get questions for this exam session from database
    questions = Question.objects.filter(
        exam_session=exam_session
    ).prefetch_related('choices').order_by('question_number')

    # Calculate total questions
    total_questions = questions.count()

    # If no questions exist, show error message
    if total_questions == 0:
        messages.warning(request, f'{exam_year.year}年 第{exam_session.session_number}回の問題データがまだ登録されていません。')
        return redirect('past_exams')

    try:
        current_question = questions[question_number - 1]
    except IndexError:
        current_question = questions.first()
        question_number = 1

    # Calculate progress
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
    """科目学習メインページ - Load subjects from database"""
    from apps.learning.models import Subject

    # Get all active subjects from database with prefetch
    subjects = Subject.objects.filter(is_active=True).prefetch_related(
        'items__chapters'
    ).order_by('order')

    # Add chapter count to each subject
    for subject in subjects:
        subject.total_chapters = sum(item.chapters.count() for item in subject.items.all())

    # Get user's language preference (URL param overrides user setting)
    user_language = request.GET.get('lang')
    if not user_language:
        user_language = request.user.native_language if request.user.is_authenticated else 'id'

    return render(request, 'subjects/subject_learning.html', {
        'subjects': subjects,
        'user': request.user,
        'user_language': user_language,
    })

@login_required
@allow_free_access
def subject_detail_view(request, subject_name):
    """個別科目詳細ページ - Load from database"""
    from django.shortcuts import get_object_or_404
    from django.http import Http404
    from apps.learning.models import Subject, SubjectItem, TextBlock

    # セキュリティ: パストラバーサル攻撃を防ぐ
    if '..' in subject_name or '/' in subject_name:
        raise Http404("Invalid subject name")

    # Get subject from database
    try:
        subject_obj = Subject.objects.get(name=subject_name, is_active=True)
    except Subject.DoesNotExist:
        raise Http404("Subject not found")

    # Get items with chapters and pages
    items = subject_obj.items.filter(is_active=True).prefetch_related(
        'chapters__pages'
    ).order_by('order')

    # Calculate stats
    total_items = items.count()
    total_chapters = sum(item.chapters.count() for item in items)

    # Calculate completion percentage (count pages with text blocks)
    total_pages = sum(chapter.pages.count() for item in items for chapter in item.chapters.all())
    completed_pages = 0
    for item in items:
        for chapter in item.chapters.all():
            for page in chapter.pages.all():
                if TextBlock.objects.filter(page=page).exists():
                    completed_pages += 1

    completion_percentage = int((completed_pages / total_pages * 100)) if total_pages > 0 else 0

    # Get user's language preference (URL param overrides user setting)
    user_language = request.GET.get('lang')
    if not user_language:
        user_language = request.user.native_language if request.user.is_authenticated else 'id'

    # Use icon and color from database with fallback defaults
    subject = {
        'title': subject_obj.name,
        'description': subject_obj.indonesian_name,
        'icon': subject_obj.icon or 'menu_book',
        'color': subject_obj.color or '#607d8b',
        'stats': {
            'total_items': total_items,
            'total_chapters': total_chapters,
            'completion_percentage': completion_percentage
        }
    }

    return render(request, 'subjects/subject_detail.html', {
        'subject_name': subject_name,
        'subject': subject,
        'subject_obj': subject_obj,
        'items': items,
        'user': request.user,
        'user_language': user_language,
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

@login_required
@allow_free_access
def flashcards_view(request):
    """暗記カード（フラッシュカード）メインページ"""
    from apps.learning.models import FlashcardDeck
    from django.db.models import Count

    # Get all active decks with card counts
    decks = FlashcardDeck.objects.filter(is_active=True).annotate(
        card_count=Count('cards')
    ).order_by('order', 'name')

    # Get deck data with card counts
    deck_data = []
    for deck in decks:
        deck_data.append({
            'deck': deck,
            'total_cards': deck.card_count
        })

    return render(request, 'flashcards/main.html', {
        'deck_data': deck_data,
        'user': request.user
    })

@login_required
@allow_free_access
def flashcards_study_view(request, deck_id):
    """暗記カード学習ページ"""
    from apps.learning.models import FlashcardDeck, FlashcardCard
    from django.shortcuts import get_object_or_404

    deck = get_object_or_404(FlashcardDeck, id=deck_id, is_active=True)

    # Get all cards in deck
    all_cards = FlashcardCard.objects.filter(deck=deck).order_by('order')

    cards_to_review = []
    for card in all_cards:
        cards_to_review.append({
            'card': card,
            'is_new': False
        })

    return render(request, 'flashcards/study.html', {
        'deck': deck,
        'cards_to_review': cards_to_review,
        'total_cards': all_cards.count(),
        'user': request.user
    })

@login_required
def flashcards_update_progress(request, card_id):
    """Update flashcard progress - simple review count only"""
    from apps.learning.models import FlashcardCard, UserFlashcardProgress
    from django.shortcuts import get_object_or_404
    from django.http import JsonResponse
    from django.utils import timezone

    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)

    card = get_object_or_404(FlashcardCard, id=card_id)

    # Get or create progress
    progress, created = UserFlashcardProgress.objects.get_or_create(
        user=request.user,
        card=card,
        defaults={
            'ease_factor': 2.5,
            'interval_days': 0,
            'repetitions': 0
        }
    )

    # Simple review count increment
    progress.total_reviews += 1
    progress.last_reviewed = timezone.now()
    progress.save()

    return JsonResponse({
        'success': True,
        'next_review_date': progress.next_review_date.isoformat(),
        'interval_days': progress.interval_days,
        'is_mastered': progress.is_mastered
    })

@login_required
def csv_import_view(request):
    """CSV/Excelインポート画面"""
    from apps.learning.models import Question, Choice

    if not request.user.is_staff:
        messages.error(request, '管理者権限が必要です。')
        return redirect('dashboard')

    if request.method == 'POST' and request.FILES.get('csv_file'):
        import csv
        import json
        from apps.learning.models import ExamYear, ExamSession, Subject

        csv_file = request.FILES['csv_file']
        file_name = csv_file.name.lower()

        # Check file extension
        if not (file_name.endswith('.csv') or file_name.endswith('.xlsx') or file_name.endswith('.xls')):
            messages.error(request, 'CSV または Excel ファイル (.csv, .xlsx, .xls) をアップロードしてください。')
            return redirect('csv_import')

        try:
            # Handle Excel files
            if file_name.endswith(('.xlsx', '.xls')):
                import openpyxl
                import io

                workbook = openpyxl.load_workbook(io.BytesIO(csv_file.read()))
                sheet = workbook.active

                # Convert to list of dicts
                headers = [cell.value for cell in sheet[1]]
                rows = []
                for row in sheet.iter_rows(min_row=2, values_only=True):
                    rows.append(dict(zip(headers, row)))
            else:
                # Handle CSV files
                decoded_file = csv_file.read().decode('utf-8').splitlines()
                reader = csv.DictReader(decoded_file)
                rows = list(reader)

            success_count = 0
            error_count = 0
            error_messages = []

            for row in rows:
                try:
                    # Get exam year
                    year = int(row['year'])
                    exam_year = ExamYear.objects.get(year=year)

                    # Get exam session
                    session_number = int(row['session'])
                    exam_session = ExamSession.objects.get(
                        year=exam_year,
                        session_number=session_number
                    )

                    # Get subject
                    subject_key = row['subject_key']
                    subject = Subject.objects.get(subject_key=subject_key)

                    # Parse vocabulary
                    vocabulary = {}
                    try:
                        if row.get('vocabulary_json'):
                            vocabulary = json.loads(row['vocabulary_json'])
                    except (json.JSONDecodeError, KeyError):
                        vocabulary = {}

                    # Create question
                    question, created = Question.objects.get_or_create(
                        exam_session=exam_session,
                        subject=subject,
                        question_number=int(row['question_number']),
                        defaults={
                            'question_type': 'past_exam',
                            'year': year,
                            'question_text': row['japanese_question'],
                            'explanation': row.get('explanation', ''),
                            'translations': {
                                'id': row.get('indonesian_question', '')
                            },
                            'vocabulary': vocabulary
                        }
                    )

                    if created:
                        # Add choices
                        choices_data = [
                            (1, row.get('choice_1'), row.get('choice_1_correct') == 'TRUE'),
                            (2, row.get('choice_2'), row.get('choice_2_correct') == 'TRUE'),
                            (3, row.get('choice_3'), row.get('choice_3_correct') == 'TRUE'),
                            (4, row.get('choice_4'), row.get('choice_4_correct') == 'TRUE'),
                            (5, row.get('choice_5'), row.get('choice_5_correct') == 'TRUE'),
                        ]

                        for choice_num, choice_text, is_correct in choices_data:
                            if choice_text:
                                Choice.objects.create(
                                    question=question,
                                    choice_number=choice_num,
                                    choice_text=choice_text,
                                    is_correct=is_correct
                                )

                        success_count += 1
                    else:
                        error_count += 1
                        error_messages.append(f"問題 {row['question_number']} は既に存在します")

                except Exception as e:
                    error_count += 1
                    error_messages.append(f"行の処理エラー: {str(e)}")

            # Show results
            if success_count > 0:
                messages.success(request, f'{success_count} 件の問題をインポートしました。')
            if error_count > 0:
                messages.warning(request, f'{error_count} 件のエラーがありました。')
                for err_msg in error_messages[:5]:  # Show first 5 errors
                    messages.error(request, err_msg)

        except Exception as e:
            messages.error(request, f'ファイルの処理中にエラーが発生しました: {str(e)}')

        return redirect('csv_import')

    # Get statistics
    from apps.learning.models import Question, Choice, ExamSession
    total_questions = Question.objects.count()
    total_choices = Choice.objects.count()
    sessions_with_questions = []

    for session in ExamSession.objects.all().order_by('-year__year', '-session_number'):
        question_count = Question.objects.filter(exam_session=session).count()
        if question_count > 0:
            sessions_with_questions.append({
                'session': session,
                'count': question_count
            })

    context = {
        'total_questions': total_questions,
        'total_choices': total_choices,
        'sessions_with_questions': sessions_with_questions,
    }

    return render(request, 'admin/csv_import.html', context)

@login_required
def chapter_page_view(request, page_id):
    """Chapter page view with text blocks, vocabulary, and quiz"""
    from apps.learning.models import Page, TextBlock, QuizQuestion
    from django.shortcuts import get_object_or_404

    page = get_object_or_404(Page, id=page_id)
    text_blocks = page.text_blocks.all().prefetch_related('vocabulary')
    quiz_questions = page.quiz_questions.all().prefetch_related('options')

    # Get user's language preference (URL param overrides user setting)
    user_language = request.GET.get('lang')
    if not user_language:
        user_language = request.user.native_language if request.user.is_authenticated else 'id'

    context = {
        'page': page,
        'text_blocks': text_blocks,
        'quiz_questions': quiz_questions,
        'chapter': page.chapter,
        'item': page.chapter.item,
        'subject': page.chapter.item.subject,
        'user_language': user_language,
    }

    return render(request, 'subjects/chapter_page.html', context)

@login_required
@allow_free_access
def videos_view(request):
    """解説動画一覧ページ"""
    from apps.learning.models import Video, Subject

    # Get all active videos
    videos = Video.objects.filter(is_active=True).select_related('subject').order_by('order', 'created_at')

    # Get subjects for filtering
    subjects = Subject.objects.filter(is_active=True).order_by('order')

    return render(request, 'videos/list.html', {
        'videos': videos,
        'subjects': subjects,
        'user': request.user
    })

@login_required
@allow_free_access
def video_detail_view(request, video_id):
    """解説動画詳細ページ"""
    from apps.learning.models import Video
    from django.shortcuts import get_object_or_404

    video = get_object_or_404(Video, id=video_id)

    return render(request, 'videos/detail.html', {
        'video': video,
        'user': request.user
    })
