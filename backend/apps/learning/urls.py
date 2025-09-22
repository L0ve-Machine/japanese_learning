from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SubjectViewSet, QuestionViewSet, WordViewSet,
    FlashCardViewSet, VideoViewSet, StudyTextViewSet
)

router = DefaultRouter()
router.register(r'subjects', SubjectViewSet)
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'words', WordViewSet, basename='word')
router.register(r'flashcards', FlashCardViewSet, basename='flashcard')
router.register(r'videos', VideoViewSet, basename='video')
router.register(r'texts', StudyTextViewSet, basename='studytext')

urlpatterns = [
    path('', include(router.urls)),
]