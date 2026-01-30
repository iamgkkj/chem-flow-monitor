import './App.css';

import { useEffect, useState } from 'react';

import Dashboard from './components/Dashboard';
import Login from './components/Login';
import { getToken } from './api';

function App() {
  const [isAuthed, setIsAuthed] = useState(false);

  useEffect(() => {
    setIsAuthed(Boolean(getToken()));
  }, []);

  return (
    <div className="App">
      {isAuthed ? (
        <Dashboard onLogout={() => setIsAuthed(false)} />
      ) : (
        <Login onLoggedIn={() => setIsAuthed(true)} />
      )}
    </div>
  );
}

export default App;
