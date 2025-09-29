import pandas as pd
import json
from django.db import transaction
from .models import ExamYear, ExamSession, Subject, SubjectGroup, Question, Choice

class DataImportService:
    """CSVまたはExcelデータをインポートするサービス"""

    def __init__(self):
        self.errors = []
        self.warnings = []
        self.created_count = {
            'years': 0,
            'sessions': 0,
            'subjects': 0,
            'questions': 0,
            'choices': 0
        }

    def process_file(self, file):
        """ファイルを処理してデータを返す"""
        try:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)

            return self.validate_and_process_data(df)
        except Exception as e:
            self.errors.append(f"ファイル読み込みエラー: {str(e)}")
            return None

    def validate_and_process_data(self, df):
        """データを検証し、処理可能な形式にする"""
        required_columns = [
            'question_id', 'session', 'year', 'question_number',
            'part', 'subject_key', 'japanese_question', 'indonesian_question'
        ]

        # 必須カラムの確認
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            self.errors.append(f"必須カラムが不足しています: {', '.join(missing_columns)}")
            return None

        # データの前処理
        processed_data = []
        for index, row in df.iterrows():
            try:
                item = self.process_row(row, index + 1)
                if item:
                    processed_data.append(item)
            except Exception as e:
                self.errors.append(f"行 {index + 1}: {str(e)}")

        return processed_data

    def process_row(self, row, row_number):
        """1行のデータを処理"""
        # 必須フィールドの確認
        if pd.isna(row['question_id']) or pd.isna(row['year']) or pd.isna(row['session']):
            raise ValueError(f"必須フィールドが空です")

        # 語彙データの抽出（カラムが存在する場合）
        vocabulary = {}
        if 'vocabulary_json' in row and not pd.isna(row['vocabulary_json']):
            try:
                vocabulary = json.loads(row['vocabulary_json'])
            except json.JSONDecodeError:
                self.warnings.append(f"行 {row_number}: 語彙データのJSON形式が正しくありません")

        # 選択肢データの抽出
        choices = []
        for i in range(1, 6):  # 最大5択
            choice_col = f'choice_{i}'
            correct_col = f'choice_{i}_correct'

            if choice_col in row and not pd.isna(row[choice_col]):
                is_correct = False
                if correct_col in row:
                    is_correct = str(row[correct_col]).lower() in ['true', '1', 'yes', 'correct']

                choices.append({
                    'choice_number': i,
                    'choice_text': str(row[choice_col]),
                    'is_correct': is_correct
                })

        return {
            'question_id': str(row['question_id']),
            'year': int(row['year']),
            'session': int(row['session']),
            'question_number': int(row['question_number']),
            'part': str(row['part']),
            'subject_key': str(row['subject_key']),
            'japanese_question': str(row['japanese_question']),
            'indonesian_question': str(row['indonesian_question']),
            'explanation': str(row.get('explanation', '')),
            'vocabulary': vocabulary,
            'choices': choices
        }

    @transaction.atomic
    def import_data(self, processed_data):
        """処理済みデータをデータベースにインポート"""
        try:
            for item in processed_data:
                self.create_question_with_relationships(item)
            return True
        except Exception as e:
            self.errors.append(f"インポートエラー: {str(e)}")
            return False

    def create_question_with_relationships(self, item):
        """問題とその関連データを作成"""
        # ExamYear作成/取得
        exam_year, created = ExamYear.objects.get_or_create(
            year=item['year'],
            defaults={'is_active': True}
        )
        if created:
            self.created_count['years'] += 1

        # ExamSession作成/取得
        exam_session, created = ExamSession.objects.get_or_create(
            year=exam_year,
            session_number=item['session'],
            defaults={'name': f'第{item["session"]}回', 'is_active': True}
        )
        if created:
            self.created_count['sessions'] += 1

        # Subject作成/取得
        subject = self.get_or_create_subject(item['subject_key'], item['part'])

        # ExamSessionにSubjectを関連付け
        exam_session.subjects.add(subject)

        # Question作成/更新
        question, created = Question.objects.update_or_create(
            subject=subject,
            exam_session=exam_session,
            question_number=item['question_number'],
            defaults={
                'question_type': 'past_exam',
                'year': item['year'],
                'question_text': item['japanese_question'],
                'explanation': item['explanation'],
                'translations': {
                    'indonesian': item['indonesian_question']
                },
                'vocabulary': item['vocabulary']
            }
        )
        if created:
            self.created_count['questions'] += 1

        # 既存の選択肢を削除して新しく作成
        if not created:
            question.choices.all().delete()

        # Choice作成
        for choice_data in item['choices']:
            Choice.objects.create(
                question=question,
                choice_number=choice_data['choice_number'],
                choice_text=choice_data['choice_text'],
                is_correct=choice_data['is_correct']
            )
            self.created_count['choices'] += 1

    def get_or_create_subject(self, subject_key, part):
        """科目を作成/取得"""
        # 科目グループのマッピング
        group_mapping = {
            'A': 'human_dignity_independence',
            'B': 'development_aging',
            'C': 'care_process'
        }

        # 科目名のマッピング
        subject_mapping = {
            'human_dignity_independence': '人間の尊厳と自立',
            'care_basics': '介護の基本',
            'social_understanding': '社会の理解',
            'human_relations_communication': '人間関係とコミュニケーション',
            'communication_technology': 'コミュニケーション技術',
            'life_support_technology': '生活支援技術',
            'development_aging': '発達と老化の理解',
            'dementia_understanding': '認知症の理解',
            'disability_understanding': '障害の理解',
            'body_mind_mechanisms': 'こころとからだのしくみ',
            'medical_care_basics': '医療的ケア（基礎）',
            'care_process': '介護過程',
            'sputum_suction': '喀痰吸引',
            'tube_feeding': '経管栄養'
        }

        # SubjectGroup作成/取得
        group_key = group_mapping.get(part, 'A')
        subject_group, created = SubjectGroup.objects.get_or_create(
            group_key=group_key,
            defaults={
                'name': f'{part}グループ',
                'order': ord(part) - ord('A') + 1,
                'is_active': True
            }
        )

        # Subject作成/取得
        subject_name = subject_mapping.get(subject_key, subject_key)
        subject, created = Subject.objects.get_or_create(
            subject_key=subject_key,
            defaults={
                'name': subject_name,
                'group': subject_group,
                'order': 1,
                'is_active': True
            }
        )
        if created:
            self.created_count['subjects'] += 1

        return subject

    def get_import_summary(self):
        """インポート結果のサマリーを返す"""
        return {
            'success': len(self.errors) == 0,
            'errors': self.errors,
            'warnings': self.warnings,
            'created_count': self.created_count
        }