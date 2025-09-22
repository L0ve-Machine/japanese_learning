import csv
import os
from django.core.management.base import BaseCommand
from apps.learning.models import Subject, ExamSession

class Command(BaseCommand):
    help = 'Import exam subjects and sessions from CSV files'

    def handle(self, *args, **options):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

        self.stdout.write('Starting import of exam data...')

        # Import subjects
        subjects_file = os.path.join(base_dir, '過去問題2. 科目分類.csv')
        self.import_subjects(subjects_file)

        # Import exam sessions
        sessions_file = os.path.join(base_dir, '過去問題8. 年度とセッション.csv')
        self.import_sessions(sessions_file)

        self.stdout.write(self.style.SUCCESS('Successfully imported exam data'))

    def import_subjects(self, file_path):
        self.stdout.write('Importing subjects...')

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return

        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            order_map = {'A': 0, 'B': 100, 'C': 200}
            current_order = 0

            for row in reader:
                group_key = row.get('group_key', '')
                subject_key = row.get('subject_key', '')
                japanese_name = row.get('japanese_name', '')
                indonesian_name = row.get('indonesian_name', '')

                if group_key in order_map:
                    current_order = order_map[group_key]
                    order_map[group_key] += 1
                else:
                    current_order += 1

                subject, created = Subject.objects.update_or_create(
                    subject_key=subject_key,
                    defaults={
                        'group_key': group_key,
                        'name': japanese_name,
                        'indonesian_name': indonesian_name,
                        'order': current_order,
                        'is_active': True
                    }
                )

                if created:
                    self.stdout.write(f'Created subject: {japanese_name} (Group {group_key})')
                else:
                    self.stdout.write(f'Updated subject: {japanese_name} (Group {group_key})')

        self.stdout.write(self.style.SUCCESS(f'Imported {Subject.objects.count()} subjects'))

    def import_sessions(self, file_path):
        self.stdout.write('Importing exam sessions...')

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return

        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                year = int(row.get('year', 0))
                session_number = int(row.get('session_number', 0))
                available_subjects = row.get('available_subjects', '')

                if year and session_number:
                    session, created = ExamSession.objects.update_or_create(
                        year=year,
                        session_number=session_number,
                        defaults={
                            'available_subjects': available_subjects
                        }
                    )

                    if created:
                        self.stdout.write(f'Created exam session: {year}年 第{session_number}回')
                    else:
                        self.stdout.write(f'Updated exam session: {year}年 第{session_number}回')

        self.stdout.write(self.style.SUCCESS(f'Imported {ExamSession.objects.count()} exam sessions'))