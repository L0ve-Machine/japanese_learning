"""
Management command to load Kotoba data into Flashcard decks
Creates one deck per subcategory with all words and examples
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.learning.models import (
    KotobaCategory, KotobaSubcategory, KotobaWord, KotobaExample,
    FlashcardDeck, FlashcardCard
)
import csv
import os
from django.conf import settings


class Command(BaseCommand):
    help = 'Load Kotoba data into Flashcard decks'

    def handle(self, *args, **options):
        self.stdout.write('Starting flashcard data import...')

        # Get all main categories
        categories = KotobaCategory.objects.all().order_by('order_number')

        deck_count = 0
        card_count = 0

        with transaction.atomic():
            for category in categories:
                # Create ONE deck for this main category
                deck_name = category.japanese_name

                # Determine deck type based on main category
                deck_type_map = {
                    'care_study': 'caregiving',
                    'work': 'vocabulary',
                    'conversation': 'vocabulary',
                    'songs_anime': 'vocabulary',
                    'casual_language': 'vocabulary',
                    'n2_study': 'grammar',
                    'n3_study': 'grammar',
                }

                deck_type = deck_type_map.get(
                    category.category_key,
                    'vocabulary'
                )

                # Check if deck already exists
                deck, created = FlashcardDeck.objects.get_or_create(
                    name=deck_name,
                    defaults={
                        'deck_type': deck_type,
                        'description': category.indonesian_translation,
                        'is_premium': False,
                        'is_active': True,
                        'order': category.order_number
                    }
                )

                if created:
                    deck_count += 1
                    self.stdout.write(f'  Created deck: {deck_name}')
                else:
                    self.stdout.write(f'  Deck already exists: {deck_name}')
                    # Clear existing cards for reimport
                    FlashcardCard.objects.filter(deck=deck).delete()

                # Get all words in this main category (across ALL subcategories)
                words = KotobaWord.objects.filter(
                    main_category=category
                ).select_related('subcategory').prefetch_related('examples').order_by('subcategory__order_number', 'japanese_word')

                # Create flashcard for each word
                card_order = 0
                for word in words:
                    # Get all examples for this word
                    examples = word.examples.all().order_by('order_number')

                    if examples.exists():
                        # Combine all examples into back text
                        example_texts = []
                        for ex in examples:
                            example_texts.append(
                                f"• {ex.japanese_example}\n  {ex.indonesian_example}"
                            )

                        example_text = "\n\n".join(example_texts)
                    else:
                        example_text = ""

                    # Create flashcard
                    card = FlashcardCard.objects.create(
                        deck=deck,
                        front_text=word.japanese_word,
                        back_text=word.indonesian_translation,
                        front_reading=word.ruby_reading,
                        example_sentence=example_text,
                        example_translation="",  # Already included in example_sentence
                        notes=f"{word.subcategory.japanese_name}",  # Just the subcategory name
                        order=card_order
                    )

                    card_order += 1
                    card_count += 1

                self.stdout.write(f'    Added {card_order} cards to deck')

        self.stdout.write(
            self.style.SUCCESS(
                f'\nImport complete!\n'
                f'  Decks created/updated: {deck_count}\n'
                f'  Total cards: {card_count}'
            )
        )