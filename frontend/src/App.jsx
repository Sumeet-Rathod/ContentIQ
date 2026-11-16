import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Sidebar from './components/Sidebar';
import Login from './pages/Login';
import Register from './pages/Register';
import CalendarView from './pages/CalendarView';
import PostCompose from './pages/PostCompose';
import Team from './pages/Team';
import Dashboard from './pages/Dashboard';
import Analytics from './pages/Analytics';
import ThumbnailScorer from './pages/ThumbnailScorer';
import Trends from './pages/Trends';
import Recommendations from './pages/Recommendations';
import FollowerForecast from './pages/FollowerForecast';
import ABTesting from './pages/ABTesting';
import Competitors from './pages/Competitors';
import Notifications from './pages/Notifications';

// Protected Route Component
const ProtectedLayout = ({ children }) => {
  const { token, loading } = useAuth();

  if (loading) {
    return (
      <div style={{ display: 'flex', height: '100vh', alignItems: 'center', justifyContent: 'center' }}>
        <div className="loading-spinner"></div>
      </div>
    );
  }

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="app-container">
      <Sidebar />
      {children}
    </div>
  );
};

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Public Auth Routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Protected Routes */}
          <Route
            path="/dashboard"
            element={
              <ProtectedLayout>
                <Dashboard />
              </ProtectedLayout>
            }
          />

          <Route
            path="/analytics"
            element={
              <ProtectedLayout>
                <Analytics />
              </ProtectedLayout>
            }
          />

          <Route
            path="/calendar"
            element={
              <ProtectedLayout>
                <CalendarView />
              </ProtectedLayout>
            }
          />

          <Route
            path="/compose"
            element={
              <ProtectedLayout>
                <PostCompose />
              </ProtectedLayout>
            }
          />

          <Route
            path="/compose/:id"
            element={
              <ProtectedLayout>
                <PostCompose />
              </ProtectedLayout>
            }
          />

          <Route
            path="/trends"
            element={
              <ProtectedLayout>
                <Trends />
              </ProtectedLayout>
            }
          />

          <Route
            path="/recommendations"
            element={
              <ProtectedLayout>
                <Recommendations />
              </ProtectedLayout>
            }
          />

          <Route
            path="/thumbnail"
            element={
              <ProtectedLayout>
                <ThumbnailScorer />
              </ProtectedLayout>
            }
          />

          <Route
            path="/forecast"
            element={
              <ProtectedLayout>
                <FollowerForecast />
              </ProtectedLayout>
            }
          />

          <Route
            path="/ab-tests"
            element={
              <ProtectedLayout>
                <ABTesting />
              </ProtectedLayout>
            }
          />

          <Route
            path="/competitors"
            element={
              <ProtectedLayout>
                <Competitors />
              </ProtectedLayout>
            }
          />

          <Route
            path="/notifications"
            element={
              <ProtectedLayout>
                <Notifications />
              </ProtectedLayout>
            }
          />

          <Route
            path="/team"
            element={
              <ProtectedLayout>
                <Team />
              </ProtectedLayout>
            }
          />

          {/* Fallback */}
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
