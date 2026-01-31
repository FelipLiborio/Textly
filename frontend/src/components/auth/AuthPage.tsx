// src/components/auth/AuthPage.tsx
'use client';

import { useState } from 'react';
import AuthHeader from './header/AuthHeader';
import LoginForm from './form/LoginForm';
import RegisterForm from './form/RegisterForm';
import styles from './AuthPage.module.css';

export default function AuthPage() {
  const [isLogin, setIsLogin] = useState(true);

  return (
    <>
      <AuthHeader />
      <div className={styles.container}>
        <div className={styles.card}>
          <h1 className={styles.title}>Textly</h1>
          <div className={styles.tabs}>
            <button
              onClick={() => setIsLogin(true)}
              className={`${styles.tab} ${isLogin ? styles.active : ''}`}
            >
              Entrar
            </button>
            <button
              onClick={() => setIsLogin(false)}
              className={`${styles.tab} ${!isLogin ? styles.active : ''}`}
            >
              Registrar
            </button>
          </div>
          {isLogin ? <LoginForm /> : <RegisterForm />}
        </div>
      </div>
    </>
  );
}