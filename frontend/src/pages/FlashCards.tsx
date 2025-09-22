import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  Button,
  IconButton,
  CircularProgress,
  Grid,
} from '@mui/material';
import { Refresh, Check, NavigateBefore, NavigateNext } from '@mui/icons-material';
import { learningService } from '../services/learning';
import { FlashCard } from '../types';
import { useAuth } from '../contexts/AuthContext';

const FlashCards: React.FC = () => {
  const [flashcards, setFlashcards] = useState<FlashCard[]>([]);
  const [loading, setLoading] = useState(true);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [showAnswer, setShowAnswer] = useState(false);
  const { user } = useAuth();

  useEffect(() => {
    loadFlashcards();
  }, []);

  const loadFlashcards = async () => {
    try {
      const data = await learningService.getFlashCards();
      setFlashcards(data.filter(card => !card.is_memorized));
    } catch (error) {
      console.error('Failed to load flashcards:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFlip = () => {
    setShowAnswer(!showAnswer);
  };

  const handleMarkMemorized = async () => {
    if (flashcards[currentIndex]) {
      try {
        await learningService.markFlashCardMemorized(flashcards[currentIndex].id);
        const newFlashcards = flashcards.filter((_, index) => index !== currentIndex);
        setFlashcards(newFlashcards);
        if (currentIndex >= newFlashcards.length && currentIndex > 0) {
          setCurrentIndex(currentIndex - 1);
        }
        setShowAnswer(false);
      } catch (error) {
        console.error('Failed to mark as memorized:', error);
      }
    }
  };

  const handleReview = async () => {
    if (flashcards[currentIndex]) {
      try {
        await learningService.reviewFlashCard(flashcards[currentIndex].id);
        handleNext();
      } catch (error) {
        console.error('Failed to review:', error);
      }
    }
  };

  const handleNext = () => {
    if (currentIndex < flashcards.length - 1) {
      setCurrentIndex(currentIndex + 1);
      setShowAnswer(false);
    }
  };

  const handlePrevious = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
      setShowAnswer(false);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" mt={4}>
        <CircularProgress />
      </Box>
    );
  }

  if (flashcards.length === 0) {
    return (
      <Container>
        <Typography variant="h5">暗記カードがありません</Typography>
        <Typography variant="body1" sx={{ mt: 2 }}>
          「ことば」ページから単語を追加してください。
        </Typography>
      </Container>
    );
  }

  const currentCard = flashcards[currentIndex];

  return (
    <Container maxWidth="md">
      <Typography variant="h4" gutterBottom>
        暗記カード
      </Typography>

      <Box sx={{ mb: 2 }}>
        <Typography variant="body2" color="text.secondary">
          カード {currentIndex + 1} / {flashcards.length}
        </Typography>
      </Box>

      <Card
        sx={{
          minHeight: 300,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          cursor: 'pointer',
          transition: 'transform 0.3s',
          '&:hover': {
            transform: 'scale(1.02)',
          },
        }}
        onClick={handleFlip}
      >
        <CardContent sx={{ textAlign: 'center' }}>
          {!showAnswer ? (
            <>
              <Typography variant="h3" gutterBottom>
                {currentCard.word_data?.japanese}
              </Typography>
              <Typography variant="h5" color="text.secondary">
                {currentCard.word_data?.reading}
              </Typography>
            </>
          ) : (
            <>
              <Typography variant="h4" gutterBottom>
                {currentCard.word_data?.translations[user?.native_language || 'en']}
              </Typography>
              {currentCard.word_data?.example_sentence && (
                <Box sx={{ mt: 3 }}>
                  <Typography variant="body1">
                    {currentCard.word_data.example_sentence}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                    {currentCard.word_data.example_translation?.[user?.native_language || 'en']}
                  </Typography>
                </Box>
              )}
            </>
          )}
        </CardContent>
      </Card>

      <Grid container spacing={2} sx={{ mt: 3 }}>
        <Grid item xs={12} sm={3}>
          <Button
            fullWidth
            variant="outlined"
            startIcon={<NavigateBefore />}
            onClick={handlePrevious}
            disabled={currentIndex === 0}
          >
            前へ
          </Button>
        </Grid>
        <Grid item xs={12} sm={3}>
          <Button
            fullWidth
            variant="outlined"
            startIcon={<Refresh />}
            onClick={handleReview}
          >
            復習
          </Button>
        </Grid>
        <Grid item xs={12} sm={3}>
          <Button
            fullWidth
            variant="contained"
            color="success"
            startIcon={<Check />}
            onClick={handleMarkMemorized}
          >
            覚えた
          </Button>
        </Grid>
        <Grid item xs={12} sm={3}>
          <Button
            fullWidth
            variant="outlined"
            endIcon={<NavigateNext />}
            onClick={handleNext}
            disabled={currentIndex === flashcards.length - 1}
          >
            次へ
          </Button>
        </Grid>
      </Grid>

      <Box sx={{ mt: 2, textAlign: 'center' }}>
        <Typography variant="caption" color="text.secondary">
          カードをクリックして裏面を表示
        </Typography>
      </Box>
    </Container>
  );
};

export default FlashCards;