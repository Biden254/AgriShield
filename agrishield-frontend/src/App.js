import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import './App.css';
import Dashboard from './pages/Dashboard';
import Alerts from './pages/Alerts';
import Report from './pages/Report';
import Settings from './pages/Settings';
import NavBar from './components/common/NavBar';
import { I18nextProvider } from 'react-i18next';
import i18n from './services/i18n';

const theme = createTheme({
  palette: {
    primary: {
      main: '#2E7D32', // Green
    },
    secondary: {
      main: '#1976D2', // Blue
    },
    error: {
      main: '#D32F2F', // Red
    },
    background: {
      default: '#f5f5f5',
    },
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
                <Route path="/" element={<Dashboard />} />
                <Route path="/alerts" element={<Alerts />} />
                <Route path="/report" element={<Report />} />
                <Route path="/settings" element={<Settings />} />
              </Routes>
            </main>
          </div>
        </Router>
      </ThemeProvider>
    </I18nextProvider>
  );
}

export default App;