import api from './api';
import { User } from '../types';

export const authService = {
  async login(email: string, password: string) {
    const response = await api.post('/auth/login/', { email, password });
    return response.data;
  },

  async register(email: string, password: string, nativeLanguage: string) {
    const response = await api.post('/auth/registration/', {
      email,
      password1: password,
      password2: password,
      native_language: nativeLanguage,
    });
    return response.data;
  },

  async logout() {
    await api.post('/auth/logout/');
  },

  async getMe(): Promise<User> {
    const response = await api.get('/users/profile/me/');
    return response.data;
  },

  async updateLanguage(language: string) {
    const response = await api.patch('/users/profile/update_language/', {
      native_language: language,
    });
    return response.data;
  },
};