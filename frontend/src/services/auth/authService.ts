// src/services/authService.ts
import { BACKEND_URL } from '../../config/api';

export interface LoginData {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
}

export const authService = {
  async login(data: LoginData) {
    const response = await fetch(`${BACKEND_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
      credentials: 'include',
    });
    if (!response.ok) {
      if (response.status === 401) {
        throw new Error('Email ou senha incorretos. Verifique e tente novamente.');
      }
      const error = await response.json();
      throw new Error(error.detail || 'Erro no login');
    }
    return response.json();
  },

  async register(data: RegisterData) {
    const response = await fetch(`${BACKEND_URL}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
      credentials: 'include',
    });
    if (!response.ok) {
      if (response.status === 409) {
        throw new Error('Este email já está cadastrado. Tente fazer login.');
      }
      const error = await response.json();
      throw new Error(error.detail || 'Erro no registro');
    }
    return response.json();
  },
};