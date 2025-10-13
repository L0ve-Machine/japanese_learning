import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.learning.models import Question
from apps.learning.templatetags.vocab_filters import highlight_vocab

# 問題を取得
question = Question.objects.first()

print("=== 単語自動検出システムのテスト ===\n")

print("1. 元の問題文（プレーンテキスト）:")
print(f"   {question.question_text}\n")

print("2. vocabulary フィールド（最初の5個）:")
vocab_items = list(question.vocabulary.items())[:5]
for word, data in vocab_items:
    print(f"   {word}: {data['translation']} ({data['reading']})")
print(f"   ... 他 {len(question.vocabulary) - 5}個\n")

print("3. フィルター適用後（HTMLタグ付き）:")
highlighted = highlight_vocab(question.question_text, question.vocabulary)
print(f"   {highlighted[:200]}...\n")

print("4. 選択肢1の例:")
choice = question.choices.first()
print(f"   元のテキスト: {choice.choice_text}")
highlighted_choice = highlight_vocab(choice.choice_text, question.vocabulary)
print(f"   フィルター適用後: {highlighted_choice}\n")

print("=== 仕組み ===")
print("1. 問題作成時:")
print("   - 問題文: プレーンテキストで保存")
print("   - vocabulary: 翻訳対象の単語リストを保存")
print()
print("2. 表示時:")
print("   - テンプレートフィルター highlight_vocab が自動実行")
print("   - vocabulary内の単語を問題文から検索")
print("   - 見つかった単語を <span class='vocab-word'> で囲む")
print("   - data-translation と data-reading を自動付与")
print()
print("3. ユーザー体験:")
print("   - 単語をクリック/ホバーで翻訳表示")
print("   - 問題文はシンプルに管理できる")
print("   - vocabulary に単語を追加するだけで自動反映")
