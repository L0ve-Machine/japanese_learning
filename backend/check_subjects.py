import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.learning.models import Subject, SubjectItem, Chapter, Page, TextBlock, QuizQuestion

subjects = Subject.objects.all()

print(f'Total subjects: {subjects.count()}\n')
print('='*60)

for s in subjects:
    items = s.items.all()
    print(f'\nSubject ID {s.id}: {s.name}')
    print(f'   Subject Key: {s.subject_key or "None"}')
    print(f'   Indonesian: {s.indonesian_name or "N/A"}')
    print(f'   Active: {s.is_active}')
    print(f'   Total Items: {items.count()}')

    for item in items:
        chapters = item.chapters.all()
        print(f'\n   -- Item: {item.name} ({chapters.count()} chapters)')

        for chapter in chapters:
            pages = chapter.pages.all()
            print(f'       -- Chapter: {chapter.name} ({pages.count()} pages)')

            for page in pages:
                text_blocks = page.text_blocks.count()
                quizzes = page.quiz_questions.count()
                print(f'           -- Page: {page.name} ({text_blocks} texts, {quizzes} quizzes)')

print('\n' + '='*60)
print('\nSummary:')
print(f'Total Subjects: {Subject.objects.count()}')
print(f'Total Items: {SubjectItem.objects.count()}')
print(f'Total Chapters: {Chapter.objects.count()}')
print(f'Total Pages: {Page.objects.count()}')
print(f'Total Text Blocks: {TextBlock.objects.count()}')
print(f'Total Quiz Questions: {QuizQuestion.objects.count()}')
