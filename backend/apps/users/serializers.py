from rest_framework import serializers
from .models import User, UserProgress

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'native_language', 'is_premium', 'subscription_end_date', 'created_at']
        read_only_fields = ['id', 'is_premium', 'subscription_end_date', 'created_at']

class UserProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProgress
        fields = ['id', 'content_type', 'content_id', 'completed', 'score', 'completed_at', 'created_at']
        read_only_fields = ['id', 'created_at']