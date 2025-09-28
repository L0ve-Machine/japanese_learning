from django.db import models
from django.contrib.postgres.fields import JSONField
from apps.users.models import User

class SubjectGroup(models.Model):
    """Subject groups for organizing exam subjects"""
    name = models.CharField(max_length=200)
    group_key = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'subject_groups'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

class Subject(models.Model):
    subject_key = models.CharField(max_length=100, unique=True, null=True, blank=True)
    group = models.ForeignKey(SubjectGroup, on_delete=models.CASCADE, related_name='subjects', null=True, blank=True)
    name = models.CharField(max_length=200)
    indonesian_name = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'subjects'
        ordering = ['group__order', 'order', 'name']

    def __str__(self):
        return self.name

class ExamYear(models.Model):
    """Year for past exams"""
    year = models.IntegerField(unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'exam_years'
        ordering = ['-year']

    def __str__(self):
        return f"{self.year}年"

class ExamSession(models.Model):
    year = models.ForeignKey(ExamYear, on_delete=models.CASCADE, related_name='sessions')
    session_number = models.IntegerField()
    name = models.CharField(max_length=200, blank=True)
    subjects = models.ManyToManyField(Subject, related_name='exam_sessions', blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'exam_sessions'
        ordering = ['-year__year', '-session_number']
        unique_together = ['year', 'session_number']

    def __str__(self):
        return f"{self.year.year}年 第{self.session_number}回"

class Question(models.Model):
    QUESTION_TYPES = [
        ('past_exam', '過去問題'),
        ('subject', '科目学習'),
    ]

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='questions', null=True, blank=True)
    exam_session = models.ForeignKey(ExamSession, on_delete=models.CASCADE, related_name='questions', null=True, blank=True)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    year = models.IntegerField(null=True, blank=True)
    question_number = models.IntegerField(default=1)
    question_text = models.TextField()
    explanation = models.TextField()
    translations = models.JSONField(default=dict, blank=True)
    vocabulary = models.JSONField(default=dict, blank=True)
    is_premium = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'questions'
        ordering = ['order', 'question_number']

    def __str__(self):
        return f"問題{self.question_number}: {self.question_text[:50]}..."

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_number = models.IntegerField()
    choice_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    explanation = models.TextField(blank=True)
    translations = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'choices'
        ordering = ['choice_number']
        unique_together = ['question', 'choice_number']

    def __str__(self):
        return f"{self.choice_number}. {self.choice_text[:30]}..."

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

# Hierarchical Learning Content Models
class SubjectItem(models.Model):
    """項目 (Item) - Second level in hierarchy"""
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    translations = models.JSONField(default=dict, blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'subject_items'
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.subject.name} - {self.name}"

class Chapter(models.Model):
    """章 (Chapter) - Third level in hierarchy"""
    item = models.ForeignKey(SubjectItem, on_delete=models.CASCADE, related_name='chapters')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    translations = models.JSONField(default=dict, blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'chapters'
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.item.name} - {self.name}"

class Page(models.Model):
    """ページ (Page) - Fourth level in hierarchy"""
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='pages')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pages'
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.chapter.name} - {self.name}"

class StudyText(models.Model):
    """テキスト (Text) - Fifth level in hierarchy"""
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='texts')
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

    def __str__(self):
        return f"{self.page.name} - {self.title}"

# User Progress Tracking
class UserProgress(models.Model):
    """Track user progress through the hierarchical content"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_progress')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    item = models.ForeignKey(SubjectItem, on_delete=models.CASCADE, null=True, blank=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, null=True, blank=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, null=True, blank=True)
    text = models.ForeignKey(StudyText, on_delete=models.CASCADE, null=True, blank=True)
    completed = models.BooleanField(default=False)
    completion_percentage = models.FloatField(default=0.0)
    last_accessed = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'learning_user_progress'
        unique_together = ['user', 'subject', 'item', 'chapter', 'page', 'text']