import React, { useEffect } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { CircularProgress, Box, Alert } from '@mui/material';
import { useAuth } from '../contexts/AuthContext';
import { useSubscription } from '../contexts/SubscriptionContext';

interface ProtectedRouteProps {
  children: React.ReactNode;
  requireSubscription?: boolean;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  children,
  requireSubscription = false
}) => {
  const { user, loading: authLoading } = useAuth();
  const { hasActiveSubscription, loading: subLoading } = useSubscription();
  const location = useLocation();

  // ローディング中の表示
  if (authLoading || (requireSubscription && subLoading)) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
        <CircularProgress />
      </Box>
    );
  }

  // 未認証の場合はログインページへ
  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // サブスクリプションが必要な場合のチェック
  if (requireSubscription && !hasActiveSubscription) {
    return (
      <Box p={3}>
        <Alert severity="warning">
          このコンテンツにアクセスするにはプレミアムプランの登録が必要です。
        </Alert>
        <Box mt={2}>
          <Navigate to="/subscription/plans" replace />
        </Box>
      </Box>
    );
  }

  return <>{children}</>;
};

export default ProtectedRoute;