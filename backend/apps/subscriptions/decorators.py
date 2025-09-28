from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from apps.subscriptions.models import Subscription

def subscription_required(view_func):
    """
    ビューレベルでサブスクリプションを要求するデコレーター
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'ログインが必要です。')
            return redirect('login')

        # スーパーユーザーは制限なし
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        # アクティブなサブスクリプションをチェック
        active_subscription = Subscription.get_user_active_subscription(request.user)

        if not active_subscription:
            messages.warning(request, 'このコンテンツにアクセスするにはプレミアムプランの登録が必要です。')
            return redirect('/subscription/plans/')

        # サブスクリプション情報を付加
        request.subscription = active_subscription
        return view_func(request, *args, **kwargs)

    return wrapper

def api_subscription_required(view_func):
    """
    APIビュー用のサブスクリプション要求デコレーター
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                'error': '認証が必要です'
            }, status=401)

        # スーパーユーザーは制限なし
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        # アクティブなサブスクリプションをチェック
        active_subscription = Subscription.get_user_active_subscription(request.user)

        if not active_subscription:
            return JsonResponse({
                'error': 'プレミアムプランの登録が必要です',
                'subscription_required': True,
                'redirect_url': '/subscription/plans/'
            }, status=403)

        request.subscription = active_subscription
        return view_func(request, *args, **kwargs)

    return wrapper