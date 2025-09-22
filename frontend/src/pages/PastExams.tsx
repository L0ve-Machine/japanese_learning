import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  Button,
  Radio,
  RadioGroup,
  FormControlLabel,
  FormControl,
  Alert,
  CircularProgress,
  Select,
  MenuItem,
  InputLabel,
  Grid,
} from '@mui/material';
import { learningService } from '../services/learning';
import { Question } from '../types';

const PastExams: React.FC = () => {
  const [questions, setQuestions] = useState<Question[]>([]);
  const [loading, setLoading] = useState(true);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
  const [showResult, setShowResult] = useState(false);
  const [score, setScore] = useState(0);
  const [year, setYear] = useState<number | ''>('');

  useEffect(() => {
    loadQuestions();
  }, [year]);

  const loadQuestions = async () => {
    setLoading(true);
    try {
      const params = year ? { type: 'past_exam', year } : { type: 'past_exam' };
      const data = await learningService.getQuestions(params);
      setQuestions(data);
      setCurrentIndex(0);
      setSelectedAnswer(null);
      setShowResult(false);
      setScore(0);
    } catch (error) {
      console.error('Failed to load questions:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAnswer = () => {
    if (selectedAnswer === null) return;

    const isCorrect = selectedAnswer === questions[currentIndex].correct_answer;
    if (isCorrect) {
      setScore(score + 1);
    }
    setShowResult(true);
  };

  const handleNext = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(currentIndex + 1);
      setSelectedAnswer(null);
      setShowResult(false);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" mt={4}>
        <CircularProgress />
      </Box>
    );
  }

  if (questions.length === 0) {
    return (
      <Container>
        <Typography variant="h5">問題が見つかりません</Typography>
      </Container>
    );
  }

  const currentQuestion = questions[currentIndex];

  return (
    <Container maxWidth="md">
      <Box sx={{ mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} sm={6}>
            <Typography variant="h4">過去問題</Typography>
          </Grid>
          <Grid item xs={12} sm={6}>
            <FormControl fullWidth size="small">
              <InputLabel>年度</InputLabel>
              <Select
                value={year}
                label="年度"
                onChange={(e) => setYear(e.target.value as number | '')}
              >
                <MenuItem value="">全て</MenuItem>
                <MenuItem value={2023}>2023年</MenuItem>
                <MenuItem value={2022}>2022年</MenuItem>
                <MenuItem value={2021}>2021年</MenuItem>
                <MenuItem value={2020}>2020年</MenuItem>
                <MenuItem value={2019}>2019年</MenuItem>
              </Select>
            </FormControl>
          </Grid>
        </Grid>
      </Box>

      <Card>
        <CardContent>
          <Box sx={{ mb: 2 }}>
            <Typography variant="body2" color="text.secondary">
              問題 {currentIndex + 1} / {questions.length}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              現在のスコア: {score} / {currentIndex + (showResult ? 1 : 0)}
            </Typography>
          </Box>

          <Typography variant="h6" sx={{ mb: 3 }}>
            {currentQuestion.question_text}
          </Typography>

          <FormControl component="fieldset">
            <RadioGroup
              value={selectedAnswer}
              onChange={(e) => setSelectedAnswer(Number(e.target.value))}
            >
              {currentQuestion.choices.map((choice, index) => (
                <FormControlLabel
                  key={index}
                  value={index}
                  control={<Radio />}
                  label={choice}
                  disabled={showResult}
                />
              ))}
            </RadioGroup>
          </FormControl>

          {showResult && (
            <Box sx={{ mt: 3 }}>
              <Alert
                severity={
                  selectedAnswer === currentQuestion.correct_answer
                    ? 'success'
                    : 'error'
                }
              >
                {selectedAnswer === currentQuestion.correct_answer
                  ? '正解！'
                  : `不正解。正解は「${currentQuestion.choices[currentQuestion.correct_answer]}」です。`}
              </Alert>
              <Typography variant="body1" sx={{ mt: 2 }}>
                <strong>解説：</strong> {currentQuestion.explanation}
              </Typography>
            </Box>
          )}

          <Box sx={{ mt: 3, display: 'flex', justifyContent: 'space-between' }}>
            {!showResult ? (
              <Button
                variant="contained"
                onClick={handleAnswer}
                disabled={selectedAnswer === null}
                fullWidth
              >
                回答する
              </Button>
            ) : (
              <>
                {currentIndex < questions.length - 1 ? (
                  <Button variant="contained" onClick={handleNext} fullWidth>
                    次の問題
                  </Button>
                ) : (
                  <Alert severity="info" sx={{ width: '100%' }}>
                    全ての問題が終了しました。最終スコア: {score} / {questions.length}
                  </Alert>
                )}
              </>
            )}
          </Box>
        </CardContent>
      </Card>
    </Container>
  );
};

export default PastExams;