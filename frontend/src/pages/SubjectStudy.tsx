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
  CircularProgress,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { learningService } from '../services/learning';
import { Subject } from '../types';

const SubjectStudy: React.FC = () => {
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    loadSubjects();
  }, []);

  const loadSubjects = async () => {
    try {
      const data = await learningService.getSubjects();
      setSubjects(data);
    } catch (error) {
      console.error('Failed to load subjects:', error);
    } finally {
      setLoading(false);
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
      <Typography variant="h4" gutterBottom>
        科目学習
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
        学習したい科目を選択してください
      </Typography>

      <Grid container spacing={3}>
        {subjects.map((subject) => (
          <Grid item xs={12} sm={6} md={4} key={subject.id}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {subject.name}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {subject.description}
                </Typography>
              </CardContent>
              <CardActions>
                <Button
                  size="small"
                  variant="contained"
                  fullWidth
                  onClick={() => navigate(`/subjects/${subject.id}`)}
                >
                  学習を始める
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
};

export default SubjectStudy;