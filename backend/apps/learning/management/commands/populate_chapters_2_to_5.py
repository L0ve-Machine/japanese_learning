from django.core.management.base import BaseCommand
from apps.learning.models import Subject, SubjectItem, Chapter, Page


class Command(BaseCommand):
    help = 'Create database structure for Chapters 2-5 (placeholders without content)'

    def handle(self, *args, **options):
        self.stdout.write('Creating database structure for Chapters 2-5...')

        # Get or create the hierarchy
        subject, _ = Subject.objects.get_or_create(
            name='介護試験対策',
            defaults={'indonesian_name': 'Persiapan Ujian Kaigo', 'order': 1}
        )

        item, _ = SubjectItem.objects.get_or_create(
            subject=subject,
            name='介護保険',
            defaults={'order': 1}
        )

        # Chapter 2
        chapter_2, _ = Chapter.objects.get_or_create(
            item=item,
            name='第2章',
            defaults={'description': '2. 被保険者（保険に加入する人）', 'order': 2}
        )

        page_2, created = Page.objects.get_or_create(
            chapter=chapter_2,
            name='2. 被保険者（保険に加入する人）',
            defaults={'order': 1}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created: {page_2}'))
        else:
            self.stdout.write(f'Already exists: {page_2}')

        # Chapter 3
        chapter_3, _ = Chapter.objects.get_or_create(
            item=item,
            name='第3章',
            defaults={'description': '3. 要介護認定（サービス利用までの流れ）', 'order': 3}
        )

        page_3, created = Page.objects.get_or_create(
            chapter=chapter_3,
            name='3. 要介護認定（サービス利用までの流れ）',
            defaults={'order': 1}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created: {page_3}'))
        else:
            self.stdout.write(f'Already exists: {page_3}')

        # Chapter 4
        chapter_4, _ = Chapter.objects.get_or_create(
            item=item,
            name='第4章',
            defaults={'description': '4. 介護保険のサービス', 'order': 4}
        )

        page_4, created = Page.objects.get_or_create(
            chapter=chapter_4,
            name='4. 介護保険のサービス',
            defaults={'order': 1}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created: {page_4}'))
        else:
            self.stdout.write(f'Already exists: {page_4}')

        # Chapter 5
        chapter_5, _ = Chapter.objects.get_or_create(
            item=item,
            name='第5章',
            defaults={'description': '5. 保険料と利用料', 'order': 5}
        )

        page_5, created = Page.objects.get_or_create(
            chapter=chapter_5,
            name='5. 保険料と利用料',
            defaults={'order': 1}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created: {page_5}'))
        else:
            self.stdout.write(f'Already exists: {page_5}')

        self.stdout.write(self.style.SUCCESS('\n[SUCCESS] Database structure for Chapters 2-5 created!'))
        self.stdout.write(self.style.WARNING('\n[NOTE] These chapters have NO CONTENT yet (no text blocks, vocabulary, or quizzes).'))
        self.stdout.write('Add content by creating CSV data or running content population commands.')
