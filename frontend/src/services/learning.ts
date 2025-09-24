import api from './api';
import {
  Subject, Question, Word, FlashCard, Video, StudyText,
  SubjectItem, Chapter, Page, UserProgress
} from '../types';

export const learningService = {
  async getSubjects(params?: {
    group?: string;
    search?: string;
  }): Promise<Subject[]> {
    const response = await api.get('/learning/subjects/', { params });
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

  async getStudyTexts(pageId?: number): Promise<StudyText[]> {
    const params = pageId ? { page: pageId } : {};
    const response = await api.get('/learning/texts/', { params });
    return response.data.results || response.data;
  },

  // Hierarchical Content Methods
  async getSubjectHierarchy(subjectId: number): Promise<Subject> {
    const response = await api.get(`/learning/subjects/${subjectId}/hierarchy/`);
    return response.data;
  },

  async getSubjectProgress(subjectId: number): Promise<UserProgress[]> {
    const response = await api.get(`/learning/subjects/${subjectId}/progress/`);
    return response.data;
  },

  async getSubjectItems(subjectId?: number): Promise<SubjectItem[]> {
    const params = subjectId ? { subject: subjectId } : {};
    const response = await api.get('/learning/subject-items/', { params });
    return response.data.results || response.data;
  },

  async getChapters(itemId?: number): Promise<Chapter[]> {
    const params = itemId ? { item: itemId } : {};
    const response = await api.get('/learning/chapters/', { params });
    return response.data.results || response.data;
  },

  async getPages(chapterId?: number): Promise<Page[]> {
    const params = chapterId ? { chapter: chapterId } : {};
    const response = await api.get('/learning/pages/', { params });
    return response.data.results || response.data;
  },

  async getPageTexts(pageId: number): Promise<StudyText[]> {
    const response = await api.get(`/learning/pages/${pageId}/texts/`);
    return response.data;
  },

  // Progress Tracking
  async getUserProgress(subjectId?: number): Promise<UserProgress[]> {
    const params = subjectId ? { subject_id: subjectId } : {};
    const response = await api.get('/learning/progress/subject_progress/', { params });
    return response.data.results || response.data;
  },

  async markCompleted(progress: {
    subject_id: number;
    item_id?: number;
    chapter_id?: number;
    page_id?: number;
    text_id?: number;
  }): Promise<UserProgress> {
    const response = await api.post('/learning/progress/mark_completed/', progress);
    return response.data;
  },
};