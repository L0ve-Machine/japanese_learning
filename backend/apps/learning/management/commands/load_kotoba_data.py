import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from apps.learning.models import (
    KotobaCategory, KotobaSubcategory, KotobaWord,
    KotobaExample, KotobaVocabulary
)


class Command(BaseCommand):
    help = 'Load Kotoba data from JSON files into database'

    def handle(self, *args, **options):
        data_dir = os.path.join(settings.BASE_DIR, 'data', 'ことば', 'New folder')

        self.stdout.write(self.style.WARNING('Clearing existing Kotoba data...'))
        # Clear existing data in reverse order of dependencies
        KotobaVocabulary.objects.all().delete()
        KotobaExample.objects.all().delete()
        KotobaWord.objects.all().delete()
        KotobaSubcategory.objects.all().delete()
        KotobaCategory.objects.all().delete()

        # Load categories
        self.stdout.write('Loading categories...')
        categories_file = os.path.join(data_dir, 'ことば２.メインカテゴリー.json')
        with open(categories_file, 'r', encoding='utf-8') as f:
            categories_data = json.load(f)
            for item in categories_data:
                KotobaCategory.objects.create(
                    category_key=item['category_key'],
                    japanese_name=item['japanese_name'],
                    indonesian_translation=item['indonesian_translation'],
                    ruby_reading=item['ruby_reading'],
                    order_number=int(item['order_number'])
                )
        self.stdout.write(self.style.SUCCESS(f'Loaded {len(categories_data)} categories'))

        # Load subcategories
        self.stdout.write('Loading subcategories...')
        subcategories_file = os.path.join(data_dir, 'ことば3. サブカテゴリー.json')
        with open(subcategories_file, 'r', encoding='utf-8') as f:
            subcategories_data = json.load(f)
            for item in subcategories_data:
                category = KotobaCategory.objects.get(category_key=item['main_category_key'])
                KotobaSubcategory.objects.create(
                    main_category=category,
                    subcategory_key=item['subcategory_key'],
                    japanese_name=item['japanese_name'],
                    indonesian_translation=item['indonesian_translation'],
                    ruby_reading=item['ruby_reading'],
                    order_number=int(item['order_number'])
                )
        self.stdout.write(self.style.SUCCESS(f'Loaded {len(subcategories_data)} subcategories'))

        # Load words
        self.stdout.write('Loading words...')
        words_file = os.path.join(data_dir, 'ことば4. 単語データ.json')
        with open(words_file, 'r', encoding='utf-8') as f:
            words_data = json.load(f)
            for item in words_data:
                category = KotobaCategory.objects.get(category_key=item['main_category_key'])
                subcategory = KotobaSubcategory.objects.get(
                    main_category=category,
                    subcategory_key=item['subcategory_key']
                )
                KotobaWord.objects.create(
                    word_id=item['word_id'],
                    main_category=category,
                    subcategory=subcategory,
                    japanese_word=item['japanese_word'],
                    ruby_reading=item['ruby_reading'],
                    indonesian_translation=item['indonesian_translation']
                )
        self.stdout.write(self.style.SUCCESS(f'Loaded {len(words_data)} words'))

        # Load examples
        self.stdout.write('Loading examples...')
        examples_file = os.path.join(data_dir, 'ことば5. 例文データ.json')
        with open(examples_file, 'r', encoding='utf-8') as f:
            examples_data = json.load(f)
            for item in examples_data:
                word = KotobaWord.objects.get(word_id=item['word_id'])
                KotobaExample.objects.create(
                    example_id=item['example_id'],
                    word=word,
                    japanese_example=item['japanese_example'],
                    indonesian_example=item['indonesian_example'],
                    order_number=int(item['order_number'])
                )
        self.stdout.write(self.style.SUCCESS(f'Loaded {len(examples_data)} examples'))

        # Load vocabulary
        self.stdout.write('Loading vocabulary...')
        vocabulary_file = os.path.join(data_dir, 'ことば6. 語彙データ.json')
        with open(vocabulary_file, 'r', encoding='utf-8') as f:
            vocabulary_data = json.load(f)
            for item in vocabulary_data:
                example = KotobaExample.objects.get(example_id=item['example_id'])
                KotobaVocabulary.objects.create(
                    vocabulary_id=item['vocabulary_id'],
                    example=example,
                    japanese_word=item['japanese_word'],
                    ruby_reading=item['ruby_reading'],
                    indonesian_translation=item['indonesian_translation']
                )
        self.stdout.write(self.style.SUCCESS(f'Loaded {len(vocabulary_data)} vocabulary items'))

        self.stdout.write(self.style.SUCCESS('Successfully loaded all Kotoba data!'))