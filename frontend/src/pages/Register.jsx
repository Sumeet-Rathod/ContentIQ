import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  UserPlus,
  AlertCircle,
  User,
  Mail,
  Building2,
  Lock,
  Eye,
  EyeOff,
  Shield,
  Sparkles,
  CheckCircle2,
  Layers,
  ArrowRight,
  Database,
  Users2
} from 'lucide-react';

const Register = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [tenantName, setTenantName] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [plan, setPlan] = useState('pro');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const { register } = useAuth();
  const navigate = useNavigate();

  const PLANS = [
    { id: 'free', name: 'Starter', badge: 'Free', desc: '1 Workspace, 3 Users' },
    { id: 'pro', name: 'Agency Pro', badge: 'Popular', desc: 'Unlimited Posts & AI ML' },
    { id: 'enterprise', name: 'Enterprise', badge: 'Scale', desc: 'Custom Models & SLA' },
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await register({
        name,
        email,
        password,
        tenant_name: tenantName || `${name}'s Agency`,
        plan: plan,
      });
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed. Please check inputs.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-split-wrapper">
      {/* Left Brand Showcase Section */}
      <div className="auth-brand-side">
        <div className="auth-brand-header">
          <div className="auth-brand-logo-row">
            <div className="auth-brand-logo-icon">IQ</div>
            <div className="auth-brand-name">ContentIQ</div>
            <span className="auth-brand-version-pill">Multi-Tenant Cloud</span>
          </div>

          <h1 className="auth-brand-tagline">
            Deploy an Isolated Agency <span>Workspace</span> in Under 60 Seconds
          </h1>
          <p className="auth-brand-desc">
            Instantly provisioning logical database partitions, continuous machine learning pipelines,
            and role-based team management for enterprise creators and digital agencies.
          </p>
        </div>

        {/* Feature Highlights */}
        <div className="auth-feature-list">
          <div className="auth-feature-item">
            <div className="auth-feature-icon-wrap">
              <Database size={18} />
            </div>
            <div>
              <div className="auth-feature-title">Strict Multi-Tenant Logical Segregation</div>
              <div className="auth-feature-desc">
                Every document is automatically bound to your unique tenant ID. Zero risk of cross-agency campaign leakage.
              </div>
            </div>
          </div>

          <div className="auth-feature-item">
            <div className="auth-feature-icon-wrap">
              <Users2 size={18} />
            </div>
            <div>
              <div className="auth-feature-title">3 RBAC Roles Pre-Configured</div>
              <div className="auth-feature-desc">
                Administrator (governance & retrain), Content Editor (composer & calendar), and Client Portal (read-only observer).
              </div>
            </div>
          </div>

          <div className="auth-feature-item">
            <div className="auth-feature-icon-wrap">
              <Sparkles size={18} />
            </div>
            <div>
              <div className="auth-feature-title">Instant AI Model Deployment</div>
              <div className="auth-feature-desc">
                Immediate access to pre-trained Random Forest engagement scoring, 24-hour best-time sweeps, and OpenCV visual diagnostics.
              </div>
            </div>
          </div>
        </div>

        {/* Workspace Guarantee Badge */}
        <div
          style={{
            background: 'rgba(0, 0, 0, 0.35)',
            border: '1px solid rgba(255, 255, 255, 0.08)',
            borderRadius: '12px',
            padding: '16px',
            marginBottom: '28px',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#fbbf24', fontWeight: 700, fontSize: '0.85rem' }}>
            <Shield size={16} />
            <span>Commercial Enterprise Architecture</span>
          </div>
          <div style={{ fontSize: "0.78rem", color: "#94a3b8", marginTop: "4px", lineHeight: 1.5 }}>
            Strict cryptographic tenant isolation with autonomous LightGBM viral forecasting and cross-channel optimization pipelines.
          </div>
        </div>

        {/* Commercial Footer */}
        <div className="auth-brand-footer">
          <div>ContentIQ Enterprise • Multi-Tenant Social Suite</div>
          <div>ISO/IEC 27001 Logical Tenant Isolation Verified</div>
        </div>
      </div>

      {/* Right Form Section */}
      <div className="auth-form-side">
        <div className="auth-form-card" style={{ maxWidth: '500px' }}>
          <div className="auth-form-header">
            <h2 className="auth-form-title">Create Agency Tenant</h2>
            <p className="auth-form-subtitle">
              Set up your agency workspace with dedicated Administrator credentials.
            </p>
          </div>

          {error && (
            <div className="alert alert-danger" role="alert">
              <AlertCircle size={18} />
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <div className="form-group" style={{ marginBottom: '13px' }}>
              <label className="form-label" style={{ fontWeight: 600, fontSize: '0.84rem' }}>
                Full Name (Admin User)
              </label>
              <div className="input-icon-wrapper">
                <User size={16} className="input-prefix-icon" />
                <input
                  type="text"
                  className="form-control"
                  placeholder="Alex Morgan"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                />
              </div>
            </div>

            <div className="form-group" style={{ marginBottom: '13px' }}>
              <label className="form-label" style={{ fontWeight: 600, fontSize: '0.84rem' }}>
                Work Email Address
              </label>
              <div className="input-icon-wrapper">
                <Mail size={16} className="input-prefix-icon" />
                <input
                  type="email"
                  className="form-control"
                  placeholder="alex@agency.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
            </div>

            <div className="form-group" style={{ marginBottom: '13px' }}>
              <label className="form-label" style={{ fontWeight: 600, fontSize: '0.84rem' }}>
                Agency / Workspace Name
              </label>
              <div className="input-icon-wrapper">
                <Building2 size={16} className="input-prefix-icon" />
                <input
                  type="text"
                  className="form-control"
                  placeholder="Acme Digital Agency"
                  value={tenantName}
                  onChange={(e) => setTenantName(e.target.value)}
                  required
                />
              </div>
              {tenantName && (
                <div style={{ fontSize: '0.73rem', color: '#64748b', marginTop: '4px' }}>
                  Workspace identifier: <code style={{ color: '#b8860b' }}>contentiq.ai/{tenantName.toLowerCase().replace(/\s+/g, '-')}</code>
                </div>
              )}
            </div>

            <div className="form-group" style={{ marginBottom: '16px' }}>
              <label className="form-label" style={{ fontWeight: 600, fontSize: '0.84rem' }}>
                Security Password (Min 6 chars)
              </label>
              <div className="input-icon-wrapper">
                <Lock size={16} className="input-prefix-icon" />
                <input
                  type={showPassword ? 'text' : 'password'}
                  className="form-control"
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  minLength={6}
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

            {/* Interactive Subscription Plan Selector */}
            <div style={{ marginBottom: '16px' }}>
              <label className="form-label" style={{ fontWeight: 600, fontSize: '0.84rem' }}>
                Select Workspace Tier
              </label>
              <div className="plan-grid">
                {PLANS.map((p) => {
                  const isSelected = plan === p.id;
                  return (
                    <div
                      key={p.id}
                      className={`plan-tile ${isSelected ? 'active' : ''}`}
                      onClick={() => setPlan(p.id)}
                    >
                      <div className="plan-tile-name">{p.name}</div>
                      <div className="plan-tile-badge">{p.badge}</div>
                      <div style={{ fontSize: '0.67rem', color: '#64748b', marginTop: '3px' }}>
                        {p.desc}
                      </div>
                    </div>
                  );
                })}
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
                  <UserPlus size={18} />
                  <span>Deploy Agency Workspace</span>
                  <ArrowRight size={16} style={{ marginLeft: '4px' }} />
                </>
              )}
            </button>
          </form>

          <div className="auth-bottom-switch">
            Already have an active agency tenant?
            <Link to="/login">Sign In to Agency</Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Register;
