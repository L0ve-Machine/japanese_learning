from django.contrib import admin
from .models import (
    Subject, ExamSession, Question, Word, FlashCard, Video, StudyText,
    SubjectItem, Chapter, Page, UserProgress
)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject_key', 'group_key', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'group_key']
    search_fields = ['name', 'subject_key']
    ordering = ['group_key', 'order', 'name']

@admin.register(ExamSession)
class ExamSessionAdmin(admin.ModelAdmin):
    list_display = ['year', 'session_number', 'available_subjects', 'created_at']
    list_filter = ['year']
    ordering = ['-year', '-session_number']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'question_type', 'subject', 'year', 'is_premium', 'order']
    list_filter = ['question_type', 'is_premium', 'year', 'subject']
    search_fields = ['question_text']
    ordering = ['order', 'id']

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