import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useSubscription } from '../contexts/SubscriptionContext';

/**
 * コンポーネント内でサブスクリプションチェックを行うカスタムフック
 */
export const useSubscriptionCheck = (requireSubscription = true) => {
  const { hasActiveSubscription, loading } = useSubscription();
  const navigate = useNavigate();

  useEffect(() => {
    if (!loading && requireSubscription && !hasActiveSubscription) {
      // サブスクリプションがない場合はプラン選択ページへリダイレクト
      navigate('/subscription/plans', {
        state: { message: 'このコンテンツにアクセスするにはプレミアムプランの登録が必要です。' }
      });
    }
  }, [hasActiveSubscription, loading, requireSubscription, navigate]);

  return { hasActiveSubscription, loading };
};