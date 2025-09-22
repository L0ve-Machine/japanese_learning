import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  TextField,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton,
  Chip,
  CircularProgress,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Grid,
} from '@mui/material';
import { Add, Visibility, VisibilityOff } from '@mui/icons-material';
import { learningService } from '../services/learning';
import { Word } from '../types';
import { useAuth } from '../contexts/AuthContext';

const Vocabulary: React.FC = () => {
  const [words, setWords] = useState<Word[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState<string>('');
  const [showTranslation, setShowTranslation] = useState(false);
  const { user } = useAuth();

  useEffect(() => {
    loadWords();
  }, [category, search]);

  const loadWords = async () => {
    setLoading(true);
    try {
      const params: any = {};
      if (category) params.category = category;
      if (search) params.search = search;

      const data = await learningService.getWords(params);
      setWords(data);
    } catch (error) {
      console.error('Failed to load words:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddToFlashcard = async (wordId: number) => {
    try {
      await learningService.createFlashCard(wordId);
    } catch (error) {
      console.error('Failed to add to flashcard:', error);
    }
  };

  const getCategoryLabel = (category: string) => {
    switch (category) {
      case 'medical':
        return '医療用語';
      case 'caregiving':
        return '介護用語';
      case 'general':
        return '一般用語';
      default:
        return category;
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" mt={4}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 3 }}>
        <Typography variant="h4" gutterBottom>
          ことば（単語帳）
        </Typography>

        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} sm={4}>
            <TextField
              fullWidth
              label="検索"
              variant="outlined"
              size="small"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </Grid>
          <Grid item xs={12} sm={3}>
            <FormControl fullWidth size="small">
              <InputLabel>カテゴリー</InputLabel>
              <Select
                value={category}
                label="カテゴリー"
                onChange={(e) => setCategory(e.target.value)}
              >
                <MenuItem value="">全て</MenuItem>
                <MenuItem value="medical">医療用語</MenuItem>
                <MenuItem value="caregiving">介護用語</MenuItem>
                <MenuItem value="general">一般用語</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={3}>
            <IconButton
              onClick={() => setShowTranslation(!showTranslation)}
              color="primary"
            >
              {showTranslation ? <VisibilityOff /> : <Visibility />}
            </IconButton>
            <Typography variant="body2" component="span">
              翻訳表示
            </Typography>
          </Grid>
        </Grid>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>日本語</TableCell>
              <TableCell>読み方</TableCell>
              <TableCell>
                {showTranslation ? '翻訳' : 'カテゴリー'}
              </TableCell>
              <TableCell>例文</TableCell>
              <TableCell align="center">アクション</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {words.map((word) => (
              <TableRow key={word.id}>
                <TableCell>
                  <Typography variant="h6">{word.japanese}</Typography>
                </TableCell>
                <TableCell>{word.reading}</TableCell>
                <TableCell>
                  {showTranslation ? (
                    word.translations[user?.native_language || 'en'] || '-'
                  ) : (
                    <Chip
                      label={getCategoryLabel(word.category)}
                      size="small"
                      color="primary"
                      variant="outlined"
                    />
                  )}
                </TableCell>
                <TableCell>
                  <Typography variant="body2">{word.example_sentence}</Typography>
                  {showTranslation && word.example_translation && (
                    <Typography variant="caption" color="text.secondary">
                      {word.example_translation[user?.native_language || 'en']}
                    </Typography>
                  )}
                </TableCell>
                <TableCell align="center">
                  <IconButton
                    onClick={() => handleAddToFlashcard(word.id)}
                    color="primary"
                  >
                    <Add />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Container>
  );
};

export default Vocabulary;