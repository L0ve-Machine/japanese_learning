from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import timedelta
from .models import SubscriptionPlan, Subscription, Payment
from .serializers import SubscriptionPlanSerializer, SubscriptionSerializer, PaymentSerializer
from .decorators import subscription_required
import stripe
import json

stripe.api_key = settings.STRIPE_SECRET_KEY if hasattr(settings, 'STRIPE_SECRET_KEY') else None

class SubscriptionPlanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubscriptionPlan.objects.filter(is_active=True)
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [AllowAny]

class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def create_checkout_session(self, request):
        plan_id = request.data.get('plan_id')
        try:
            plan = SubscriptionPlan.objects.get(id=plan_id)

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': plan.stripe_price_id,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=request.build_absolute_uri('/success'),
                cancel_url=request.build_absolute_uri('/cancel'),
                customer_email=request.user.email,
                metadata={
                    'user_id': request.user.id,
                    'plan_id': plan.id
                }
            )

            return Response({'checkout_url': checkout_session.url})
        except SubscriptionPlan.DoesNotExist:
            return Response({'error': 'Plan not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        subscription = self.get_object()
        try:
            if subscription.stripe_subscription_id:
                stripe.Subscription.modify(
                    subscription.stripe_subscription_id,
                    cancel_at_period_end=True
                )
            subscription.status = 'cancelled'
            subscription.save()
            return Response({'status': 'cancelled'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)


# Web View Functions
@login_required
def subscription_plans_view(request):
    """サブスクリプションプラン一覧表示"""
    plans = SubscriptionPlan.objects.filter(is_active=True)
    current_subscription = Subscription.get_user_active_subscription(request.user)

    context = {
        'plans': plans,
        'current_subscription': current_subscription,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY if hasattr(settings, 'STRIPE_PUBLIC_KEY') else '',
    }
    return render(request, 'subscriptions/plans.html', context)


@csrf_exempt
@require_POST
def stripe_webhook(request):
    """Stripe Webhookハンドラー"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    if not hasattr(settings, 'STRIPE_WEBHOOK_SECRET'):
        return JsonResponse({'error': 'Webhook設定が不完全です'}, status=500)

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({'error': 'Invalid signature'}, status=400)

    # チェックアウト完了時の処理
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_id = session.get('metadata', {}).get('user_id')
        plan_id = session.get('metadata', {}).get('plan_id')
        stripe_subscription_id = session.get('subscription')

        if user_id and plan_id:
            from apps.users.models import User
            try:
                user = User.objects.get(id=user_id)
                plan = SubscriptionPlan.objects.get(id=plan_id)

                # 既存のアクティブなサブスクリプションをキャンセル
                Subscription.objects.filter(user=user, status='active').update(status='cancelled')

                # 新しいサブスクリプション作成
                subscription = Subscription.objects.create(
                    user=user,
                    plan=plan,
                    status='active',
                    start_date=timezone.now(),
                    end_date=timezone.now() + timedelta(days=plan.duration_days),
                    stripe_subscription_id=stripe_subscription_id or ''
                )

                Payment.objects.create(
                    user=user,
                    subscription=subscription,
                    amount=plan.price,
                    currency='JPY',
                    stripe_payment_intent_id=session.get('payment_intent', ''),
                    status='completed'
                )
            except (User.DoesNotExist, SubscriptionPlan.DoesNotExist) as e:
                print(f"Webhook processing error: {str(e)}")

    return JsonResponse({'received': True})


@login_required
def subscription_success(request):
    """サブスクリプション成功ページ"""
    messages.success(request, 'プレミアムプランへの登録が完了しました！')
    return redirect('dashboard')


@login_required
@subscription_required
def premium_content_view(request):
    """プレミアム会員限定コンテンツの例"""
    return render(request, 'subscriptions/premium_content.html', {
        'subscription': request.subscription
    })