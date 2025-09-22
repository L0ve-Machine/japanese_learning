from rest_framework import serializers
from .models import Subject, Question, Word, FlashCard, Video, StudyText

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'description', 'order', 'is_active']

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

class StudyTextSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)

    class Meta:
        model = StudyText
        fields = ['id', 'subject', 'subject_name', 'title', 'content',
                  'translations', 'order', 'is_premium']