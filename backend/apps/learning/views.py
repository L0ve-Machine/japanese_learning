from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from .models import Subject, Question, Word, FlashCard, Video, StudyText
from .serializers import (
    SubjectSerializer, QuestionSerializer, WordSerializer,
    FlashCardSerializer, VideoSerializer, StudyTextSerializer
)

class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subject.objects.filter(is_active=True)
    serializer_class = SubjectSerializer
    permission_classes = [AllowAny]

class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Question.objects.all()
        user = self.request.user

        if not user.is_premium:
            queryset = queryset.filter(is_premium=False)

        question_type = self.request.query_params.get('type')
        if question_type:
            queryset = queryset.filter(question_type=question_type)

        subject_id = self.request.query_params.get('subject')
        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)

        year = self.request.query_params.get('year')
        if year:
            queryset = queryset.filter(year=year)

        return queryset

    @action(detail=False, methods=['get'])
    def random(self, request):
        count = int(request.query_params.get('count', 10))
        questions = self.get_queryset().order_by('?')[:count]
        serializer = self.get_serializer(questions, many=True)
        return Response(serializer.data)

class WordViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Word.objects.all()
        user = self.request.user

        if not user.is_premium:
            queryset = queryset.filter(is_premium=False)

        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)

        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(japanese__icontains=search) |
                Q(reading__icontains=search)
            )

        return queryset

class FlashCardViewSet(viewsets.ModelViewSet):
    serializer_class = FlashCardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FlashCard.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_memorized(self, request, pk=None):
        flashcard = self.get_object()
        flashcard.is_memorized = True
        flashcard.save()
        return Response({'status': 'memorized'})

    @action(detail=True, methods=['post'])
    def review(self, request, pk=None):
        flashcard = self.get_object()
        flashcard.review_count += 1
        flashcard.last_reviewed = timezone.now()
        flashcard.save()
        return Response({'review_count': flashcard.review_count})

class VideoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Video.objects.all()
        user = self.request.user

        if not user.is_premium:
            queryset = queryset.filter(is_premium=False)

        subject_id = self.request.query_params.get('subject')
        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)

        return queryset

class StudyTextViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StudyTextSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = StudyText.objects.all()
        user = self.request.user

        if not user.is_premium:
            queryset = queryset.filter(is_premium=False)

        subject_id = self.request.query_params.get('subject')
        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)

        return queryset