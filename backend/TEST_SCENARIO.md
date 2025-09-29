# アクセス制御テストシナリオ

## 1. 未決済ユーザーのテスト

### 手順：
1. 新規ユーザー登録
2. ログイン
3. 各ページへのアクセスを試みる

### 期待される動作：

| ページ | URL | アクセス可否 | 動作 |
|-------|-----|------------|------|
| ダッシュボード | /dashboard | ✅ 可能 | 表示される |
| 過去問題 | /past-exams | ❌ 不可 | /subscription/plans へリダイレクト |
| 科目学習 | /subjects | ❌ 不可 | /subscription/plans へリダイレクト |
| 単語帳 | /vocabulary | ❌ 不可 | /subscription/plans へリダイレクト |
| 暗記カード | /flashcards | ❌ 不可 | /subscription/plans へリダイレクト |
| 解説動画 | /videos | ❌ 不可 | /subscription/plans へリダイレクト |
| プラン選択 | /subscription/plans | ✅ 可能 | 表示される |

## 2. 決済完了ユーザーのテスト

### 手順：
1. Stripe決済を完了
2. Webhookが処理される
3. 各ページへのアクセスを試みる

### 期待される動作：
- 全てのページにアクセス可能

## 3. APIエンドポイントのテスト

### 未決済ユーザーの場合：
```bash
# APIリクエスト例
curl -H "Authorization: Bearer TOKEN" http://localhost:8000/api/learning/questions/

# 期待されるレスポンス
{
  "error": "プレミアムプランの登録が必要です",
  "subscription_required": true,
  "redirect_url": "/subscription/plans/"
}
```

## 4. ミドルウェアの動作確認

### settings.pyに追加が必要：
```python
MIDDLEWARE = [
    # ... 既存のミドルウェア
    'apps.subscriptions.middleware.SubscriptionRequiredMiddleware',
]
```

## 5. 環境変数の設定確認

### 必須の環境変数：
- `STRIPE_PUBLIC_KEY`
- `STRIPE_SECRET_KEY`
- `STRIPE_WEBHOOK_SECRET`

これらが設定されていない場合、決済機能は動作しません。