from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse

def allow_free_access(view_func):
    """
    無料アクセス可能なビューを示すデコレーター
    ミドルウェアでのチェックをスキップする
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        request.skip_subscription_check = True
        return view_func(request, *args, **kwargs)
    return wrapper