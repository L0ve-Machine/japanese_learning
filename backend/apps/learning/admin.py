from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import (
    SubjectGroup, Subject, ExamYear, ExamSession, Question, Choice, Word, FlashCard, Video, StudyText,
    SubjectItem, Chapter, Page, UserProgress
)
from .forms import DataImportForm
from .services import DataImportService

@admin.register(SubjectGroup)
class SubjectGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'group_key', 'order', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'group_key', 'description']
    ordering = ['order', 'name']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject_key', 'group', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'group']
    search_fields = ['name', 'subject_key']
    ordering = ['group__order', 'order', 'name']

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

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ['japanese', 'reading', 'category', 'is_premium', 'created_at']
    list_filter = ['category', 'is_premium']
    search_fields = ['japanese', 'reading']

@admin.register(FlashCard)
class FlashCardAdmin(admin.ModelAdmin):
    list_display = ['user', 'word', 'is_memorized', 'review_count', 'last_reviewed']
    list_filter = ['is_memorized']
    search_fields = ['user__email', 'word__japanese']

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'duration_minutes', 'is_premium', 'order']
    list_filter = ['is_premium', 'subject']
    search_fields = ['title', 'description']
    ordering = ['order', 'title']

# Hierarchical Content Admin
@admin.register(SubjectItem)
class SubjectItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'subject']
    search_fields = ['name', 'description']
    ordering = ['subject', 'order', 'name']

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ['name', 'item', 'get_subject', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'item__subject']
    search_fields = ['name', 'description']
    ordering = ['item__subject', 'item__order', 'order', 'name']

    def get_subject(self, obj):
        return obj.item.subject.name
    get_subject.short_description = 'Subject'

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['name', 'chapter', 'get_item', 'get_subject', 'order', 'is_active']
    list_filter = ['is_active', 'chapter__item__subject']
    search_fields = ['name', 'description']
    ordering = ['chapter__item__subject', 'chapter__item__order', 'chapter__order', 'order']

    def get_item(self, obj):
        return obj.chapter.item.name
    get_item.short_description = 'Item'

    def get_subject(self, obj):
        return obj.chapter.item.subject.name
    get_subject.short_description = 'Subject'

@admin.register(StudyText)
class StudyTextAdmin(admin.ModelAdmin):
    list_display = ['title', 'page', 'get_chapter', 'get_subject', 'order', 'is_premium']
    list_filter = ['is_premium', 'page__chapter__item__subject']
    search_fields = ['title', 'content']
    ordering = ['page__chapter__item__subject', 'page__chapter__order', 'page__order', 'order']

    def get_chapter(self, obj):
        return obj.page.chapter.name
    get_chapter.short_description = 'Chapter'

    def get_subject(self, obj):
        return obj.page.chapter.item.subject.name
    get_subject.short_description = 'Subject'

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject', 'item', 'chapter', 'page', 'completed', 'completion_percentage', 'last_accessed']
    list_filter = ['completed', 'subject']
    search_fields = ['user__email', 'subject__name']
    ordering = ['-last_accessed']

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

# 全てのモデルをカスタム管理サイトに登録
learning_admin_site.register(SubjectGroup, SubjectGroupAdmin)
learning_admin_site.register(Subject, SubjectAdmin)
learning_admin_site.register(ExamYear, ExamYearAdmin)
learning_admin_site.register(ExamSession, ExamSessionAdmin)
learning_admin_site.register(Question, QuestionAdmin)
learning_admin_site.register(Choice, ChoiceAdmin)
learning_admin_site.register(Word, WordAdmin)
learning_admin_site.register(FlashCard, FlashCardAdmin)
learning_admin_site.register(Video, VideoAdmin)
learning_admin_site.register(SubjectItem, SubjectItemAdmin)
learning_admin_site.register(Chapter, ChapterAdmin)
learning_admin_site.register(Page, PageAdmin)
learning_admin_site.register(StudyText, StudyTextAdmin)
learning_admin_site.register(UserProgress, UserProgressAdmin)