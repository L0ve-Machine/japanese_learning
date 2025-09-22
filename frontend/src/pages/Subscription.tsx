import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  CircularProgress,
  Alert,
} from '@mui/material';
import { Check, Star } from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';

const Subscription: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const { user } = useAuth();

  const plans = [
    {
      id: 1,
      name: 'ベーシック',
      price: 0,
      duration: '無料',
      features: [
        '基本的な過去問題',
        '限定された科目学習',
        '基本単語帳',
        '暗記カード（100枚まで）',
      ],
    },
    {
      id: 2,
      name: 'プレミアム',
      price: 980,
      duration: '月額',
      features: [
        '全ての過去問題（5年分）',
        '全13科目の学習コンテンツ',
        '専門用語を含む全単語',
        '無制限の暗記カード',
        '全ての解説動画',
        '学習進捗の詳細分析',
        '広告なし',
      ],
      recommended: true,
    },
    {
      id: 3,
      name: 'プレミアム年間',
      price: 9800,
      duration: '年額',
      features: [
        'プレミアムの全機能',
        '2ヶ月分お得',
        '優先サポート',
      ],
    },
  ];

  const handleSubscribe = async (planId: number) => {
    setLoading(true);
    try {
      console.log('Subscribe to plan:', planId);
    } catch (error) {
      console.error('Subscription failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ textAlign: 'center', mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          プランを選択
        </Typography>
        <Typography variant="body1" color="text.secondary">
          あなたの学習目標に合わせて最適なプランをお選びください
        </Typography>
      </Box>

      {user?.is_premium && (
        <Alert severity="success" sx={{ mb: 3 }}>
          現在プレミアム会員です。有効期限: {user.subscription_end_date}
        </Alert>
      )}

      <Grid container spacing={3}>
        {plans.map((plan) => (
          <Grid item xs={12} md={4} key={plan.id}>
            <Card
              sx={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                position: 'relative',
                border: plan.recommended ? '2px solid' : '1px solid',
                borderColor: plan.recommended ? 'primary.main' : 'divider',
              }}
            >
              {plan.recommended && (
                <Box
                  sx={{
                    position: 'absolute',
                    top: -15,
                    left: '50%',
                    transform: 'translateX(-50%)',
                    bgcolor: 'primary.main',
                    color: 'white',
                    px: 2,
                    py: 0.5,
                    borderRadius: 1,
                    display: 'flex',
                    alignItems: 'center',
                    gap: 0.5,
                  }}
                >
                  <Star fontSize="small" />
                  <Typography variant="caption" fontWeight="bold">
                    おすすめ
                  </Typography>
                </Box>
              )}
              <CardContent sx={{ flexGrow: 1 }}>
                <Typography variant="h5" gutterBottom align="center" sx={{ mt: 2 }}>
                  {plan.name}
                </Typography>
                <Typography variant="h3" align="center" color="primary">
                  ¥{plan.price.toLocaleString()}
                </Typography>
                <Typography variant="body2" align="center" color="text.secondary" sx={{ mb: 3 }}>
                  {plan.duration}
                </Typography>
                <List dense>
                  {plan.features.map((feature, index) => (
                    <ListItem key={index}>
                      <ListItemIcon sx={{ minWidth: 32 }}>
                        <Check fontSize="small" color="primary" />
                      </ListItemIcon>
                      <ListItemText primary={feature} />
                    </ListItem>
                  ))}
                </List>
              </CardContent>
              <CardActions sx={{ p: 2 }}>
                {plan.price === 0 ? (
                  <Button fullWidth variant="outlined" disabled>
                    現在のプラン
                  </Button>
                ) : (
                  <Button
                    fullWidth
                    variant={plan.recommended ? 'contained' : 'outlined'}
                    onClick={() => handleSubscribe(plan.id)}
                    disabled={loading || user?.is_premium}
                  >
                    {user?.is_premium ? '加入済み' : '選択する'}
                  </Button>
                )}
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Box sx={{ mt: 4, p: 3, bgcolor: 'background.paper', borderRadius: 2 }}>
        <Typography variant="h6" gutterBottom>
          よくある質問
        </Typography>
        <Typography variant="body2" paragraph>
          Q: いつでも解約できますか？
        </Typography>
        <Typography variant="body2" color="text.secondary" paragraph>
          A: はい、いつでも解約可能です。解約後も期限まではサービスをご利用いただけます。
        </Typography>
        <Typography variant="body2" paragraph>
          Q: 支払い方法は？
        </Typography>
        <Typography variant="body2" color="text.secondary">
          A: クレジットカード（Visa, Mastercard, JCB, AMEX）がご利用いただけます。
        </Typography>
      </Box>
    </Container>
  );
};

export default Subscription;