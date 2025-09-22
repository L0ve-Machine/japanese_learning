import api from './api';
import { Subject, Question, Word, FlashCard, Video, StudyText } from '../types';

export const learningService = {
  async getSubjects(): Promise<Subject[]> {
    const response = await api.get('/learning/subjects/');
    return response.data.results || response.data;
  },

  async getQuestions(params?: {
    type?: string;
    subject?: number;
    year?: number;
  }): Promise<Question[]> {
    const response = await api.get('/learning/questions/', { params });
    return response.data.results || response.data;
  },

  async getRandomQuestions(count: number = 10): Promise<Question[]> {
    const response = await api.get(`/learning/questions/random/?count=${count}`);
    return response.data;
  },

  async getWords(params?: {
    category?: string;
    search?: string;
  }): Promise<Word[]> {
    const response = await api.get('/learning/words/', { params });
    return response.data.results || response.data;
  },

  async getFlashCards(): Promise<FlashCard[]> {
    const response = await api.get('/learning/flashcards/');
    return response.data.results || response.data;
  },

  async createFlashCard(wordId: number): Promise<FlashCard> {
    const response = await api.post('/learning/flashcards/', { word: wordId });
    return response.data;
  },

  async markFlashCardMemorized(id: number): Promise<void> {
    await api.post(`/learning/flashcards/${id}/mark_memorized/`);
  },

  async reviewFlashCard(id: number): Promise<void> {
    await api.post(`/learning/flashcards/${id}/review/`);
  },

  async getVideos(subjectId?: number): Promise<Video[]> {
    const params = subjectId ? { subject: subjectId } : {};
    const response = await api.get('/learning/videos/', { params });
    return response.data.results || response.data;
  },

  async getStudyTexts(subjectId?: number): Promise<StudyText[]> {
    const params = subjectId ? { subject: subjectId } : {};
    const response = await api.get('/learning/texts/', { params });
    return response.data.results || response.data;
  },
};