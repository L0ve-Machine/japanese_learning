import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import axios from 'axios';
import { useAuth } from './AuthContext';

interface SubscriptionPlan {
  id: number;
  name: string;
  description: string;
  price: number;
  duration_days: number;
  features: string[];
}

interface Subscription {
  id: number;
  plan: SubscriptionPlan;
  status: 'active' | 'cancelled' | 'expired' | 'pending';
  start_date: string;
  end_date: string;
  is_active: boolean;
}

interface SubscriptionContextType {
  subscription: Subscription | null;
  loading: boolean;
  hasActiveSubscription: boolean;
  checkSubscriptionStatus: () => Promise<void>;
  requireSubscription: (callback: () => void) => void;
}

const SubscriptionContext = createContext<SubscriptionContextType | undefined>(undefined);

export const useSubscription = () => {
  const context = useContext(SubscriptionContext);
  if (!context) {
    throw new Error('useSubscription must be used within SubscriptionProvider');
  }
  return context;
};

interface SubscriptionProviderProps {
  children: ReactNode;
}

export const SubscriptionProvider: React.FC<SubscriptionProviderProps> = ({ children }) => {
  const { user, token } = useAuth();
  const [subscription, setSubscription] = useState<Subscription | null>(null);
  const [loading, setLoading] = useState(true);

  const checkSubscriptionStatus = async () => {
    if (!user || !token) {
      setSubscription(null);
      setLoading(false);
      return;
    }

    try {
      const response = await axios.get('/api/subscriptions/current/', {
        headers: { Authorization: `Bearer ${token}` }
      });

      if (response.data) {
        // サーバーサイドで is_active を計算
        const subscriptionData = {
          ...response.data,
          is_active: response.data.status === 'active' &&
                     new Date(response.data.end_date) > new Date()
        };
        setSubscription(subscriptionData);
      } else {
        setSubscription(null);
      }
    } catch (error) {
      console.error('Failed to fetch subscription status:', error);
      setSubscription(null);
    } finally {
      setLoading(false);
    }
  };

  const requireSubscription = (callback: () => void) => {
    if (!subscription || !subscription.is_active) {
      // サブスクリプションが無い場合はプラン選択ページへ
      window.location.href = '/subscription/plans';
    } else {
      callback();
    }
  };

  useEffect(() => {
    checkSubscriptionStatus();
  }, [user, token]);

  const hasActiveSubscription = subscription?.is_active || false;

  return (
    <SubscriptionContext.Provider
      value={{
        subscription,
        loading,
        hasActiveSubscription,
        checkSubscriptionStatus,
        requireSubscription
      }}
    >
      {children}
    </SubscriptionContext.Provider>
  );
};