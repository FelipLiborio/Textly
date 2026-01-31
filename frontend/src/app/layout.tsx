import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Textly',
  description: 'Aplicação de anotações',
  icons: {
    icon: '/Textly/Versao01.png',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}