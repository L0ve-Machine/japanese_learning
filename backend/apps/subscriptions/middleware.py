from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
from apps.subscriptions.models import Subscription

class SubscriptionRequiredMiddleware:
    """
    サブスクリプションが必要なページへのアクセスを制御するミドルウェア
    """

    # サブスクリプション不要なパス
    EXEMPT_PATHS = [
        '/admin/',
        '/api/auth/',
        '/login/',
        '/logout/',
        '/register/',
        '/',  # ランディングページ
        '/static/',
        '/media/',
        '/stripe/webhook/',  # Stripe Webhook
        '/subscription/plans/',  # プラン一覧
        '/subscription/checkout/',  # チェックアウト
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # デコレーターでスキップ指定されている場合
        if hasattr(request, 'skip_subscription_check') and request.skip_subscription_check:
            return self.get_response(request)

        # 認証不要なパスはスキップ
        if any(request.path.startswith(path) for path in self.EXEMPT_PATHS):
            return self.get_response(request)

        # 未認証ユーザーはログインページへ
        if not request.user.is_authenticated:
            if not request.path.startswith('/api/'):
                return redirect(reverse('login'))
            return self.get_response(request)

        # スーパーユーザーは無制限アクセス
        if request.user.is_superuser:
            return self.get_response(request)

        # アクティブなサブスクリプションをチェック
        active_subscription = Subscription.get_user_active_subscription(request.user)

        if not active_subscription:
            # APIリクエストの場合は403を返す
            if request.path.startswith('/api/'):
                from django.http import JsonResponse
                return JsonResponse({
                    'error': 'サブスクリプションが必要です',
                    'redirect': '/subscription/plans/'
                }, status=403)

            # 通常のリクエストはサブスクリプションページへリダイレクト
            messages.warning(request, 'このコンテンツにアクセスするにはプレミアムプランの登録が必要です。')
            return redirect('/subscription/plans/')

        # サブスクリプション情報をリクエストに追加
        request.subscription = active_subscription

        return self.get_response(request)