// src/components/auth/LoginForm.tsx
"use client";

import { useState } from "react";
import { useAuth } from "../../../hooks/useAuth";
import styles from "./AuthForm.module.css";

export default function LoginForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const { login, loading, error } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await login({ email, password });
  };

  return (
    <form onSubmit={handleSubmit} className={styles.form}>
      <div className={styles.group}>
        <label className={styles.label}>Email</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className={styles.input}
          required
        />
      </div>
      <div className={styles.group}>
        <label className={styles.label}>Senha</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className={styles.input}
          required
        />
      </div>
      {error && <p className={styles.error}>{error}</p>}
      <button type="submit" disabled={loading} className={styles.button}>
        {loading ? "Entrando..." : "Entrar"}
      </button>
    </form>
  );
}
