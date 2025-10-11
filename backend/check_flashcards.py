import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.learning.models import FlashcardDeck, FlashcardCard, UserFlashcardProgress

# Check flashcard decks
decks = FlashcardDeck.objects.all()
print(f"Total Flashcard Decks: {decks.count()}")
print("\nDeck Details:")
for deck in decks:
    card_count = deck.cards.count()
    print(f"  - {deck.name} ({deck.deck_type})")
    print(f"    Cards: {card_count}")
    print(f"    Premium: {deck.is_premium}")
    print(f"    Active: {deck.is_active}")
    print()

# Check total cards
total_cards = FlashcardCard.objects.count()
print(f"Total Flashcard Cards: {total_cards}")

# Check user progress
total_progress = UserFlashcardProgress.objects.count()
print(f"Total User Progress Records: {total_progress}")
