from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class TranslationCache(models.Model):
    """翻訳結果のキャッシュ"""
    original_text = models.TextField()
    translated_text = models.TextField()
    source_language = models.CharField(max_length=10, default='ja')
    target_language = models.CharField(max_length=10)
    translation_service = models.CharField(max_length=50, default='google')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'translation_cache'
        unique_together = ['original_text', 'source_language', 'target_language']
        indexes = [
            models.Index(fields=['source_language', 'target_language']),
        ]

    def __str__(self):
        return f"{self.source_language} -> {self.target_language}: {self.original_text[:50]}..."

class UserLanguagePreference(models.Model):
    """ユーザーの言語設定"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='language_preference')
    preferred_language = models.CharField(max_length=10, default='ja')
    auto_translate = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_language_preferences'

    def __str__(self):
        return f"{self.user.email}: {self.preferred_language}"