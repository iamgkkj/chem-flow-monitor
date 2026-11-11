import { useState } from 'react';

import { login, setToken } from '../api';

import newLogoFull from '../newlogofull.png';

// DRF returns field errors as {"non_field_errors": [...]} or {"detail": "..."},
// so the generic axios message ("Request failed with status code 400") is
// only used as a last resort.
export function errorMessage(err) {
  const data = err?.response?.data;

  if (data) {
    if (typeof data.detail === 'string') return data.detail;
    if (Array.isArray(data.non_field_errors) && data.non_field_errors[0]) {
      return String(data.non_field_errors[0]);
    }
    if (Array.isArray(data)) return String(data[0] ?? 'Login failed');

    const first = Object.values(data)[0];
    if (typeof first === 'string') return first;
    if (Array.isArray(first) && first[0]) return String(first[0]);
  }

  if (err?.code === 'ERR_NETWORK') {
    return 'Cannot reach the API. Check that the backend is deployed and reachable.';
  }

  return err?.message || 'Login failed';
}

export default function Login({ onLoggedIn, theme }) {
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
      setError(errorMessage(err));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="container">
      <div className="card">
        <img className="loginLogo" src={newLogoFull} alt="Chem Flow Monitor" />
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
