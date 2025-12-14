import React, { useState, useEffect } from 'react';
import AuthForm from './AuthForm';
import SweetManager from './SweetManager';
import { setAuthToken } from './api';
import './App.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    // Check if a token exists in local storage on component mount
    const token = localStorage.getItem('token');
    if (token) {
      setIsAuthenticated(true);
    }
  }, []);

  const handleLogout = () => {
    setAuthToken(null); // Clear the token
    setIsAuthenticated(false);
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>🍬 Sweet Shop Management System</h1>
        {isAuthenticated && (
          <button onClick={handleLogout} className="logout-button">
            Logout
          </button>
        )}
      </header>

      <main className="app-main">
        {isAuthenticated ? (
          <SweetManager />
        ) : (
          <AuthForm onAuthSuccess={() => setIsAuthenticated(true)} />
        )}
      </main>
    </div>
  );
}

export default App;