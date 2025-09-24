from django.core.management.base import BaseCommand
from apps.learning.models import Subject, SubjectItem, Chapter, Page, StudyText


class Command(BaseCommand):
    help = 'Create sample subject data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample subject data...')

        # Single sample subject - content to be added later
        subjects_data = [
            {
                'subject_key': 'kaigo_kihon',
                'group_key': 'A',
                'name': '介護の基本',
                'indonesian_name': 'Dasar-dasar Perawatan',
                'description': '介護職の役割と専門性について学習します',
                'order': 1,
                'items': []  # Empty for now - content will be added later
            }
        ]

        # Create subjects and their hierarchy
        for subject_data in subjects_data:
            # Create or get subject
            subject, created = Subject.objects.get_or_create(
                subject_key=subject_data['subject_key'],
                defaults={
                    'name': subject_data['name'],
                    'indonesian_name': subject_data.get('indonesian_name'),
                    'group_key': subject_data['group_key'],
                    'description': subject_data['description'],
                    'order': subject_data['order'],
                    'is_active': True
                }
            )

            if created:
                self.stdout.write(f'Created subject: {subject.name}')
            else:
                self.stdout.write(f'Subject already exists: {subject.name}')

            # Create items
            for item_data in subject_data.get('items', []):
                item, created = SubjectItem.objects.get_or_create(
                    subject=subject,
                    name=item_data['name'],
                    defaults={
                        'description': item_data['description'],
                        'order': item_data['order'],
                        'is_active': True
                    }
                )

                if created:
                    self.stdout.write(f'  Created item: {item.name}')

                # Create chapters
                for chapter_data in item_data.get('chapters', []):
                    chapter, created = Chapter.objects.get_or_create(
                        item=item,
                        name=chapter_data['name'],
                        defaults={
                            'description': chapter_data['description'],
                            'order': chapter_data['order'],
                            'is_active': True
                        }
                    )

                    if created:
                        self.stdout.write(f'    Created chapter: {chapter.name}')

                    # Create pages
                    for page_data in chapter_data.get('pages', []):
                        page, created = Page.objects.get_or_create(
                            chapter=chapter,
                            name=page_data['name'],
                            defaults={
                                'description': page_data['description'],
                                'order': page_data['order'],
                                'is_active': True
                            }
                        )

                        if created:
                            self.stdout.write(f'      Created page: {page.name}')

                        # Create texts
                        for text_data in page_data.get('texts', []):
                            text, created = StudyText.objects.get_or_create(
                                page=page,
                                title=text_data['title'],
                                defaults={
                                    'content': text_data['content'],
                                    'translations': text_data.get('translations', {}),
                                    'order': text_data['order'],
                                    'is_premium': text_data.get('is_premium', False)
                                }
                            )

                            if created:
                                self.stdout.write(f'        Created text: {text.title}')

        self.stdout.write(
            self.style.SUCCESS('Successfully created sample subject data!')
        )