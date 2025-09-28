import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AuthProvider } from './contexts/AuthContext';
import { SubscriptionProvider } from './contexts/SubscriptionContext';
import { LanguageProvider } from './contexts/LanguageContext';
import { theme } from './styles/theme';
import Layout from './components/Layout';
import PrivateRoute from './components/PrivateRoute';
import ProtectedRoute from './components/ProtectedRoute';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import PastExams from './pages/PastExams';
import SubjectStudy from './pages/SubjectStudy';
import Vocabulary from './pages/Vocabulary';
import FlashCards from './pages/FlashCards';
import Videos from './pages/Videos';
import Subscription from './pages/Subscription';
import Profile from './pages/Profile';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,
      gcTime: 10 * 60 * 1000,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <AuthProvider>
          <LanguageProvider>
            <SubscriptionProvider>
              <Router>
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route element={<PrivateRoute />}>
                <Route element={<Layout />}>
                  <Route path="/" element={<Navigate to="/dashboard" replace />} />
                  <Route path="/dashboard" element={<Dashboard />} />
                  <Route path="/past-exams" element={
                    <ProtectedRoute requireSubscription={true}>
                      <PastExams />
                    </ProtectedRoute>
                  } />
                  <Route path="/subjects" element={
                    <ProtectedRoute requireSubscription={true}>
                      <SubjectStudy />
                    </ProtectedRoute>
                  } />
                  <Route path="/vocabulary" element={
                    <ProtectedRoute requireSubscription={true}>
                      <Vocabulary />
                    </ProtectedRoute>
                  } />
                  <Route path="/flashcards" element={
                    <ProtectedRoute requireSubscription={true}>
                      <FlashCards />
                    </ProtectedRoute>
                  } />
                  <Route path="/videos" element={
                    <ProtectedRoute requireSubscription={true}>
                      <Videos />
                    </ProtectedRoute>
                  } />
                  <Route path="/subscription" element={<Subscription />} />
                  <Route path="/profile" element={<Profile />} />
                </Route>
              </Route>
            </Routes>
              </Router>
            </SubscriptionProvider>
          </LanguageProvider>
        </AuthProvider>
      </ThemeProvider>
    </QueryClientProvider>
  );
}

export default App;