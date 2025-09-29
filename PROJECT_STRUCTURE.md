# Japanese Learning Platform - プロジェクト構造

## 📁 プロジェクト概要
介護福祉士試験対策のための日本語学習プラットフォーム
Django (バックエンド) + HTML/CSS/JavaScript (フロントエンド)

---

## 📂 ディレクトリ構造

```
japanese_learning/
├── 📁 backend/                    # Djangoバックエンド
│   ├── 📁 apps/                   # Djangoアプリケーション群
│   │   ├── 📁 learning/           # 学習機能アプリ
│   │   ├── 📁 subscriptions/      # サブスクリプション管理
│   │   ├── 📁 translations/       # 翻訳機能
│   │   ├── 📁 users/             # ユーザー管理
│   │   └── 📁 web/               # メインWebアプリ
│   ├── 📁 core/                   # Django設定
│   ├── 📁 templates/              # HTMLテンプレート
│   ├── 📁 static/                 # 静的ファイル (CSS等)
│   ├── 📁 media/                  # アップロード画像等
│   ├── db.sqlite3                 # SQLiteデータベース
│   └── manage.py                  # Django管理スクリプト
├── 📁 frontend/                   # フロントエンド静的ファイル
├── 📁 .claude/                    # Claude設定
└── 📄 各種設定ファイル
```

---

## 🔧 Backend (Django)

### 📁 `backend/apps/` - Djangoアプリケーション

#### 📂 `apps/learning/` - 学習機能
```
learning/
├── models.py          # データモデル (ExamYear, Subject, Question, Choice等)
├── views.py           # ビュー関数
├── admin.py          # Django管理画面設定
├── migrations/        # データベースマイグレーション
└── apps.py           # アプリ設定
```
**主要機能**: 過去問データ管理、科目管理、試験年度管理

#### 📂 `apps/web/` - メインWebアプリ
```
web/
├── views.py          # メインビュー (ログイン、ダッシュボード、過去問等)
├── urls.py           # URL設定
├── decorators.py     # カスタムデコレーター (@allow_free_access等)
└── forms.py          # フォーム定義
```
**主要機能**: 認証、ダッシュボード、過去問表示、クイズ機能

#### 📂 `apps/users/` - ユーザー管理
```
users/
├── models.py         # カスタムUserモデル (email認証)
├── admin.py          # ユーザー管理画面
└── migrations/       # ユーザー関連マイグレーション
```
**主要機能**: emailベース認証、ユーザープロファイル

#### 📂 `apps/subscriptions/` - サブスクリプション
```
subscriptions/
├── models.py         # サブスクリプションプラン、支払い管理
├── views.py          # 料金プラン表示
└── migrations/       # サブスクリプション関連テーブル
```
**主要機能**: 有料プラン管理、アクセス制御

#### 📂 `apps/translations/` - 翻訳機能
```
translations/
├── models.py         # 翻訳データモデル
├── views.py          # 翻訳API
└── migrations/       # 翻訳関連テーブル
```
**主要機能**: 日本語⇔インドネシア語翻訳

### 📁 `backend/core/` - Django設定
```
core/
├── settings.py       # Django設定 (データベース、認証等)
├── urls.py          # ルートURL設定
├── wsgi.py          # WSGI設定
└── asgi.py          # ASGI設定
```

### 📁 `backend/templates/` - HTMLテンプレート
```
templates/
├── base.html             # ベーステンプレート
├── landing.html          # ランディングページ
├── dashboard.html        # ダッシュボード
├── past_exams.html       # 過去問選択ページ ⭐重要
├── quiz.html            # クイズ画面
├── registration/        # 認証関連テンプレート
│   ├── login.html       # ログイン
│   └── register.html    # 新規登録
└── admin/              # 管理画面カスタマイズ
```

### 📁 `backend/static/` - 静的ファイル
```
static/
├── css/
│   └── style.css        # メインCSS
├── js/                  # JavaScript
└── images/              # 画像ファイル
```

### 📄 データベース・設定ファイル
```
backend/
├── db.sqlite3                    # メインデータベース
├── manage.py                     # Django管理コマンド
├── requirements.txt              # Python依存関係
├── populate_learning_data.py     # 初期データ投入スクリプト
├── populate_questions.py         # 過去問データ投入
├── create_users.py              # テストユーザー作成
└── sample_data.csv              # サンプル過去問データ
```

---

## 🎨 Frontend

### 📁 `frontend/` - 静的フロントエンド
```
frontend/
├── dashboard-preview.html        # ダッシュボードプレビュー
├── landing-preview.html         # ランディングページプレビュー
└── (過去の静的ファイルは削除済み)
```

---

## 🗄️ データベース構造

### 主要テーブル
```sql
-- ユーザー関連
users               # カスタムユーザー (email認証)

-- 学習データ
learning_examyear        # 試験年度 (2023, 2024, 2025)
learning_examsession     # 試験回 (35回, 36回, 37回)
learning_subjectgroup    # 科目グループ (A,B,C)
learning_subject         # 科目 (人間の尊厳と自立, 介護の基本等)
learning_question        # 問題データ
learning_choice          # 選択肢データ

-- サブスクリプション
subscriptions_plan       # 料金プラン
subscriptions_subscription # ユーザーサブスクリプション

-- 翻訳
translations_*          # 翻訳関連テーブル
```

---

## 🚀 重要ファイル・機能

### 🔥 `backend/templates/past_exams.html`
- **機能**: 過去問年度・科目選択画面
- **重要な修正**: `/quiz/2025/1/` → `/quiz/2025/37/` 自動リダイレクト
- **JavaScript**: 簡素化されたstartQuiz()関数で直接ルーティング

### 🔥 `backend/apps/web/views.py`
- **quiz_view()**: 過去問表示メイン関数
- **重要な修正**: session_number=1の場合の自動リダイレクト処理
- **past_exams_view()**: 過去問選択画面データ提供

### 🔥 `backend/apps/learning/models.py`
- **ExamYear**: 試験年度管理
- **ExamSession**: 試験回管理
- **Subject**: 科目データ
- **Question/Choice**: 問題・選択肢データ

### 🔥 データベース初期化スクリプト
- `populate_learning_data.py`: 年度・科目・セッション基礎データ
- `populate_questions.py`: CSVから過去問データ読み込み
- `create_users.py`: テストユーザー作成

---

## 🎯 主要機能フロー

### 1. ユーザー認証
```
ランディング → ログイン/登録 → ダッシュボード
```

### 2. 過去問学習
```
ダッシュボード → 過去問選択 → 年度・科目選択 → クイズ開始
```

### 3. データフロー
```
CSV → populate_questions.py → データベース → quiz_view → テンプレート
```

---

## ⚙️ 開発・運用

### 🔧 開発サーバー起動
```bash
cd backend
python manage.py runserver 8000
```

### 🗄️ データベース操作
```bash
python manage.py migrate              # マイグレーション実行
python manage.py makemigrations       # マイグレーション作成
python manage.py createsuperuser      # 管理者作成
```

### 📊 データ投入
```bash
python populate_learning_data.py      # 基礎データ
python populate_questions.py          # 過去問データ
python create_users.py               # テストユーザー
```

---

## 🔍 トラブルシューティング

### よくある問題
1. **"no such table: users"** → `python manage.py migrate`
2. **404エラー /quiz/2025/1/** → views.pyで自動リダイレクト済み
3. **ログインできない** → `python create_users.py`でテストユーザー作成

### テストアカウント
```
admin@test.com / adminpass123
test@test.com / testpass123
premium@test.com / premiumpass123
```

---

## 📝 最近の重要な修正 (2024/09/29)

1. **過去問ルーティング問題解決**: `/quiz/2025/1/` → `/quiz/2025/37/` 自動リダイレクト
2. **データベースエラー解決**: "no such table: users"完全修正
3. **古いファイル削除**: 競合していた静的ファイル削除
4. **JavaScript簡素化**: 直接リダイレクト方式採用

---

*最終更新: 2024年9月29日*
*プロジェクト状態: ✅ 完全動作*