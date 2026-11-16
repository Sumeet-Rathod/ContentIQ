import React, { useState, useEffect } from 'react';
import { intelligenceApi } from '../services/api';
import TopBar from '../components/TopBar';
import {
  ResponsiveContainer,
  ComposedChart,
  Line,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid
} from 'recharts';
import {
  LineChart as LineChartIcon,
  TrendingUp,
  Plus,
  Upload,
  AlertTriangle,
  CheckCircle2,
  Calendar,
  Sparkles,
  Users,
  Instagram,
  Linkedin,
  Youtube,
  ShieldCheck
} from 'lucide-react';

const FollowerForecast = () => {
  const [platform, setPlatform] = useState('instagram');
  const [daysAhead, setDaysAhead] = useState(30);
  const [forecastData, setForecastData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Manual Entry State
  const [snapshotDate, setSnapshotDate] = useState(new Date().toISOString().split('T')[0]);
  const [followerCount, setFollowerCount] = useState('');
  const [entryLoading, setEntryLoading] = useState(false);

  const fetchForecast = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await intelligenceApi.getForecast(platform, daysAhead);
      setForecastData(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch Prophet follower forecast.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchForecast();
  }, [platform, daysAhead]);

  const handleManualAdd = async (e) => {
    e.preventDefault();
    if (!followerCount || isNaN(followerCount)) {
      setError('Please provide a valid follower count.');
      return;
    }

    setEntryLoading(true);
    setError('');
    setSuccess('');

    try {
      await intelligenceApi.addSnapshot({
        platform,
        date: snapshotDate,
        follower_count: parseInt(followerCount, 10),
      });
      setSuccess(`Snapshot for ${snapshotDate} added to time-series store!`);
      setFollowerCount('');
      fetchForecast();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to add snapshot.');
    } finally {
      setEntryLoading(false);
    }
  };

  // Seed 60-day historical demo data helper
  const handleSeedHistoricalDemo = async () => {
    setEntryLoading(true);
    setError('');
    setSuccess('');

    try {
      const today = new Date();
      let count = platform === 'linkedin' ? 8500 : platform === 'youtube' ? 24000 : 15200;
      
      for (let i = 60; i >= 0; i--) {
        const d = new Date(today);
        d.setDate(d.getDate() - i);
        const dtStr = d.toISOString().split('T')[0];
        count += Math.floor(Math.random() * 35) + 12;
        await intelligenceApi.addSnapshot({
          platform,
          date: dtStr,
          follower_count: count,
        });
      }
      setSuccess(`Successfully seeded 60 days of historical snapshots for ${platform.toUpperCase()}!`);
      fetchForecast();
    } catch (err) {
      setError('Failed to seed demo data: ' + err.message);
    } finally {
      setEntryLoading(false);
    }
  };

  return (
    <div className="main-wrapper">
      <TopBar title="Prophet Follower Time-Series Forecasting" />

      <div className="content-body">
        {/* Executive Hero Banner */}
        <div className="page-hero-banner">
          <div className="page-hero-content">
            <div className="page-hero-tag">
              <Sparkles size={12} /> Time-Series Prophet Forecasting (M6)
            </div>
            <h1 className="page-hero-title">
              Audience Growth Trajectory & Forecast
            </h1>
            <p className="page-hero-subtitle">
              Decompose longitudinal follower counts into non-linear growth trends, weekly seasonality harmonics, and 80% Bayesian uncertainty confidence intervals.
            </p>
          </div>
          <div className="page-hero-actions">
            <button
              onClick={handleSeedHistoricalDemo}
              className="btn btn-gold btn-sm"
              disabled={entryLoading}
              style={{ boxShadow: '0 4px 12px rgba(184, 134, 11, 0.3)' }}
            >
              <Sparkles size={14} /> Seed 60-Day Viva History
            </button>
          </div>
        </div>

        {/* Filter & Controls Bar */}
        <div className="interactive-card" style={{ padding: '14px 20px', marginBottom: '18px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '14px' }}>
            {/* Platform Selector Pills */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span style={{ fontSize: '0.78rem', fontWeight: 700, color: '#1f3864', textTransform: 'uppercase' }}>
                Channel:
              </span>
              <div className="pill-filter-bar">
                {[
                  { id: 'instagram', label: 'Instagram', icon: Instagram },
                  { id: 'linkedin', label: 'LinkedIn', icon: Linkedin },
                  { id: 'youtube', label: 'YouTube', icon: Youtube },
                ].map((p) => {
                  const Icon = p.icon;
                  return (
                    <button
                      key={p.id}
                      type="button"
                      className={`pill-filter-btn ${platform === p.id ? 'active' : ''}`}
                      onClick={() => setPlatform(p.id)}
                    >
                      <Icon size={14} />
                      {p.label}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Forecast Horizon Pills */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span style={{ fontSize: '0.78rem', fontWeight: 700, color: '#1f3864', textTransform: 'uppercase' }}>
                Horizon:
              </span>
              <div className="pill-filter-bar">
                {[
                  { val: 30, label: '30 Days' },
                  { val: 60, label: '60 Days' },
                  { val: 90, label: '90 Days' },
                ].map((h) => (
                  <button
                    key={h.val}
                    type="button"
                    className={`pill-filter-btn ${daysAhead === h.val ? 'active' : ''}`}
                    onClick={() => setDaysAhead(h.val)}
                  >
                    {h.label}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {error && (
          <div className="alert alert-danger" style={{ marginBottom: '16px' }}>
            <AlertTriangle size={18} />
            <span>{error}</span>
          </div>
        )}

        {success && (
          <div className="alert alert-success" style={{ marginBottom: '16px' }}>
            <CheckCircle2 size={18} />
            <span>{success}</span>
          </div>
        )}

        {/* Insufficient Data State */}
        {forecastData?.status === 'insufficient_data' && (
          <div className="interactive-card" style={{ padding: '40px 20px', textAlign: 'center', background: '#fffbeb', border: '1px solid #fef3c7', marginBottom: '20px' }}>
            <div
              style={{
                width: '52px',
                height: '52px',
                borderRadius: '50%',
                background: '#fef3c7',
                color: '#d97706',
                display: 'inline-flex',
                alignItems: 'center',
                justifyContent: 'center',
                marginBottom: '14px',
              }}
            >
              <AlertTriangle size={26} />
            </div>
            <h3 style={{ fontSize: '1.2rem', fontWeight: 800, color: '#92400e', marginBottom: '8px' }}>
              Insufficient Time-Series Snapshots for Prophet
            </h3>
            <p style={{ maxWidth: '500px', margin: '0 auto 18px', color: '#b45309', fontSize: '0.88rem', lineHeight: 1.5 }}>
              {forecastData.message}
            </p>
            <button onClick={handleSeedHistoricalDemo} className="btn btn-gold" disabled={entryLoading}>
              <Sparkles size={16} /> Seed 60-Day History for {platform.toUpperCase()} Demo
            </button>
          </div>
        )}

        {/* Success Forecast Visualizations */}
        {forecastData?.status === 'success' && (
          <div>
            {/* KPI Summary Cards */}
            <div className="kpi-cards-grid" style={{ gridTemplateColumns: 'repeat(4, 1fr)', marginBottom: '20px' }}>
              <div className="kpi-card" style={{ borderTop: '4px solid #1f3864' }}>
                <div className="kpi-card-header">
                  <span className="kpi-card-title">Current Baseline</span>
                  <div className="kpi-icon-box" style={{ background: '#eff6ff', color: '#1d4ed8' }}>
                    <Users size={16} />
                  </div>
                </div>
                <div className="kpi-card-value" style={{ color: '#1f3864' }}>
                  {forecastData.current_followers.toLocaleString()}
                </div>
                <div className="kpi-card-footer">
                  <span className="kpi-trend-pill" style={{ background: '#eff6ff', color: '#1d4ed8' }}>
                    {platform.toUpperCase()}
                  </span>
                  <span className="kpi-footer-text">Verified Count</span>
                </div>
              </div>

              <div className="kpi-card" style={{ borderTop: '4px solid #b8860b' }}>
                <div className="kpi-card-header">
                  <span className="kpi-card-title">{daysAhead}-Day Projection</span>
                  <div className="kpi-icon-box" style={{ background: '#fefce8', color: '#ca8a04' }}>
                    <TrendingUp size={16} />
                  </div>
                </div>
                <div className="kpi-card-value" style={{ color: '#b8860b' }}>
                  {forecastData.projected_30d_followers.toLocaleString()}
                </div>
                <div className="kpi-card-footer">
                  <span className="kpi-trend-pill" style={{ background: '#fefce8', color: '#a16207' }}>
                    yhat Expected
                  </span>
                  <span className="kpi-footer-text">End Horizon</span>
                </div>
              </div>

              <div className="kpi-card" style={{ borderTop: '4px solid #16a34a' }}>
                <div className="kpi-card-header">
                  <span className="kpi-card-title">Projected Growth</span>
                  <div className="kpi-icon-box" style={{ background: '#f0fdf4', color: '#16a34a' }}>
                    <TrendingUp size={16} />
                  </div>
                </div>
                <div className="kpi-card-value" style={{ color: '#16a34a' }}>
                  +{forecastData.projected_growth_rate}%
                </div>
                <div className="kpi-card-footer">
                  <span className="kpi-trend-pill" style={{ background: '#f0fdf4', color: '#15803d' }}>
                    +{((forecastData.projected_30d_followers - forecastData.current_followers) / daysAhead).toFixed(0)}/day
                  </span>
                  <span className="kpi-footer-text">Velocity</span>
                </div>
              </div>

              <div className="kpi-card" style={{ borderTop: '4px solid #0284c7' }}>
                <div className="kpi-card-header">
                  <span className="kpi-card-title">Trend Trajectory</span>
                  <div className="kpi-icon-box" style={{ background: '#f0f9ff', color: '#0284c7' }}>
                    <ShieldCheck size={16} />
                  </div>
                </div>
                <div className="kpi-card-value" style={{ color: '#0284c7', textTransform: 'capitalize', fontSize: '1.5rem' }}>
                  {forecastData.trend_direction}
                </div>
                <div className="kpi-card-footer">
                  <span className="kpi-trend-pill" style={{ background: '#f0f9ff', color: '#0369a1' }}>
                    80% Bayesian
                  </span>
                  <span className="kpi-footer-text">Confidence</span>
                </div>
              </div>
            </div>

            {/* Prophet Forecast Chart with Confidence Band */}
            <div className="interactive-card" style={{ marginBottom: '20px' }}>
              <div className="card-top-header">
                <div>
                  <h4 className="card-top-title">
                    Facebook Prophet Follower Trajectory & 80% Bayesian Interval
                  </h4>
                  <div className="card-top-subtitle">
                    Solid Blue: Historical Actual | Dashed Gold: Expected (yhat) | Gold Area: 80% Confidence Band
                  </div>
                </div>
                <span className="chart-badge-pill">Additive Decomp</span>
              </div>

              <div style={{ width: '100%', height: 330 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <ComposedChart data={forecastData.timeline} margin={{ top: 10, right: 30, left: 10, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                    <XAxis
                      dataKey="date"
                      tick={{ fontSize: 11, fill: '#64748b' }}
                      tickFormatter={(val) => val.slice(5)}
                    />
                    <YAxis
                      domain={['auto', 'auto']}
                      tick={{ fontSize: 11, fill: '#64748b' }}
                      tickFormatter={(val) => `${(val / 1000).toFixed(1)}k`}
                    />
                    <Tooltip
                      formatter={(val, name) => [
                        val ? val.toLocaleString() : 'N/A',
                        name === 'actual'
                          ? 'Historical Actual'
                          : name === 'yhat'
                          ? 'Prophet Expected (yhat)'
                          : name === 'yhat_upper'
                          ? 'Upper Bound (80%)'
                          : 'Lower Bound (80%)',
                      ]}
                    />
                    <Legend />
                    <Area
                      type="monotone"
                      dataKey="yhat_upper"
                      stroke="none"
                      fill="#fef3c7"
                      fillOpacity={0.6}
                      name="Confidence Band"
                    />
                    <Area
                      type="monotone"
                      dataKey="yhat_lower"
                      stroke="none"
                      fill="#ffffff"
                      fillOpacity={1.0}
                    />
                    <Line
                      type="monotone"
                      dataKey="actual"
                      stroke="#1f3864"
                      strokeWidth={2.5}
                      dot={{ r: 2 }}
                      name="Actual Followers"
                      connectNulls={false}
                    />
                    <Line
                      type="monotone"
                      dataKey="yhat"
                      stroke="#b8860b"
                      strokeWidth={2.5}
                      strokeDasharray="4 4"
                      dot={false}
                      name="Prophet Forecast (yhat)"
                    />
                  </ComposedChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        )}

        {/* Manual Record Form */}
        <div className="interactive-card">
          <div className="card-top-header">
            <div>
              <h4 className="card-top-title">Record Daily Snapshot Telemetry</h4>
              <div className="card-top-subtitle">Add manual data points to extend the longitudinal time-series store</div>
            </div>
          </div>
          <form onSubmit={handleManualAdd} style={{ display: 'flex', gap: '16px', alignItems: 'flex-end', flexWrap: 'wrap' }}>
            <div style={{ flex: 1, minWidth: '180px' }}>
              <label className="form-label" style={{ fontWeight: 700 }}>Observation Date</label>
              <input
                type="date"
                className="form-control"
                value={snapshotDate}
                onChange={(e) => setSnapshotDate(e.target.value)}
                required
              />
            </div>

            <div style={{ flex: 1, minWidth: '180px' }}>
              <label className="form-label" style={{ fontWeight: 700 }}>Follower Count</label>
              <input
                type="number"
                className="form-control"
                placeholder="e.g. 15420"
                value={followerCount}
                onChange={(e) => setFollowerCount(e.target.value)}
                required
              />
            </div>

            <button type="submit" className="btn btn-gold" disabled={entryLoading} style={{ padding: '10px 18px' }}>
              <Plus size={16} /> Save Daily Record
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default FollowerForecast;
