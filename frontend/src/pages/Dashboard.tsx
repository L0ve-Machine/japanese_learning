import React from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  CardActions,
  Button,
  LinearProgress,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import {
  Assignment,
  School,
  Translate,
  Quiz,
  VideoLibrary,
  TrendingUp,
} from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

  const features = [
    {
      title: '過去問題',
      description: '過去5年分の問題を練習',
      icon: <Assignment sx={{ fontSize: 40 }} />,
      path: '/past-exams',
      color: '#4CAF50',
    },
    {
      title: '科目学習',
      description: '13科目から学習',
      icon: <School sx={{ fontSize: 40 }} />,
      path: '/subjects',
      color: '#2196F3',
    },
    {
      title: 'ことば',
      description: '重要単語を学習',
      icon: <Translate sx={{ fontSize: 40 }} />,
      path: '/vocabulary',
      color: '#FF9800',
    },
    {
      title: '暗記カード',
      description: 'フラッシュカードで復習',
      icon: <Quiz sx={{ fontSize: 40 }} />,
      path: '/flashcards',
      color: '#9C27B0',
    },
    {
      title: '解説動画',
      description: '動画で詳しく学習',
      icon: <VideoLibrary sx={{ fontSize: 40 }} />,
      path: '/videos',
      color: '#F44336',
    },
    {
      title: '学習進捗',
      description: '進捗状況を確認',
      icon: <TrendingUp sx={{ fontSize: 40 }} />,
      path: '/dashboard',
      color: '#00BCD4',
    },
  ];

  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          こんにちは、{user?.email}さん
        </Typography>
        <Typography variant="body1" color="text.secondary">
          今日も頑張りましょう！
        </Typography>
      </Box>

      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography color="text.secondary" gutterBottom>
              今週の学習時間
            </Typography>
            <Typography variant="h4">12時間</Typography>
            <LinearProgress variant="determinate" value={60} sx={{ mt: 2 }} />
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography color="text.secondary" gutterBottom>
              完了した問題
            </Typography>
            <Typography variant="h4">234問</Typography>
            <LinearProgress variant="determinate" value={45} sx={{ mt: 2 }} />
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography color="text.secondary" gutterBottom>
              正答率
            </Typography>
            <Typography variant="h4">78%</Typography>
            <LinearProgress variant="determinate" value={78} sx={{ mt: 2 }} />
          </Paper>
        </Grid>
      </Grid>

      <Typography variant="h5" gutterBottom sx={{ mb: 2 }}>
        学習メニュー
      </Typography>
      <Grid container spacing={3}>
        {features.map((feature) => (
          <Grid item xs={12} sm={6} md={4} key={feature.title}>
            <Card>
              <CardContent>
                <Box
                  sx={{
                    display: 'flex',
                    justifyContent: 'center',
                    mb: 2,
                    color: feature.color,
                  }}
                >
                  {feature.icon}
                </Box>
                <Typography variant="h6" component="div" align="center">
                  {feature.title}
                </Typography>
                <Typography
                  variant="body2"
                  color="text.secondary"
                  align="center"
                >
                  {feature.description}
                </Typography>
              </CardContent>
              <CardActions>
                <Button
                  fullWidth
                  variant="contained"
                  onClick={() => navigate(feature.path)}
                >
                  開始
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
};

export default Dashboard;