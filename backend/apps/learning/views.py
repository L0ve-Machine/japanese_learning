from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from django.utils import timezone
from .models import (
    Subject, Question, Word, FlashCard, Video, StudyText,
    SubjectItem, Chapter, Page, UserProgress
)
from .serializers import (
    SubjectSerializer, QuestionSerializer, WordSerializer,
    FlashCardSerializer, VideoSerializer, StudyTextSerializer,
    SubjectDetailSerializer, SubjectItemSerializer, SubjectItemListSerializer,
    ChapterSerializer, PageSerializer, UserProgressSerializer
)

class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subject.objects.filter(is_active=True).prefetch_related(
        'items__chapters__pages__texts'
    )
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SubjectDetailSerializer
        return SubjectSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by group if specified
        group_key = self.request.query_params.get('group')
        if group_key:
            queryset = queryset.filter(group_key=group_key)

        # Search functionality
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(indonesian_name__icontains=search)
            )

        return queryset.order_by('group_key', 'order', 'name')

    @action(detail=True, methods=['get'])
    def hierarchy(self, request, pk=None):
        """Get complete hierarchical structure for a subject"""
        subject = self.get_object()
        serializer = SubjectDetailSerializer(subject)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def progress(self, request, pk=None):
        """Get user progress for this subject"""
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=401)

        subject = self.get_object()
        progress = UserProgress.objects.filter(
            user=request.user,
            subject=subject
        )
        serializer = UserProgressSerializer(progress, many=True)
        return Response(serializer.data)

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

# Hierarchical Content ViewSets
class SubjectItemViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SubjectItemListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SubjectItem.objects.filter(is_active=True)

    @action(detail=True, methods=['get'])
    def chapters(self, request, pk=None):
        """Get all chapters for this subject item"""
        item = self.get_object()
        chapters = item.chapters.filter(is_active=True)
        serializer = ChapterSerializer(chapters, many=True)
        return Response(serializer.data)

class ChapterViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ChapterSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Chapter.objects.filter(is_active=True)

    @action(detail=True, methods=['get'])
    def pages(self, request, pk=None):
        """Get all pages for this chapter"""
        chapter = self.get_object()
        pages = chapter.pages.filter(is_active=True)
        serializer = PageSerializer(pages, many=True)
        return Response(serializer.data)

class PageViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Page.objects.filter(is_active=True)

    @action(detail=True, methods=['get'])
    def texts(self, request, pk=None):
        """Get all texts for this page"""
        page = self.get_object()
        user = self.request.user

        texts = page.texts.all()
        if not user.is_premium:
            texts = texts.filter(is_premium=False)

        serializer = StudyTextSerializer(texts, many=True)
        return Response(serializer.data)

class StudyTextViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StudyTextSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = StudyText.objects.all()
        user = self.request.user

        if not user.is_premium:
            queryset = queryset.filter(is_premium=False)

        page_id = self.request.query_params.get('page')
        if page_id:
            queryset = queryset.filter(page_id=page_id)

        return queryset

class UserProgressViewSet(viewsets.ModelViewSet):
    serializer_class = UserProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProgress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'])
    def mark_completed(self, request):
        """Mark a specific content level as completed"""
        data = request.data
        user = request.user

        # Create or update progress record
        progress, created = UserProgress.objects.get_or_create(
            user=user,
            subject_id=data.get('subject_id'),
            item_id=data.get('item_id'),
            chapter_id=data.get('chapter_id'),
            page_id=data.get('page_id'),
            text_id=data.get('text_id'),
            defaults={'completed': True, 'completion_percentage': 100}
        )

        if not created:
            progress.completed = True
            progress.completion_percentage = 100
            progress.save()

        serializer = self.get_serializer(progress)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def subject_progress(self, request):
        """Get progress for a specific subject"""
        subject_id = request.query_params.get('subject_id')
        if not subject_id:
            return Response({'error': 'subject_id is required'}, status=400)

        progress = self.get_queryset().filter(subject_id=subject_id)
        serializer = self.get_serializer(progress, many=True)
        return Response(serializer.data)