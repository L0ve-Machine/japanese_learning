#!/usr/bin/env python
"""
Populate questions from actual CSV data
"""
import os
import csv
import json
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.learning.models import ExamYear, ExamSession, SubjectGroup, Subject, Question, Choice

def populate_questions():
    """Populate questions from sample_data.csv"""
    print("📝 Populating questions from sample data...")

    # Read sample data
    sample_file = 'sample_data.csv'
    if not os.path.exists(sample_file):
        print(f"❌ {sample_file} not found!")
        return

    with open(sample_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            print(f"\n📋 Processing question {row['question_number']} for year {row['year']}")

            try:
                # Get exam year
                year = int(row['year'])
                exam_year = ExamYear.objects.get(year=year)

                # Get exam session
                session_number = int(row['session'])
                exam_session = ExamSession.objects.get(
                    year=exam_year,
                    session_number=session_number
                )

                # Get subject
                subject_key = row['subject_key']
                subject = Subject.objects.get(subject_key=subject_key)

                # Parse vocabulary
                vocabulary = {}
                try:
                    if row['vocabulary_json']:
                        vocabulary = json.loads(row['vocabulary_json'])
                except (json.JSONDecodeError, KeyError):
                    vocabulary = {}

                # Create question
                question, created = Question.objects.get_or_create(
                    exam_session=exam_session,
                    subject=subject,
                    question_number=int(row['question_number']),
                    defaults={
                        'question_type': 'past_exam',
                        'year': year,
                        'question_text': row['japanese_question'],
                        'explanation': row['explanation'],
                        'translations': {
                            'id': row['indonesian_question']
                        },
                        'vocabulary': vocabulary
                    }
                )

                if created:
                    print(f"  ✅ Created question: {question.question_text[:50]}...")

                    # Add choices
                    choices_data = [
                        (1, row['choice_1'], row['choice_1_correct'] == 'TRUE'),
                        (2, row['choice_2'], row['choice_2_correct'] == 'TRUE'),
                        (3, row['choice_3'], row['choice_3_correct'] == 'TRUE'),
                        (4, row['choice_4'], row['choice_4_correct'] == 'TRUE'),
                        (5, row['choice_5'], row['choice_5_correct'] == 'TRUE'),
                    ]

                    for choice_num, choice_text, is_correct in choices_data:
                        if choice_text:  # Only add if choice text exists
                            choice, choice_created = Choice.objects.get_or_create(
                                question=question,
                                choice_number=choice_num,
                                defaults={
                                    'choice_text': choice_text,
                                    'is_correct': is_correct
                                }
                            )
                            if choice_created:
                                print(f"    ✅ Added choice {choice_num}: {choice_text[:30]}...")
                else:
                    print(f"  ⚠️  Question already exists")

            except Exception as e:
                print(f"  ❌ Error processing question: {str(e)}")

    print("\n✅ Questions population completed!")

    # Show summary
    print(f"\n📊 Summary:")
    print(f"  Total Questions: {Question.objects.count()}")
    print(f"  Total Choices: {Choice.objects.count()}")

    # Show questions by year/session
    for session in ExamSession.objects.all().order_by('-year__year', '-session_number'):
        question_count = Question.objects.filter(exam_session=session).count()
        print(f"  {session.name}: {question_count} questions")

if __name__ == '__main__':
    populate_questions()