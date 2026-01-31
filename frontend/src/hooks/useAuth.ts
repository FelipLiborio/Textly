// src/hooks/useAuth.ts
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { authService, LoginData, RegisterData } from '../services/auth/authService';

export const useAuth = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const router = useRouter();

  const login = async (data: LoginData) => {
    setLoading(true);
    setError('');
    try {
      await authService.login(data);
      router.push('/home'); // Redirecionar após login
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const register = async (data: RegisterData) => {
    setLoading(true);
    setError('');
    try {
      await authService.register(data);
      router.push('/home'); 
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return { login, register, loading, error };
};