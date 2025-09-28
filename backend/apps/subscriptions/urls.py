from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'plans', views.SubscriptionPlanViewSet)
router.register(r'subscriptions', views.SubscriptionViewSet, basename='subscription')
router.register(r'payments', views.PaymentViewSet, basename='payment')

# Web URLs
urlpatterns = [
    # API URLs
    path('api/', include(router.urls)),

    # Web URLs
    path('plans/', views.subscription_plans_view, name='subscription_plans'),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('success/', views.subscription_success, name='subscription_success'),
    path('premium/', views.premium_content_view, name='premium_content'),
]