// src/components/auth/header/AuthHeader.tsx
import styles from './AuthHeader.module.css';

export default function AuthHeader() {
  return (
    <header className={styles.header}>
      <div className={styles.container}>
        <span className={styles.brand}>Textly</span>
        <nav className={styles.nav}>
          <a href="#" className={styles.link}>Sobre</a>
          <a href="#" className={styles.link}>Contato</a>
        </nav>
      </div>
    </header>
  );
}