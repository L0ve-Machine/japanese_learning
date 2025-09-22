from django.contrib import admin
from .models import Subject, ExamSession, Question, Word, FlashCard, Video, StudyText

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

@admin.register(StudyText)
class StudyTextAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'order', 'is_premium', 'created_at']
    list_filter = ['is_premium', 'subject']
    search_fields = ['title', 'content']
    ordering = ['order', 'title']