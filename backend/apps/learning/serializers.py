from rest_framework import serializers
from .models import (
    Subject, Question, Word, FlashCard, Video, StudyText,
    SubjectItem, Chapter, Page, UserProgress
)

class SubjectSerializer(serializers.ModelSerializer):
    items_count = serializers.SerializerMethodField()
    chapters_count = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = ['id', 'name', 'indonesian_name', 'description', 'group_key',
                 'order', 'is_active', 'items_count', 'chapters_count', 'created_at', 'updated_at']

    def get_items_count(self, obj):
        return obj.items.filter(is_active=True).count()

    def get_chapters_count(self, obj):
        return sum(item.chapters.filter(is_active=True).count()
                  for item in obj.items.filter(is_active=True))

class QuestionSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'subject', 'subject_name', 'question_type', 'year', 'question_text',
                  'choices', 'correct_answer', 'explanation', 'translations', 'is_premium']

class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['id', 'japanese', 'reading', 'category', 'translations',
                  'example_sentence', 'example_translation', 'is_premium']

class FlashCardSerializer(serializers.ModelSerializer):
    word_data = WordSerializer(source='word', read_only=True)

    class Meta:
        model = FlashCard
        fields = ['id', 'word', 'word_data', 'is_memorized', 'review_count', 'last_reviewed']

class VideoSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)

    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'video_url', 'thumbnail_url',
                  'duration_minutes', 'subject', 'subject_name', 'is_premium', 'order']

# Hierarchical Content Serializers
class StudyTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyText
        fields = ['id', 'title', 'content', 'translations', 'order', 'is_premium']

class PageSerializer(serializers.ModelSerializer):
    texts = StudyTextSerializer(many=True, read_only=True)

    class Meta:
        model = Page
        fields = ['id', 'name', 'description', 'order', 'is_active', 'texts']

class ChapterSerializer(serializers.ModelSerializer):
    pages = PageSerializer(many=True, read_only=True)

    class Meta:
        model = Chapter
        fields = ['id', 'name', 'description', 'translations', 'order', 'is_active', 'pages']

class SubjectItemSerializer(serializers.ModelSerializer):
    chapters = ChapterSerializer(many=True, read_only=True)

    class Meta:
        model = SubjectItem
        fields = ['id', 'name', 'description', 'translations', 'order', 'is_active', 'chapters']

# Enhanced Subject Serializer with hierarchy
class SubjectDetailSerializer(serializers.ModelSerializer):
    items = SubjectItemSerializer(many=True, read_only=True)

    class Meta:
        model = Subject
        fields = ['id', 'name', 'description', 'group_key', 'order', 'is_active', 'items']

# Simple serializers for navigation
class PageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['id', 'name', 'description', 'order']

class ChapterListSerializer(serializers.ModelSerializer):
    pages = PageListSerializer(many=True, read_only=True)

    class Meta:
        model = Chapter
        fields = ['id', 'name', 'description', 'order', 'pages']

class SubjectItemListSerializer(serializers.ModelSerializer):
    chapters = ChapterListSerializer(many=True, read_only=True)

    class Meta:
        model = SubjectItem
        fields = ['id', 'name', 'description', 'order', 'chapters']

class UserProgressSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    item_name = serializers.CharField(source='item.name', read_only=True)
    chapter_name = serializers.CharField(source='chapter.name', read_only=True)
    page_name = serializers.CharField(source='page.name', read_only=True)
    text_title = serializers.CharField(source='text.title', read_only=True)

    class Meta:
        model = UserProgress
        fields = [
            'id', 'subject', 'subject_name', 'item', 'item_name',
            'chapter', 'chapter_name', 'page', 'page_name',
            'text', 'text_title', 'completed', 'completion_percentage',
            'last_accessed'
        ]