from django.core.management.base import BaseCommand
from apps.learning.models import Subject, SubjectItem, Chapter, Page


class Command(BaseCommand):
    help = 'Create database structure for all subjects (準備中 - empty placeholders)'

    def handle(self, *args, **options):
        self.stdout.write('Creating all subjects structure...\n')

        # Subject 1: 介護試験対策 (already exists, but ensure it's there)
        subject_1, created = Subject.objects.get_or_create(
            name='介護試験対策',
            defaults={
                'indonesian_name': 'Persiapan Ujian Kaigo',
                'order': 1,
                'is_active': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created Subject: {subject_1.name}'))
        else:
            self.stdout.write(f'Already exists: {subject_1.name}')

        # Subject 2: 介護の実務会話
        subject_2, created = Subject.objects.get_or_create(
            name='介護の実務会話',
            defaults={
                'indonesian_name': 'Percakapan Praktis Kaigo',
                'order': 2,
                'is_active': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created Subject: {subject_2.name}'))
        else:
            self.stdout.write(f'Already exists: {subject_2.name}')

        # Subject 3: 日本人と会話
        subject_3, created = Subject.objects.get_or_create(
            name='日本人と会話',
            defaults={
                'indonesian_name': 'Percakapan dengan Orang Jepang',
                'order': 3,
                'is_active': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created Subject: {subject_3.name}'))
        else:
            self.stdout.write(f'Already exists: {subject_3.name}')

        # Subject 4: 特定技能評価試験
        subject_4, created = Subject.objects.get_or_create(
            name='特定技能評価試験',
            defaults={
                'indonesian_name': 'Ujian Evaluasi Keterampilan Khusus',
                'order': 4,
                'is_active': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created Subject: {subject_4.name}'))
        else:
            self.stdout.write(f'Already exists: {subject_4.name}')

        # Subject 5: 日本の生活マナー
        subject_5, created = Subject.objects.get_or_create(
            name='日本の生活マナー',
            defaults={
                'indonesian_name': 'Etiket Kehidupan di Jepang',
                'order': 5,
                'is_active': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created Subject: {subject_5.name}'))
        else:
            self.stdout.write(f'Already exists: {subject_5.name}')

        self.stdout.write('\n' + '='*50)
        self.stdout.write('Creating Items (with 準備中 placeholder pages)...\n')

        # Items for Subject 2: 介護の実務会話
        items_2 = [
            ('先輩との会話', 'Percakapan dengan Senior'),
            ('介護分野', 'Bidang Perawatan'),
            ('緊急時の報告', 'Laporan Darurat'),
        ]
        for idx, (name, indo_name) in enumerate(items_2, 1):
            item, created = SubjectItem.objects.get_or_create(
                subject=subject_2,
                name=name,
                defaults={'order': idx, 'is_active': True}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  Created Item: {name}'))

                # Create a placeholder chapter and page
                chapter, _ = Chapter.objects.get_or_create(
                    item=item,
                    name='第1章',
                    defaults={'description': '準備中', 'order': 1}
                )
                Page.objects.get_or_create(
                    chapter=chapter,
                    name=f'{name} - 準備中',
                    defaults={'order': 1}
                )
            else:
                self.stdout.write(f'  Already exists: {name}')

        # Items for Subject 3: 日本人と会話
        items_3 = [
            ('趣味を聞く', 'Menanyakan Hobi'),
            ('食事に誘う', 'Mengajak Makan'),
        ]
        for idx, (name, indo_name) in enumerate(items_3, 1):
            item, created = SubjectItem.objects.get_or_create(
                subject=subject_3,
                name=name,
                defaults={'order': idx, 'is_active': True}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  Created Item: {name}'))

                chapter, _ = Chapter.objects.get_or_create(
                    item=item,
                    name='第1章',
                    defaults={'description': '準備中', 'order': 1}
                )
                Page.objects.get_or_create(
                    chapter=chapter,
                    name=f'{name} - 準備中',
                    defaults={'order': 1}
                )
            else:
                self.stdout.write(f'  Already exists: {name}')

        # Items for Subject 4: 特定技能評価試験
        items_4 = [
            ('飲食料品製造業分野', 'Bidang Manufaktur Makanan dan Minuman'),
        ]
        for idx, (name, indo_name) in enumerate(items_4, 1):
            item, created = SubjectItem.objects.get_or_create(
                subject=subject_4,
                name=name,
                defaults={'order': idx, 'is_active': True}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  Created Item: {name}'))

                chapter, _ = Chapter.objects.get_or_create(
                    item=item,
                    name='第1章',
                    defaults={'description': '準備中', 'order': 1}
                )
                Page.objects.get_or_create(
                    chapter=chapter,
                    name=f'{name} - 準備中',
                    defaults={'order': 1}
                )
            else:
                self.stdout.write(f'  Already exists: {name}')

        # Items for Subject 5: 日本の生活マナー
        items_5 = [
            ('ごみの分別', 'Pemilahan Sampah'),
            ('公共交通機関の利用', 'Penggunaan Transportasi Umum'),
        ]
        for idx, (name, indo_name) in enumerate(items_5, 1):
            item, created = SubjectItem.objects.get_or_create(
                subject=subject_5,
                name=name,
                defaults={'order': idx, 'is_active': True}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  Created Item: {name}'))

                chapter, _ = Chapter.objects.get_or_create(
                    item=item,
                    name='第1章',
                    defaults={'description': '準備中', 'order': 1}
                )
                Page.objects.get_or_create(
                    chapter=chapter,
                    name=f'{name} - 準備中',
                    defaults={'order': 1}
                )
            else:
                self.stdout.write(f'  Already exists: {name}')

        self.stdout.write('\n' + self.style.SUCCESS('[SUCCESS] All subjects structure created!'))
        self.stdout.write(self.style.WARNING('[NOTE] All new items have NO CONTENT yet (準備中).'))
        self.stdout.write('You can now add content through the Django admin panel.')

        # Summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write('SUMMARY:')
        total_subjects = Subject.objects.count()
        total_items = SubjectItem.objects.count()
        total_chapters = Chapter.objects.count()
        total_pages = Page.objects.count()
        self.stdout.write(f'  Total Subjects: {total_subjects}')
        self.stdout.write(f'  Total Items: {total_items}')
        self.stdout.write(f'  Total Chapters: {total_chapters}')
        self.stdout.write(f'  Total Pages: {total_pages}')
