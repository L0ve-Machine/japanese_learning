import React, { useState } from 'react';
import {
  Container,
  Typography,
  Box,
  Paper,
  Grid,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
} from '@mui/material';
import { useAuth } from '../contexts/AuthContext';
import { authService } from '../services/auth';

const Profile: React.FC = () => {
  const { user, updateUser } = useAuth();
  const [nativeLanguage, setNativeLanguage] = useState(user?.native_language || 'en');
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');

  const languages = [
    { code: 'en', name: 'English' },
    { code: 'vi', name: 'Tiếng Việt' },
    { code: 'zh', name: '中文' },
    { code: 'ko', name: '한국어' },
    { code: 'th', name: 'ไทย' },
    { code: 'id', name: 'Bahasa Indonesia' },
    { code: 'my', name: 'မြန်မာ' },
  ];

  const handleLanguageUpdate = async () => {
    setSuccess(false);
    setError('');

    try {
      await authService.updateLanguage(nativeLanguage);
      if (user) {
        updateUser({ ...user, native_language: nativeLanguage });
      }
      setSuccess(true);
    } catch (err: any) {
      setError('言語の更新に失敗しました');
    }
  };

  return (
    <Container maxWidth="md">
      <Typography variant="h4" gutterBottom>
        プロフィール
      </Typography>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          基本情報
        </Typography>
        <Grid container spacing={3}>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="メールアドレス"
              value={user?.email || ''}
              disabled
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="会員ステータス"
              value={user?.is_premium ? 'プレミアム会員' : '無料会員'}
              disabled
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <FormControl fullWidth>
              <InputLabel>母語</InputLabel>
              <Select
                value={nativeLanguage}
                label="母語"
                onChange={(e) => setNativeLanguage(e.target.value)}
              >
                {languages.map((lang) => (
                  <MenuItem key={lang.code} value={lang.code}>
                    {lang.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="登録日"
              value={user?.created_at ? new Date(user.created_at).toLocaleDateString('ja-JP') : ''}
              disabled
            />
          </Grid>
        </Grid>

        {success && (
          <Alert severity="success" sx={{ mt: 2 }}>
            言語設定を更新しました
          </Alert>
        )}
        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}

        <Box sx={{ mt: 3 }}>
          <Button variant="contained" onClick={handleLanguageUpdate}>
            設定を保存
          </Button>
        </Box>
      </Paper>

      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          学習統計
        </Typography>
        <Grid container spacing={3}>
          <Grid item xs={12} sm={4}>
            <Box>
              <Typography variant="body2" color="text.secondary">
                総学習時間
              </Typography>
              <Typography variant="h4">24時間</Typography>
            </Box>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Box>
              <Typography variant="body2" color="text.secondary">
                完了した問題
              </Typography>
              <Typography variant="h4">456問</Typography>
            </Box>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Box>
              <Typography variant="body2" color="text.secondary">
                習得した単語
              </Typography>
              <Typography variant="h4">234語</Typography>
            </Box>
          </Grid>
        </Grid>
      </Paper>
    </Container>
  );
};

export default Profile;