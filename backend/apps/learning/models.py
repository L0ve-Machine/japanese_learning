from django.db import models
from django.contrib.postgres.fields import JSONField
from apps.users.models import User

class Subject(models.Model):
    subject_key = models.CharField(max_length=100, unique=True, null=True, blank=True)
    group_key = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=200)
    indonesian_name = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'subjects'
        ordering = ['group_key', 'order', 'name']

    def __str__(self):
        return self.name

class ExamSession(models.Model):
    year = models.IntegerField()
    session_number = models.IntegerField()
    available_subjects = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'exam_sessions'
        ordering = ['-year', '-session_number']
        unique_together = ['year', 'session_number']

    def __str__(self):
        return f"{self.year}年 第{self.session_number}回"

class Question(models.Model):
    QUESTION_TYPES = [
        ('past_exam', '過去問題'),
        ('subject', '科目学習'),
    ]

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='questions', null=True, blank=True)
    exam_session = models.ForeignKey(ExamSession, on_delete=models.CASCADE, related_name='questions', null=True, blank=True)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    year = models.IntegerField(null=True, blank=True)
    question_text = models.TextField()
    choices = models.JSONField()
    correct_answer = models.IntegerField()
    explanation = models.TextField()
    translations = models.JSONField(default=dict, blank=True)
    is_premium = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'questions'
        ordering = ['order', 'id']

class Word(models.Model):
    WORD_CATEGORIES = [
        ('medical', '医療用語'),
        ('caregiving', '介護用語'),
        ('general', '一般用語'),
    ]

    japanese = models.CharField(max_length=200)
    reading = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=20, choices=WORD_CATEGORIES)
    translations = models.JSONField(default=dict)
    example_sentence = models.TextField(blank=True)
    example_translation = models.JSONField(default=dict, blank=True)
    is_premium = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'words'
        ordering = ['japanese']

class FlashCard(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='flashcards')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='flashcards')
    is_memorized = models.BooleanField(default=False)
    review_count = models.IntegerField(default=0)
    last_reviewed = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'flashcards'
        unique_together = ['word', 'user']

class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video_url = models.URLField()
    thumbnail_url = models.URLField(blank=True)
    duration_minutes = models.IntegerField(null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='videos', null=True, blank=True)
    is_premium = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'videos'
        ordering = ['order', 'title']

class StudyText(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='texts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    translations = models.JSONField(default=dict, blank=True)
    order = models.IntegerField(default=0)
    is_premium = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'study_texts'
        ordering = ['order', 'title']