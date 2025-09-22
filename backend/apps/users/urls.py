from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserProgressViewSet

router = DefaultRouter()
router.register(r'profile', UserViewSet, basename='user')
router.register(r'progress', UserProgressViewSet, basename='progress')

urlpatterns = [
    path('', include(router.urls)),
]