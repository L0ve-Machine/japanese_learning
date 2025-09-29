# 🎌 Japanese Learning Platform
**介護福祉士試験対策のための日本語学習プラットフォーム**

[![Django](https://img.shields.io/badge/Django-4.2.7-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Status](https://img.shields.io/badge/Status-✅_Active-brightgreen.svg)]()

## 🌟 Features

- 📚 **過去問学習**: 介護福祉士試験の過去問題を年度・科目別に学習
- 🔐 **ユーザー認証**: emailベースの認証システム
- 💎 **サブスクリプション**: 有料プラン対応
- 🌏 **多言語対応**: 日本語⇔インドネシア語翻訳
- 📱 **レスポンシブ**: モバイル対応デザイン
- ⚡ **高速**: 最適化されたクエリとキャッシュ

## 🚀 技術スタック

- **Backend**: Django 4.2.7
- **Frontend**: HTML/CSS/JavaScript (Template-based)
- **Database**: SQLite (開発) / PostgreSQL (本番)
- **Authentication**: Django Auth + Custom User Model
- **Payment**: Stripe (予定)

## 🚀 Quick Start

### 1. プロジェクトクローン
```bash
git clone https://github.com/L0ve-Machine/japanese_learning.git
cd japanese_learning
```

### 2. 仮想環境セットアップ (推奨)
```bash
# Windows (WSL推奨)
cd backend
python -m venv venv
source venv/bin/activate  # WSL
# または
venv\Scripts\activate     # Windows CMD

# 依存関係インストール
pip install -r requirements.txt
```

### 3. データベース初期化
```bash
cd backend

# マイグレーション実行
python manage.py migrate

# 初期データ投入
python populate_learning_data.py    # 基礎データ (年度・科目)
python populate_questions.py        # 過去問データ
python create_users.py             # テストユーザー
```

### 4. サーバー起動
```bash
python manage.py runserver 8000
```

### 5. アクセス
- **メインサイト**: http://127.0.0.1:8000/
- **管理画面**: http://127.0.0.1:8000/admin/

## 👤 テストアカウント

```
📧 Email: test@test.com
🔐 Password: testpass123

📧 Email: admin@test.com
🔐 Password: adminpass123

📧 Email: premium@test.com
🔐 Password: premiumpass123
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
http://localhost:8000/quiz/2025/37/
```
> ⚠️ **重要**: `/quiz/2025/1/` は自動的に `/quiz/2025/37/` にリダイレクトされます

### 機能
- ✅ **問題表示**: 日本語問題文
- ✅ **翻訳表示**: インドネシア語翻訳（切り替え可能）
- ✅ **語彙学習**: ホバーで語彙翻訳表示
- ✅ **答え合わせ**: 正誤判定と解説表示
- ✅ **ナビゲーション**: 前の問題・次の問題移動
- ✅ **キーボード操作**: 1-5キーで選択肢選択、Enterで答え合わせ

---

## 📈 最新アップデート

### v1.2.0 (2024/09/29) 🎉
- ✅ **過去問ルーティング問題完全解決**
  - `/quiz/2025/1/` → `/quiz/2025/37/` 自動リダイレクト
  - views.pyでsession_number=1の自動処理
- ✅ **データベースエラー修正**
  - "no such table: users" 完全解決
  - マイグレーション整備完了
- ✅ **コードクリーンアップ**
  - 古い競合ファイル削除 (past-exams-data.html, past-exams-standalone.html)
  - JavaScript簡素化 (startQuiz関数直接リダイレクト)
- ✅ **安定性向上**
  - エラーハンドリング強化
  - デバッグログ追加

## 🚨 トラブルシューティング

### よくある問題と解決法

#### ❌ "no such table: users"
```bash
python manage.py migrate
```

#### ❌ 404エラー "/quiz/2025/1/"
自動リダイレクト機能が実装済みです。ブラウザキャッシュをクリアしてください。

#### ❌ ログインできない
```bash
python create_users.py  # テストユーザー再作成
```

#### ❌ 過去問データが表示されない
```bash
python populate_learning_data.py  # 基礎データ
python populate_questions.py      # 過去問データ
```

## 📂 プロジェクト構造

```
japanese_learning/
├── 📁 backend/              # Django バックエンド
│   ├── 📁 apps/            # Django アプリケーション群
│   │   ├── learning/       # 学習機能 (過去問、科目管理)
│   │   ├── web/           # メインWebアプリ (認証、ダッシュボード)
│   │   ├── users/         # ユーザー管理
│   │   ├── subscriptions/ # サブスクリプション管理
│   │   └── translations/  # 翻訳機能
│   ├── 📁 templates/       # HTMLテンプレート
│   ├── 📁 static/         # CSS/JS/画像
│   └── db.sqlite3         # SQLiteデータベース
├── 📁 frontend/            # 静的フロントエンド
├── 📄 PROJECT_STRUCTURE.md # 📘 詳細な構造説明
└── 📄 README.md           # このファイル
```

> 📘 **詳細なファイル構造は [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) をご確認ください**

---

**Made with ❤️ for Japanese learners**

*最終更新: 2024年9月29日*
*プロジェクト状態: ✅ 完全動作*