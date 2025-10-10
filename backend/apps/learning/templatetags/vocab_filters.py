import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='highlight_vocab')
def highlight_vocab(text, vocabulary):
    """
    テキスト内の単語を自動検出して、翻訳データ付きのHTMLタグで囲む

    Args:
        text: 問題文などのテキスト
        vocabulary: 単語辞書 {'単語': {'reading': '読み', 'translation': '訳'}, ...}

    Returns:
        HTMLタグが付与されたテキスト
    """
    if not vocabulary or not text:
        return text

    # 長い単語から順にソート（部分一致を防ぐため）
    sorted_words = sorted(vocabulary.keys(), key=len, reverse=True)

    # 既に処理済みの位置を記録
    processed_ranges = []
    replacements = []

    for word in sorted_words:
        vocab_data = vocabulary[word]
        reading = vocab_data.get('reading', '')
        translation = vocab_data.get('translation', '')

        # 単語を検索（エスケープしてから）
        pattern = re.escape(word)

        for match in re.finditer(pattern, text):
            start, end = match.span()

            # 既に処理済みの範囲と重複していないか確認
            overlaps = False
            for proc_start, proc_end in processed_ranges:
                if not (end <= proc_start or start >= proc_end):
                    overlaps = True
                    break

            if not overlaps:
                # HTMLタグを作成
                html_tag = f"<span class='vocab-word' data-translation='{translation}' data-reading='{reading}'>{word}</span>"
                replacements.append((start, end, html_tag))
                processed_ranges.append((start, end))

    # 位置でソート（後ろから置き換えるため）
    replacements.sort(key=lambda x: x[0], reverse=True)

    # 後ろから順に置き換え（インデックスがずれないように）
    result = text
    for start, end, html_tag in replacements:
        result = result[:start] + html_tag + result[end:]

    return mark_safe(result)


@register.filter(name='highlight_vocab_choice')
def highlight_vocab_choice(choice_text, question):
    """
    選択肢テキスト内の単語を自動検出

    Args:
        choice_text: 選択肢のテキスト
        question: Question オブジェクト

    Returns:
        HTMLタグが付与されたテキスト
    """
    if not hasattr(question, 'vocabulary') or not question.vocabulary:
        return choice_text

    return highlight_vocab(choice_text, question.vocabulary)
