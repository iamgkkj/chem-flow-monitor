import { useState } from 'react';

import { login, setToken } from '../api';

export default function Login({ onLoggedIn }) {
  const [username, setUsername] = useState('demo');
  const [password, setPassword] = useState('demo12345');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const data = await login(username, password);
      setToken(data.token);
      onLoggedIn();
    } catch (err) {
      const msg = err?.response?.data?.detail || err?.message || 'Login failed';
      setError(msg);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="container">
      <div className="card">
        <h1 className="title">Chem Flow Monitor</h1>
        <p className="subtitle">Sign in to access the dashboard</p>

        <form onSubmit={handleSubmit} className="form">
          <label className="label">
            Username
            <input
              className="input"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              autoComplete="username"
            />
          </label>

          <label className="label">
            Password
            <input
              className="input"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
            />
          </label>

          {error ? <div className="error">{error}</div> : null}

          <button className="button" type="submit" disabled={loading}>
            {loading ? 'Signing in…' : 'Sign in'}
          </button>
        </form>

        <p className="hint">
          Tip: default demo user is <code>demo</code> / <code>demo12345</code>
        </p>
      </div>
    </div>
  );
}
