import './App.css';

import { useEffect, useState } from 'react';

import Dashboard from './components/Dashboard';
import Login from './components/Login';
import { getToken } from './api';

function App() {
  const [isAuthed, setIsAuthed] = useState(false);
  const [theme, setTheme] = useState('dark');

  useEffect(() => {
    setIsAuthed(Boolean(getToken()));
    const savedTheme = localStorage.getItem('theme');
    setTheme(savedTheme === 'light' ? 'light' : 'dark');
  }, []);

  function toggleTheme() {
    setTheme((prev) => {
      const next = prev === 'dark' ? 'light' : 'dark';
      localStorage.setItem('theme', next);
      return next;
    });
  }

  return (
    <div className={`App theme-${theme}`}>
      {isAuthed ? (
        <Dashboard onLogout={() => setIsAuthed(false)} theme={theme} onToggleTheme={toggleTheme} />
      ) : (
        <Login onLoggedIn={() => setIsAuthed(true)} theme={theme} />
      )}
    </div>
  );
}

export default App;
