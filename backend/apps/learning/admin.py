from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
import nested_admin
from .models import (
    SubjectGroup, Subject, ExamYear, ExamSession, Question, Choice, Video, VideoContentBlock,
    SubjectItem, Chapter, Page, UserProgress,
    KotobaCategory, KotobaSubcategory, KotobaWord, KotobaExample, KotobaVocabulary, UserWordProgress,
    TextBlock, VocabularyEntry, QuizQuestion, QuizOption
)
from .forms import DataImportForm
# from .services import DataImportService

# ============================================================================
# GROUP 1: STRUCTURE/OUTLINE - Nested Inlines for Subject → Item → Chapter → Page
# ============================================================================

class PageNestedInline(nested_admin.NestedStackedInline):
    model = Page
    extra = 1
    fields = ['name', 'description', 'order', 'is_active']
    ordering = ['order']
    show_change_link = True  # Link to edit page content
    verbose_name = "Page"
    verbose_name_plural = "Pages (belong to this chapter)"
    classes = ['collapse']  # Makes each page collapsible

class ChapterNestedInline(nested_admin.NestedTabularInline):
    model = Chapter
    extra = 1
    fields = ['name', 'description', 'order', 'is_active']
    ordering = ['order']
    inlines = [PageNestedInline]
    show_change_link = True
    verbose_name = "Chapter"
    verbose_name_plural = "Chapters (expand to add pages)"

class SubjectItemNestedInline(nested_admin.NestedTabularInline):
    model = SubjectItem
    extra = 1
    fields = ['name', 'description', 'order', 'is_active']
    ordering = ['order']
    inlines = [ChapterNestedInline]
    show_change_link = True
    verbose_name = "Item"
    verbose_name_plural = "Items (expand to add chapters and pages)"

# ============================================================================
# GROUP 2: CONTENT/DETAILS - Nested Inlines for Page → TextBlocks → Vocab, Quizzes → Options
# ============================================================================

class VocabularyEntryNestedInline(nested_admin.NestedTabularInline):
    model = VocabularyEntry
    extra = 1
    fields = ['japanese_word', 'indonesian_translation', 'translations', 'order']
    ordering = ['order']

class TextBlockNestedInline(nested_admin.NestedStackedInline):
    model = TextBlock
    extra = 1
    fields = ['japanese_text', 'indonesian_translation', 'translations', 'order']
    ordering = ['order']
    inlines = [VocabularyEntryNestedInline]

class QuizOptionNestedInline(nested_admin.NestedTabularInline):
    model = QuizOption
    extra = 5
    fields = ['option_number', 'option_text', 'is_correct', 'explanation_japanese', 'explanation_indonesian', 'translations']
    ordering = ['option_number']

class QuizQuestionNestedInline(nested_admin.NestedStackedInline):
    model = QuizQuestion
    extra = 1
    fields = ['question_number', 'question_text', 'order']
    ordering = ['order']
    inlines = [QuizOptionNestedInline]

# ============================================================================
# ADMIN CLASSES
# ============================================================================

@admin.register(SubjectGroup)
class SubjectGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'group_key', 'order', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'group_key', 'description']
    ordering = ['order', 'name']

@admin.register(Subject)
class SubjectAdmin(nested_admin.NestedModelAdmin):
    list_display = ['name', 'icon', 'color', 'subject_key', 'group', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'group']
    search_fields = ['name', 'subject_key']
    ordering = ['group__order', 'order', 'name']
    inlines = [SubjectItemNestedInline]  # GROUP 1: Nested structure

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'indonesian_name', 'translations', 'description', 'subject_key', 'group')
        }),
        ('UI Customization', {
            'fields': ('icon', 'color'),
            'description': 'Customize how this subject appears on the subjects page'
        }),
        ('Organization', {
            'fields': ('order', 'is_active')
        }),
    )

@admin.register(ExamYear)
class ExamYearAdmin(admin.ModelAdmin):
    list_display = ['year', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['year', 'description']
    ordering = ['-year']

@admin.register(ExamSession)
class ExamSessionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'year', 'session_number', 'name', 'is_active', 'created_at']
    list_filter = ['year__year', 'is_active']
    search_fields = ['name']
    ordering = ['-year__year', '-session_number']
    filter_horizontal = ['subjects']

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4
    ordering = ['choice_number']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_number', 'question_type', 'subject', 'exam_session', 'year', 'is_premium']
    list_filter = ['question_type', 'is_premium', 'year', 'subject', 'exam_session']
    search_fields = ['question_text', 'question_number']
    ordering = ['exam_session', 'question_number']
    inlines = [ChoiceInline]

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['question', 'choice_number', 'choice_text', 'is_correct']
    list_filter = ['is_correct', 'question__subject', 'question__exam_session']
    search_fields = ['choice_text', 'question__question_text']
    ordering = ['question', 'choice_number']

# Note: Old Word and FlashCard models are deprecated
# Now using KotobaWord and FlashcardDeck/FlashcardCard instead

class VideoContentBlockInline(admin.StackedInline):
    model = VideoContentBlock
    extra = 1
    fields = ['japanese_text', 'indonesian_translation', 'order']
    ordering = ['order']
    verbose_name = 'コンテンツブロック'
    verbose_name_plural = 'コンテンツブロック（日本語とインドネシア語翻訳）'

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'duration_minutes', 'is_premium', 'order', 'created_at']
    list_filter = ['is_premium', 'subject']
    search_fields = ['title', 'description', 'content']
    ordering = ['order', 'title']
    list_editable = ['order']
    inlines = [VideoContentBlockInline]

    fieldsets = (
        ('基本情報', {
            'fields': ('title', 'description', 'subject')
        }),
        ('動画設定', {
            'fields': ('video_url', 'thumbnail_url', 'duration_minutes'),
            'description': 'YouTube URL (例: https://youtu.be/7fvCb5_Nzq4 または https://youtube.com/watch?v=...)'
        }),
        ('その他', {
            'fields': ('is_premium', 'order')
        }),
    )

# Hierarchical Content Admin
# Note: SubjectItem and Chapter are edited via nested inlines in SubjectAdmin
# This keeps the admin interface clean and organized

@admin.register(Page)
class PageAdmin(nested_admin.NestedModelAdmin):
    list_display = ['name', 'chapter', 'get_item', 'get_subject', 'order', 'is_active']
    list_filter = ['is_active', 'chapter__item__subject']
    search_fields = ['name', 'description']
    ordering = ['chapter__item__subject', 'chapter__item__order', 'chapter__order', 'order']
    inlines = [TextBlockNestedInline, QuizQuestionNestedInline]  # GROUP 2: Nested content

    def get_item(self, obj):
        return obj.chapter.item.name
    get_item.short_description = 'Item'

    def get_subject(self, obj):
        return obj.chapter.item.subject.name
    get_subject.short_description = 'Subject'

# Note: StudyText is not being used (deprecated in favor of TextBlock)
# Note: TextBlock, VocabularyEntry, QuizQuestion, QuizOption are edited via nested inlines in PageAdmin
# This provides a cleaner workflow: edit everything on the Page admin page

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject', 'item', 'chapter', 'page', 'completed', 'completion_percentage', 'last_accessed']
    list_filter = ['completed', 'subject']
    search_fields = ['user__email', 'subject__name']
    ordering = ['-last_accessed']

# ============================================================================
# KOTOBA ADMIN - Nested structure for efficient editing
# ============================================================================

# Nested inline for vocabulary within examples
class KotobaVocabularyNestedInline(nested_admin.NestedTabularInline):
    model = KotobaVocabulary
    extra = 1
    fields = ['vocabulary_id', 'japanese_word', 'ruby_reading', 'indonesian_translation']
    ordering = ['japanese_word']
    verbose_name = "Vocabulary word in example"
    verbose_name_plural = "Vocabulary words in this example"

# Nested inline for examples within words
class KotobaExampleNestedInline(nested_admin.NestedStackedInline):
    model = KotobaExample
    extra = 1
    fields = ['example_id', 'japanese_example', 'indonesian_example', 'order_number']
    ordering = ['order_number']
    inlines = [KotobaVocabularyNestedInline]
    verbose_name = "Example sentence"
    verbose_name_plural = "Example sentences"
    classes = ['collapse']

# Kotoba Admin Classes
@admin.register(KotobaCategory)
class KotobaCategoryAdmin(admin.ModelAdmin):
    list_display = ['japanese_name', 'category_key', 'indonesian_translation', 'ruby_reading', 'order_number', 'word_count', 'created_at']
    search_fields = ['japanese_name', 'category_key', 'indonesian_translation']
    ordering = ['order_number', 'japanese_name']
    list_editable = ['order_number']  # Quick edit order in list view

    def word_count(self, obj):
        return obj.words.count()
    word_count.short_description = 'Total Words'

@admin.register(KotobaSubcategory)
class KotobaSubcategoryAdmin(admin.ModelAdmin):
    list_display = ['japanese_name', 'subcategory_key', 'main_category', 'indonesian_translation', 'ruby_reading', 'order_number', 'word_count']
    list_filter = ['main_category']
    search_fields = ['japanese_name', 'subcategory_key', 'indonesian_translation']
    ordering = ['main_category__order_number', 'order_number']
    list_editable = ['order_number']  # Quick edit order in list view

    def word_count(self, obj):
        return obj.words.count()
    word_count.short_description = 'Words'

@admin.register(KotobaWord)
class KotobaWordAdmin(nested_admin.NestedModelAdmin):
    list_display = ['japanese_word', 'ruby_reading', 'word_id', 'main_category', 'subcategory', 'indonesian_translation', 'example_count']
    list_filter = ['main_category', 'subcategory']
    search_fields = ['japanese_word', 'word_id', 'indonesian_translation', 'ruby_reading']
    ordering = ['main_category__order_number', 'subcategory__order_number', 'japanese_word']
    inlines = [KotobaExampleNestedInline]  # Add examples and vocab inline

    fieldsets = (
        ('Word Information', {
            'fields': ('word_id', 'japanese_word', 'ruby_reading', 'indonesian_translation')
        }),
        ('Category', {
            'fields': ('main_category', 'subcategory')
        }),
    )

    def example_count(self, obj):
        return obj.examples.count()
    example_count.short_description = 'Examples'

# Note: KotobaExample and KotobaVocabulary are managed via nested inlines in KotobaWordAdmin
# This keeps the admin interface clean - edit everything from the Word page

@admin.register(UserWordProgress)
class UserWordProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'word', 'is_memorized', 'review_count', 'last_reviewed']
    list_filter = ['is_memorized', 'word__main_category']
    search_fields = ['user__email', 'word__japanese_word']
    ordering = ['-last_reviewed']

class LearningAdminSite(admin.AdminSite):
    """学習データ管理用のカスタム管理サイト"""
    site_header = '介護福祉士試験対策 - データ管理'
    site_title = 'データ管理'
    index_title = 'データ管理メニュー'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-data/', self.admin_view(self.import_data_view), name='import_data'),
            path('download-template/', self.admin_view(self.download_template_view), name='download_template'),
        ]
        return custom_urls + urls

    def import_data_view(self, request):
        """データインポートビュー"""
        if request.method == 'POST':
            form = DataImportForm(request.POST, request.FILES)
            if form.is_valid():
                service = DataImportService()

                # ファイル処理
                processed_data = service.process_file(request.FILES['file'])

                if processed_data is not None:
                    # データインポート実行
                    success = service.import_data(processed_data)
                    summary = service.get_import_summary()

                    if success:
                        messages.success(
                            request,
                            f'データインポートが完了しました！\n'
                            f'作成された項目: '
                            f'年度 {summary["created_count"]["years"]}件, '
                            f'セッション {summary["created_count"]["sessions"]}件, '
                            f'科目 {summary["created_count"]["subjects"]}件, '
                            f'問題 {summary["created_count"]["questions"]}件, '
                            f'選択肢 {summary["created_count"]["choices"]}件'
                        )
                        return redirect('admin:index')
                    else:
                        for error in summary['errors']:
                            messages.error(request, error)
                else:
                    summary = service.get_import_summary()
                    for error in summary['errors']:
                        messages.error(request, error)
        else:
            form = DataImportForm()

        return render(request, 'admin/learning/import_data.html', {
            'form': form,
            'title': 'データインポート',
            'opts': {'app_label': 'learning'},
        })

    def download_template_view(self, request):
        """テンプレートダウンロードビュー"""
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="question_template.csv"'

        # UTF-8 BOM を追加（Excelで正しく表示するため）
        response.write('\ufeff')

        writer = csv.writer(response)

        # ヘッダー行
        writer.writerow([
            'question_id',
            'session',
            'year',
            'question_number',
            'part',
            'subject_key',
            'japanese_question',
            'indonesian_question',
            'explanation',
            'choice_1',
            'choice_1_correct',
            'choice_2',
            'choice_2_correct',
            'choice_3',
            'choice_3_correct',
            'choice_4',
            'choice_4_correct',
            'choice_5',
            'choice_5_correct',
            'vocabulary_json'
        ])

        # サンプル行
        writer.writerow([
            'q_37_2025_1',
            '37',
            '2025',
            '1',
            'A',
            'human_dignity_independence',
            '次の記述のうち、介護福祉職がアドボカシー（advocacy）の視点から行う対応として、最も適切なものを1つ選びなさい。',
            'Dari deskripsi berikut pilihlah satu tindakan yang paling tepat yang dilakukan oleh pekerja perawatan dari sudut pandang advokasi (advocacy).',
            'アドボカシーとは、利用者の権利を擁護し、代弁することです。',
            '利用者の最善の利益を代弁する。',
            'TRUE',
            '家族が希望する介護サービスを提供する。',
            'FALSE',
            '施設の規則に従って介護を提供する。',
            'FALSE',
            '利用者個人の趣味を生かして、レクリエーション活動を行う。',
            'FALSE',
            '視覚障害者が必要とする情報を、利用しやすいようにする。',
            'FALSE',
            '{"次": {"reading": "つぎ", "translation": "berikut"}, "記述": {"reading": "きじゅつ", "translation": "deskripsi"}}'
        ])

        return response

# カスタム管理サイトのインスタンス作成
learning_admin_site = LearningAdminSite(name='learning_admin')

# Register only essential models for custom admin site
# Note: SubjectItem, Chapter are managed via nested inlines in SubjectAdmin
# Note: TextBlock, VocabularyEntry, QuizQuestion, QuizOption are managed via nested inlines in PageAdmin
# Note: Word, FlashCard, FlashcardDeck (old models) are deprecated - using KotobaWord for vocabulary
learning_admin_site.register(SubjectGroup, SubjectGroupAdmin)
learning_admin_site.register(Subject, SubjectAdmin)
learning_admin_site.register(ExamYear, ExamYearAdmin)
learning_admin_site.register(ExamSession, ExamSessionAdmin)
learning_admin_site.register(Question, QuestionAdmin)
learning_admin_site.register(Choice, ChoiceAdmin)
learning_admin_site.register(Video, VideoAdmin)
learning_admin_site.register(Page, PageAdmin)
learning_admin_site.register(UserProgress, UserProgressAdmin)