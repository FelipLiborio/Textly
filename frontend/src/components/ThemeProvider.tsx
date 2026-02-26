// src/components/ThemeProvider.tsx
'use client';

import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1f2937', // Gray dark, similar to the CSS variable
    },
    background: {
      default: '#f3f4f6', // Light gray
      paper: '#ffffff', // White
    },
    text: {
      primary: '#1f2937',
      secondary: '#6b7280',
    },
  },
});

export default function MuiThemeProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      {children}
    </ThemeProvider>
  );
}