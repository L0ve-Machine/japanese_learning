export interface User {
  id: number;
  email: string;
  native_language: string;
  is_premium: boolean;
  subscription_end_date?: string;
  created_at: string;
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

// Hierarchical Learning Content Types
export interface StudyText {
  id: number;
  title: string;
  content: string;
  translations: Record<string, any>;
  order: number;
  is_premium: boolean;
}

export interface Page {
  id: number;
  name: string;
  description: string;
  order: number;
  is_active: boolean;
  texts?: StudyText[];
}

export interface Chapter {
  id: number;
  name: string;
  description: string;
  translations: Record<string, any>;
  order: number;
  is_active: boolean;
  pages?: Page[];
}

export interface SubjectItem {
  id: number;
  name: string;
  description: string;
  translations: Record<string, any>;
  order: number;
  is_active: boolean;
  chapters?: Chapter[];
}

// Enhanced Subject interface with hierarchy
export interface Subject {
  id: number;
  name: string;
  description: string;
  group_key?: string;
  indonesian_name?: string;
  order: number;
  is_active: boolean;
  items?: SubjectItem[];
  // Computed fields for display
  group?: string;
  progress?: number;
  lessons?: number;
  questions?: number;
  completed?: boolean;
  created_at?: string;
  updated_at?: string;
}

// Navigation breadcrumb type
export interface Breadcrumb {
  id: number;
  name: string;
  type: 'subject' | 'item' | 'chapter' | 'page' | 'text';
}

export interface UserProgress {
  id: number;
  subject: number;
  subject_name?: string;
  item?: number;
  item_name?: string;
  chapter?: number;
  chapter_name?: string;
  page?: number;
  page_name?: string;
  text?: number;
  text_title?: string;
  completed: boolean;
  completion_percentage: number;
  last_accessed: string;
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