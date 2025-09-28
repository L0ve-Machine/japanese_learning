import os
from typing import Optional
from django.conf import settings

# 翻訳用の辞書（簡易実装）
TRANSLATION_DICT = {
    'ja_to_en': {
        '介護': 'caregiving',
        '福祉': 'welfare',
        '試験': 'exam',
        '学習': 'learning',
        '問題': 'question',
        '解答': 'answer',
        '科目': 'subject',
        '単語': 'vocabulary',
        'ダッシュボード': 'Dashboard',
        '過去問題': 'Past Exams',
        '科目学習': 'Subject Study',
        '単語帳': 'Vocabulary',
        '暗記カード': 'Flashcards',
        '解説動画': 'Videos',
    },
    'ja_to_vi': {
        '介護': 'chăm sóc',
        '福祉': 'phúc lợi',
        '試験': 'kỳ thi',
        '学習': 'học tập',
        '問題': 'câu hỏi',
        '解答': 'câu trả lời',
        '科目': 'môn học',
        '単語': 'từ vựng',
    },
    'ja_to_id': {
        '介護': 'perawatan',
        '福祉': 'kesejahteraan',
        '試験': 'ujian',
        '学習': 'pembelajaran',
        '問題': 'pertanyaan',
        '解答': 'jawaban',
        '科目': 'mata pelajaran',
        '単語': 'kosakata',
    },
    'ja_to_zh': {
        '介護': '护理',
        '福祉': '福利',
        '試験': '考试',
        '学習': '学习',
        '問題': '问题',
        '解答': '答案',
        '科目': '科目',
        '単語': '词汇',
    },
    'ja_to_ko': {
        '介護': '간호',
        '福祉': '복지',
        '試験': '시험',
        '学習': '학습',
        '問題': '문제',
        '解答': '답변',
        '科目': '과목',
        '単語': '단어',
    },
    'ja_to_th': {
        '介護': 'การดูแล',
        '福祉': 'สวัสดิการ',
        '試験': 'การสอบ',
        '学習': 'การเรียนรู้',
        '問題': 'คำถาม',
        '解答': 'คำตอบ',
        '科目': 'วิชา',
        '単語': 'คำศัพท์',
    },
    'ja_to_my': {
        '介護': 'စောင့်ရှောက်မှု',
        '福祉': 'သက်သာချောင်ချိရေး',
        '試験': 'စာမေးပွဲ',
        '学習': 'သင်ယူမှု',
        '問題': 'မေးခွန်း',
        '解答': 'အဖြေ',
        '科目': 'ဘာသာရပ်',
        '単語': 'ဝေါဟာရ',
    }
}

class TranslationService:
    """翻訳サービス"""

    def __init__(self):
        # Google翻訳APIキー（将来の実装用）
        self.google_api_key = getattr(settings, 'GOOGLE_TRANSLATE_API_KEY', None)
        # DeepL APIキー（将来の実装用）
        self.deepl_api_key = getattr(settings, 'DEEPL_API_KEY', None)

    def translate(self, text: str, source_lang: str = 'ja', target_lang: str = 'en') -> str:
        """
        テキストを翻訳
        現在は簡易辞書による翻訳のみ実装
        将来的にはGoogle翻訳APIやDeepL APIを使用
        """
        if source_lang == target_lang:
            return text

        # 簡易辞書による翻訳
        dict_key = f'{source_lang}_to_{target_lang}'
        if dict_key in TRANSLATION_DICT:
            translation_dict = TRANSLATION_DICT[dict_key]

            # 完全一致を探す
            if text in translation_dict:
                return translation_dict[text]

            # 部分的な翻訳を試みる
            translated_text = text
            for ja_word, translated_word in translation_dict.items():
                translated_text = translated_text.replace(ja_word, translated_word)

            if translated_text != text:
                return translated_text

        # 将来的にはここで外部APIを呼び出す
        # if self.google_api_key:
        #     return self._translate_with_google(text, source_lang, target_lang)
        # elif self.deepl_api_key:
        #     return self._translate_with_deepl(text, source_lang, target_lang)

        # 翻訳できない場合は元のテキストを返す
        return f"[{target_lang.upper()}] {text}"

    def _translate_with_google(self, text: str, source_lang: str, target_lang: str) -> str:
        """Google翻訳APIを使用した翻訳（未実装）"""
        # TODO: Google Translate API実装
        pass

    def _translate_with_deepl(self, text: str, source_lang: str, target_lang: str) -> str:
        """DeepL APIを使用した翻訳（未実装）"""
        # TODO: DeepL API実装
        pass

    def detect_language(self, text: str) -> str:
        """言語を検出"""
        # 簡易実装: 日本語文字が含まれているかチェック
        japanese_chars = set('あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽ')
        if any(char in japanese_chars for char in text):
            return 'ja'

        # アルファベットのみの場合は英語と判定
        if all(char.isalpha() or char.isspace() for char in text):
            return 'en'

        return 'unknown'