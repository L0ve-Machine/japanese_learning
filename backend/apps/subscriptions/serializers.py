from rest_framework import serializers
from .models import SubscriptionPlan, Subscription, Payment

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ['id', 'name', 'description', 'price', 'duration_days', 'features', 'is_active']

class SubscriptionSerializer(serializers.ModelSerializer):
    plan_details = SubscriptionPlanSerializer(source='plan', read_only=True)

    class Meta:
        model = Subscription
        fields = ['id', 'plan', 'plan_details', 'status', 'start_date', 'end_date', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'subscription', 'amount', 'currency', 'status', 'created_at']
        read_only_fields = ['id', 'created_at']