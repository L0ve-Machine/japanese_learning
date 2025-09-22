import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Grid,
  Card,
  CardMedia,
  CardContent,
  CardActions,
  Button,
  CircularProgress,
  Chip,
} from '@mui/material';
import { PlayArrow, Lock } from '@mui/icons-material';
import { learningService } from '../services/learning';
import { Video } from '../types';
import { useAuth } from '../contexts/AuthContext';

const Videos: React.FC = () => {
  const [videos, setVideos] = useState<Video[]>([]);
  const [loading, setLoading] = useState(true);
  const { user } = useAuth();

  useEffect(() => {
    loadVideos();
  }, []);

  const loadVideos = async () => {
    try {
      const data = await learningService.getVideos();
      setVideos(data);
    } catch (error) {
      console.error('Failed to load videos:', error);
    } finally {
      setLoading(false);
    }
  };

  const handlePlayVideo = (videoUrl: string) => {
    window.open(videoUrl, '_blank');
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
        解説動画
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
        動画で詳しく学習しましょう
      </Typography>

      <Grid container spacing={3}>
        {videos.map((video) => (
          <Grid item xs={12} sm={6} md={4} key={video.id}>
            <Card>
              <CardMedia
                component="img"
                height="200"
                image={video.thumbnail_url || 'https://via.placeholder.com/400x200?text=Video'}
                alt={video.title}
                sx={{
                  position: 'relative',
                  filter: video.is_premium && !user?.is_premium ? 'blur(3px)' : 'none',
                }}
              />
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {video.title}
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                  {video.description}
                </Typography>
                <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                  {video.subject_name && (
                    <Chip label={video.subject_name} size="small" />
                  )}
                  {video.duration_minutes && (
                    <Chip label={`${video.duration_minutes}分`} size="small" variant="outlined" />
                  )}
                  {video.is_premium && (
                    <Chip label="プレミアム" size="small" color="secondary" />
                  )}
                </Box>
              </CardContent>
              <CardActions>
                {video.is_premium && !user?.is_premium ? (
                  <Button
                    fullWidth
                    variant="outlined"
                    disabled
                    startIcon={<Lock />}
                  >
                    プレミアム会員限定
                  </Button>
                ) : (
                  <Button
                    fullWidth
                    variant="contained"
                    startIcon={<PlayArrow />}
                    onClick={() => handlePlayVideo(video.video_url)}
                  >
                    視聴する
                  </Button>
                )}
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
};

export default Videos;