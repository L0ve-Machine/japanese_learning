import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.learning.models import Subject, SubjectItem, Chapter, Page

# Find the subject
subject = Subject.objects.filter(name__contains='介護').first()
if not subject:
    print("Subject not found")
    exit()

print(f'Subject: {subject.name}')
item = subject.items.first()
if not item:
    print("No items found")
    exit()

print(f'Item: {item.name}')
for chapter in item.chapters.all().order_by('order'):
    print(f'  Chapter {chapter.id}: {chapter.name} (order: {chapter.order})')
    for page in chapter.pages.all().order_by('order'):
        print(f'    - Page {page.id}: {page.name} (order: {page.order})')
