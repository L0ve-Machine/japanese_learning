export interface User {
  id: number;
  email: string;
  native_language: string;
  is_premium: boolean;
  subscription_end_date?: string;
  created_at: string;
}

export interface Subject {
  id: number;
  name: string;
  description: string;
  order: number;
  is_active: boolean;
}

export interface Question {
  id: number;
  subject?: number;
  subject_name?: string;
  question_type: 'past_exam' | 'subject';
  year?: number;
  question_text: string;
  choices: string[];
  correct_answer: number;
  explanation: string;
  translations: Record<string, any>;
  is_premium: boolean;
}

export interface Word {
  id: number;
  japanese: string;
  reading: string;
  category: 'medical' | 'caregiving' | 'general';
  translations: Record<string, string>;
  example_sentence?: string;
  example_translation?: Record<string, string>;
  is_premium: boolean;
}

export interface FlashCard {
  id: number;
  word: number;
  word_data?: Word;
  is_memorized: boolean;
  review_count: number;
  last_reviewed?: string;
}

export interface Video {
  id: number;
  title: string;
  description: string;
  video_url: string;
  thumbnail_url?: string;
  duration_minutes?: number;
  subject?: number;
  subject_name?: string;
  is_premium: boolean;
  order: number;
}

export interface StudyText {
  id: number;
  subject: number;
  subject_name?: string;
  title: string;
  content: string;
  translations: Record<string, any>;
  order: number;
  is_premium: boolean;
}

export interface SubscriptionPlan {
  id: number;
  name: string;
  description: string;
  price: number;
  duration_days: number;
  features: string[];
  is_active: boolean;
}

export interface Subscription {
  id: number;
  plan: number;
  plan_details?: SubscriptionPlan;
  status: 'active' | 'cancelled' | 'expired' | 'pending';
  start_date: string;
  end_date: string;
  created_at: string;
}

export interface UserProgress {
  id: number;
  content_type: string;
  content_id: number;
  completed: boolean;
  score?: number;
  completed_at?: string;
  created_at: string;
}