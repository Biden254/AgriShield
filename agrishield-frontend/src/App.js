import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import './App.css';

// Existing pages
import Dashboard from './pages/Dashboard';
import Alerts from './pages/Alerts';
import Report from './pages/Report';
import Settings from './pages/Settings';

// Auth pages
import Login from './pages/Login';
import Signup from './pages/Signup';

// Components
import NavBar from './components/common/NavBar';
import ProtectedRoute from './components/ProtectedRoute';

import { I18nextProvider } from 'react-i18next';
import i18n from './services/i18n';

const theme = createTheme({
  palette: {
    primary: { main: '#2E7D32' },
    secondary: { main: '#1976D2' },
    error: { main: '#D32F2F' },
    background: { default: '#f5f5f5' },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
  },
});

function App() {
  return (
    <I18nextProvider i18n={i18n}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Router>
          <div className="app-container">
            <NavBar />
            <main className="main-content">
              <Routes>
                {/* Public routes */}
                <Route path="/login" element={<Login />} />
                <Route path="/signup" element={<Signup />} />

                {/* Protected routes */}
                <Route
                  path="/"
                  element={
                    <ProtectedRoute>
                      <Dashboard />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/alerts"
                  element={
                    <ProtectedRoute>
                      <Alerts />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/report"
                  element={
                    <ProtectedRoute>
                      <Report />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/settings"
                  element={
                    <ProtectedRoute>
                      <Settings />
                    </ProtectedRoute>
                  }
                />
              </Routes>
            </main>
          </div>
        </Router>
      </ThemeProvider>
    </I18nextProvider>
  );
}

export default App;
