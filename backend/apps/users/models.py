from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('vi', 'Vietnamese'),
        ('zh', 'Chinese'),
        ('ko', 'Korean'),
        ('th', 'Thai'),
        ('id', 'Indonesian'),
        ('my', 'Burmese'),
    ]

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    native_language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='en')
    is_premium = models.BooleanField(default=False)
    subscription_end_date = models.DateTimeField(null=True, blank=True)
    stripe_customer_id = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    content_type = models.CharField(max_length=50)
    content_id = models.IntegerField()
    completed = models.BooleanField(default=False)
    score = models.FloatField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_progress'
        unique_together = ['user', 'content_type', 'content_id']