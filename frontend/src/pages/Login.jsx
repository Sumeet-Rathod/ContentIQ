import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  LogIn,
  AlertCircle,
  Mail,
  Lock,
  Eye,
  EyeOff,
  Shield,
  Edit3,
  CheckCircle2,
  Sparkles,
  TrendingUp,
  Image as ImageIcon,
  LineChart,
  ArrowRight
} from 'lucide-react';

const Login = () => {
  const [email, setEmail] = useState('alpha_admin@example.com');
  const [password, setPassword] = useState('Password123!');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [activeRoleKey, setActiveRoleKey] = useState('alpha_admin');

  const { login } = useAuth();
  const navigate = useNavigate();

  const DEMO_ROLES = [
    {
      key: 'alpha_admin',
      role: 'admin',
      tenant: 'Apex Digital Agency',
      name: 'Alex Vance (Admin)',
      email: 'alpha_admin@example.com',
      pass: 'Password123!',
      icon: Shield,
      badge: 'Full Access',
      desc: '12 Modules + Continuous ML Retraining Trigger'
    },
    {
      key: 'alpha_editor',
      role: 'editor',
      tenant: 'Apex Digital Agency',
      name: 'Elena Rostova (Editor)',
      email: 'alpha_editor@example.com',
      pass: 'Password123!',
      icon: Edit3,
      badge: 'Creator',
      desc: 'Compose Posts, AI Predictions & Calendar'
    },
    {
      key: 'alpha_client',
      role: 'client',
      tenant: 'Apex Digital Agency',
      name: 'Chloe Sullivan (Client)',
      email: 'alpha_client@example.com',
      pass: 'Password123!',
      icon: Eye,
      badge: 'Observer',
      desc: 'Read-Only Portal (Retrain strictly locked)'
    },
    {
      key: 'beta_admin',
      role: 'admin',
      tenant: 'Nexus Global Media',
      name: 'Bruce Wayne (Tenant 2)',
      email: 'beta_admin@example.com',
      pass: 'Password123!',
      icon: Shield,
      badge: 'Tenant B',
      desc: 'Demonstrates 100% Zero-Leak Tenant Isolation'
    }
  ];

  const handleSelectRole = (r) => {
    setActiveRoleKey(r.key);
    setEmail(r.email);
    setPassword(r.pass);
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await login(email, password);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Invalid email or password.');
    } finally {
      setLoading(false);
    }
  };

  React.useEffect(() => {
    const storedToken = localStorage.getItem('contentiq_token');
    if (storedToken) {
      navigate('/dashboard', { replace: true });
    }
  }, [navigate]);

  const activeRoleObj = DEMO_ROLES.find((r) => r.key === activeRoleKey);

  return (
    <div className="auth-split-wrapper">
      {/* Left Brand Showcase Section */}
      <div className="auth-brand-side">
        <div className="auth-brand-header">
          <div className="auth-brand-logo-row">
            <div className="auth-brand-logo-icon">IQ</div>
            <div className="auth-brand-name">ContentIQ</div>
            <span className="auth-brand-version-pill">v1.0 Enterprise</span>
          </div>

          <h1 className="auth-brand-tagline">
            The Autonomous Social Media <span>Intelligence</span> & Scheduling Platform
          </h1>
          <p className="auth-brand-desc">
            Engineered for high-velocity marketing agencies and creator teams. Seamlessly integrates
            pre-publish machine learning predictions, computer vision thumbnail analytics, and strict multi-tenant governance.
          </p>
        </div>

        {/* Feature Highlights with Micro-cards */}
        <div className="auth-feature-list">
          <div className="auth-feature-item">
            <div className="auth-feature-icon-wrap">
              <Sparkles size={18} />
            </div>
            <div>
              <div className="auth-feature-title">Pre-Flight Predictive AI Scoring</div>
              <div className="auth-feature-desc">
                10-feature Random Forest ensemble predicting engagement tiers (Low, Med, High) with 88% precision prior to publication.
              </div>
            </div>
          </div>

          <div className="auth-feature-item">
            <div className="auth-feature-icon-wrap">
              <LineChart size={18} />
            </div>
            <div>
              <div className="auth-feature-title">Facebook Prophet Growth Curves</div>
              <div className="auth-feature-desc">
                Bayesian time-series follower projection with 80% confidence intervals and cyclical day-of-week seasonality analysis.
              </div>
            </div>
          </div>

          <div className="auth-feature-item">
            <div className="auth-feature-icon-wrap">
              <ImageIcon size={18} />
            </div>
            <div>
              <div className="auth-feature-title">OpenCV Computer Vision Scorer</div>
              <div className="auth-feature-desc">
                Headless image aesthetics calculating Rule-of-Thirds balance, Shannon entropy contrast, and facial presence.
              </div>
            </div>
          </div>
        </div>

        {/* Stat Ticker Strip */}
        <div className="auth-stat-strip">
          <div className="auth-stat-cell">
            <div className="auth-stat-num">12</div>
            <div className="auth-stat-lbl">Active Modules</div>
          </div>
          <div className="auth-stat-cell">
            <div className="auth-stat-num">88.0%</div>
            <div className="auth-stat-lbl">Model Precision</div>
          </div>
          <div className="auth-stat-cell">
            <div className="auth-stat-num">9</div>
            <div className="auth-stat-lbl">Collections</div>
          </div>
          <div className="auth-stat-cell">
            <div className="auth-stat-num">100%</div>
            <div className="auth-stat-lbl">Offline Viva Ready</div>
          </div>
        </div>

        {/* Commercial Footer */}
        <div className="auth-brand-footer">
          <div>ContentIQ Enterprise • Cloud Multimodal Social Intelligence</div>
          <div>Production SLA 99.9% • Real-time Active Learning</div>
        </div>
      </div>

      {/* Right Interactive Form Section */}
      <div className="auth-form-side">
        <div className="auth-form-card">
          <div className="auth-form-header">
            <h2 className="auth-form-title">Sign In to Agency</h2>
            <p className="auth-form-subtitle">
              Enter credentials or pick a 1-click viva evaluator role below for instant automated testing.
            </p>
          </div>

          {error && (
            <div className="alert alert-danger" role="alert">
              <AlertCircle size={18} />
              <span>{error}</span>
            </div>
          )}

          {/* 1-Click Role Switcher Hub */}
          <div className="role-hub-container">
            <div className="role-hub-header">
              <span className="role-hub-title">
                <Sparkles size={14} color="#b8860b" />
                1-Click Viva Demo Role Switcher
              </span>
              <span className="role-hub-badge">Interactive</span>
            </div>

            <div className="role-hub-grid">
              {DEMO_ROLES.map((r) => {
                const IconComponent = r.icon;
                const isSelected = activeRoleKey === r.key;
                return (
                  <button
                    key={r.key}
                    type="button"
                    className={`role-tile ${isSelected ? 'active' : ''}`}
                    onClick={() => handleSelectRole(r)}
                  >
                    <div className="role-tile-top">
                      <span className="role-tile-title">
                        <IconComponent size={14} color={isSelected ? '#b8860b' : '#1f3864'} />
                        {r.role === 'admin' && r.key.startsWith('alpha') ? 'Agency Admin' :
                         r.role === 'editor' ? 'Content Editor' :
                         r.role === 'client' ? 'Client Portal' : 'Tenant 2 Admin'}
                      </span>
                      <span className="role-tile-status-dot" />
                    </div>
                    <span className="role-tile-desc">{r.desc}</span>
                  </button>
                );
              })}
            </div>

            {activeRoleObj && (
              <div className="role-selected-banner">
                <CheckCircle2 size={13} color="#b8860b" />
                <span>
                  Selected: <strong>{activeRoleObj.name}</strong> • {activeRoleObj.tenant} ({activeRoleObj.badge})
                </span>
              </div>
            )}
          </div>

          {/* Login Form */}
          <form onSubmit={handleSubmit}>
            <div className="form-group" style={{ marginBottom: '14px' }}>
              <label className="form-label" style={{ fontWeight: 600, fontSize: '0.84rem' }}>
                Account Email Address
              </label>
              <div className="input-icon-wrapper">
                <Mail size={16} className="input-prefix-icon" />
                <input
                  type="email"
                  className="form-control"
                  placeholder="name@agency.com"
                  value={email}
                  onChange={(e) => {
                    setEmail(e.target.value);
                    setActiveRoleKey('');
                  }}
                  required
                />
              </div>
            </div>

            <div className="form-group" style={{ marginBottom: '18px' }}>
              <label className="form-label" style={{ fontWeight: 600, fontSize: '0.84rem' }}>
                Security Password
              </label>
              <div className="input-icon-wrapper">
                <Lock size={16} className="input-prefix-icon" />
                <input
                  type={showPassword ? 'text' : 'password'}
                  className="form-control"
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
                <button
                  type="button"
                  className="input-toggle-btn"
                  onClick={() => setShowPassword(!showPassword)}
                  title={showPassword ? 'Hide password' : 'Show password'}
                >
                  {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
            </div>

            <button
              type="submit"
              className="btn-auth-submit"
              disabled={loading}
            >
              {loading ? (
                <span className="loading-spinner" />
              ) : (
                <>
                  <LogIn size={18} />
                  <span>Access Platform Dashboard</span>
                  <ArrowRight size={16} style={{ marginLeft: '4px' }} />
                </>
              )}
            </button>
          </form>

          <div className="auth-bottom-switch">
            Need a fresh agency tenant workspace?
            <Link to="/register">Create new tenant</Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
