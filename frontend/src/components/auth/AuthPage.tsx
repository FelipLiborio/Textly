// src/components/auth/AuthPage.tsx
'use client';

import { useState } from 'react';
import { Container, Card, CardContent, Typography, Tabs, Tab, Box } from '@mui/material';
import AuthHeader from './header/AuthHeader';
import LoginForm from './form/LoginForm';
import RegisterForm from './form/RegisterForm';

export default function AuthPage() {
  const [isLogin, setIsLogin] = useState(true);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setIsLogin(newValue === 0);
  };

  return (
    <>
      <AuthHeader />
      <Container component="main" maxWidth="sm" sx={{ mt: 8 }}>
        <Card>
          <CardContent>
            <Typography component="h1" variant="h4" align="center" gutterBottom sx={{ mt: 3 }}>
              Textly
            </Typography>
            <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
              <Tabs value={isLogin ? 0 : 1} onChange={handleTabChange} aria-label="auth tabs">
                <Tab label="Entrar" />
                <Tab label="Registrar" />
              </Tabs>
            </Box>
            {isLogin ? <LoginForm /> : <RegisterForm />}
          </CardContent>
        </Card>
      </Container>
    </>
  );
}