import React from 'react';
import { Box, Card, CardContent, Typography, Button, Alert } from '@mui/material';
import { Lock } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useSubscription } from '../contexts/SubscriptionContext';

interface SubscriptionGateProps {
  children: React.ReactNode;
  fallbackMessage?: string;
}

/**
 * サブスクリプションが必要なコンテンツをラップするコンポーネント
 * サブスクリプションがない場合は、プラン選択を促すUIを表示
 */
const SubscriptionGate: React.FC<SubscriptionGateProps> = ({
  children,
  fallbackMessage = 'このコンテンツを閲覧するにはプレミアムプランへの登録が必要です。'
}) => {
  const { hasActiveSubscription, loading } = useSubscription();
  const navigate = useNavigate();

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <Typography>読み込み中...</Typography>
      </Box>
    );
  }

  if (!hasActiveSubscription) {
    return (
      <Box p={3}>
        <Card sx={{ maxWidth: 600, mx: 'auto', mt: 4 }}>
          <CardContent sx={{ textAlign: 'center', py: 4 }}>
            <Lock sx={{ fontSize: 60, color: 'text.secondary', mb: 2 }} />
            <Typography variant="h5" gutterBottom>
              プレミアムコンテンツ
            </Typography>
            <Typography variant="body1" color="text.secondary" paragraph>
              {fallbackMessage}
            </Typography>
            <Alert severity="info" sx={{ mb: 3 }}>
              プレミアムプランに登録すると、以下の機能が利用できます：
              <ul style={{ textAlign: 'left', marginTop: '8px' }}>
                <li>過去5年分の試験問題（625問）</li>
                <li>13科目の詳細な学習コンテンツ</li>
                <li>医療・介護用語の単語帳</li>
                <li>暗記カード機能</li>
                <li>解説動画の視聴</li>
                <li>7言語での翻訳サポート</li>
              </ul>
            </Alert>
            <Button
              variant="contained"
              color="primary"
              size="large"
              onClick={() => navigate('/subscription/plans')}
            >
              プランを見る
            </Button>
          </CardContent>
        </Card>
      </Box>
    );
  }

  return <>{children}</>;
};

export default SubscriptionGate;