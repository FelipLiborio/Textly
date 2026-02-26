// src/components/auth/header/AuthHeader.tsx
import { AppBar, Toolbar, Typography, Link, Box } from '@mui/material';

export default function AuthHeader() {
  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Textly
        </Typography>
        <Box>
          <Link href="#" color="inherit" sx={{ mr: 2 }}>
            Sobre
          </Link>
          <Link href="#" color="inherit">
            Contato
          </Link>
        </Box>
      </Toolbar>
    </AppBar>
  );
}