# 外国人向け日本語学習WEBアプリ

介護資格取得を目指す外国人向けの日本語学習プラットフォーム

## 技術スタック

- **Backend**: Django 4.2 + Django REST Framework
- **Frontend**: React 18 + TypeScript + Material-UI
- **Database**: PostgreSQL
- **Payment**: Stripe

## セットアップ

### Backend

1. Python仮想環境を作成
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

2. 依存関係をインストール
```bash
pip install -r requirements.txt
```

3. 環境変数を設定
```bash
cp .env.example .env
# .envファイルを編集して必要な設定を追加
```

4. データベースをセットアップ
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

5. サーバーを起動
```bash
python manage.py runserver
```

### Frontend

1. 依存関係をインストール
```bash
cd frontend
npm install
```

2. 開発サーバーを起動
```bash
npm start
```

## 機能一覧

### 🎯 学習機能
- **過去問題**: 過去問題のクイズ形式練習
- **語彙学習**: ホバー翻訳機能付き単語学習
- **インドネシア語翻訳**: 問題文の翻訳表示機能
- **科目学習**: 13科目の学習コンテンツ
- **単語帳**: 医療・介護用語の学習
- **暗記カード**: フラッシュカード形式の復習
- **解説動画**: Vimeoを使用した動画学習

### 🔧 管理機能
- **CSV/Excelインポート**: ワンクリックでデータ一括登録
- **テンプレートダウンロード**: 正しいフォーマットのCSVテンプレート
- **自動関係構築**: 年度・セッション・科目の自動生成
- **Django Admin**: カスタム管理画面

### 🌐 システム機能
- **多言語対応**: 7言語サポート（英語、ベトナム語、中国語、韓国語、タイ語、インドネシア語、ミャンマー語）
- **サブスクリプション**: Stripeを使用した課金システム

## API エンドポイント

- `/api/auth/` - 認証関連
- `/api/users/` - ユーザー管理
- `/api/learning/` - 学習コンテンツ
- `/api/subscriptions/` - サブスクリプション管理

## 管理画面

- **標準Django管理画面**: http://localhost:8000/admin/
- **学習データ管理**: http://localhost:8000/learning-admin/
- **データインポート**: http://localhost:8000/learning-admin/import-data/
- **CSVテンプレート**: http://localhost:8000/learning-admin/download-template/
- **API Documentation**: http://localhost:8000/api/docs/

## 新機能：データインポートシステム 🚀

### CSV/Excelファイルからワンクリックで問題データを一括登録！

#### 使用方法
1. **管理画面にアクセス**: http://localhost:8000/learning-admin/
2. **データインポートページ**: http://localhost:8000/learning-admin/import-data/
3. **CSVテンプレートをダウンロード**して正しいフォーマットを確認
4. **データを入力**してCSVまたはExcelファイルを作成
5. **ファイルをアップロード**してインポート実行

#### 対応データ形式
- CSV (.csv)
- Excel (.xlsx, .xls)

#### 自動生成される項目
- ExamYear (年度)
- ExamSession (セッション)
- SubjectGroup (科目グループ)
- Subject (科目)
- Question (問題)
- Choice (選択肢)

## クイズ機能

### アクセス方法
```
http://localhost:8000/quiz/2025/1/
```

### 機能
- ✅ **問題表示**: 日本語問題文
- ✅ **翻訳表示**: インドネシア語翻訳（切り替え可能）
- ✅ **語彙学習**: ホバーで語彙翻訳表示
- ✅ **答え合わせ**: 正誤判定と解説表示
- ✅ **ナビゲーション**: 前の問題・次の問題移動
- ✅ **キーボード操作**: 1-5キーで選択肢選択、Enterで答え合わせ