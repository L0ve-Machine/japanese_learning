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

- **過去問題**: 過去5年分の試験問題（125問×5択）
- **科目学習**: 13科目の学習コンテンツ
- **単語帳**: 医療・介護用語の学習
- **暗記カード**: フラッシュカード形式の復習
- **解説動画**: Vimeoを使用した動画学習
- **多言語対応**: 7言語サポート（英語、ベトナム語、中国語、韓国語、タイ語、インドネシア語、ミャンマー語）
- **サブスクリプション**: Stripeを使用した課金システム

## API エンドポイント

- `/api/auth/` - 認証関連
- `/api/users/` - ユーザー管理
- `/api/learning/` - 学習コンテンツ
- `/api/subscriptions/` - サブスクリプション管理

## 管理画面

Django管理画面: http://localhost:8000/admin/
API Documentation: http://localhost:8000/api/docs/