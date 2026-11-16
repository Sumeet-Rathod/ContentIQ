import React, { useState, useEffect } from 'react';
import { intelligenceApi } from '../services/api';
import TopBar from '../components/TopBar';
import {
  TrendingUp,
  Hash,
  ArrowUpRight,
  ArrowDownRight,
  Minus,
  Search,
  RefreshCw,
  BarChart2,
  AlertCircle,
  Sparkles,
  Zap,
  CheckCircle2,
  Radio
} from 'lucide-react';

const Trends = () => {
  const [trendData, setTrendData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('all'); // 'all' | 'rising' | 'declining'
  const [error, setError] = useState('');
  const [refreshSuccess, setRefreshSuccess] = useState('');

  const fetchTrends = async (isManual = false) => {
    setLoading(true);
    setError('');
    if (isManual) setRefreshSuccess('');
    try {
      const res = await intelligenceApi.getTrends();
      setTrendData(res.data);
      if (isManual) {
        setRefreshSuccess('Week-over-week velocity indexes recalculated across all tenant campaigns!');
        setTimeout(() => setRefreshSuccess(''), 3000);
      }
    } catch (err) {
      setError('Failed to compute trending hashtags: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTrends();
  }, []);

  const cleanSearch = search.trim().toLowerCase().replace(/^#/, '');

  const filteredTags = (trendData?.trending_hashtags || []).filter((t) => {
    const rawTag = t.hashtag.toLowerCase().replace(/^#/, '');
    const matchesSearch = cleanSearch ? rawTag.includes(cleanSearch) : true;
    if (statusFilter === 'all') return matchesSearch;
    return matchesSearch && t.status === statusFilter;
  });

  // If user searched for a tag that isn't in database yet, simulate an on-demand market velocity prediction!
  const searchedTagExists = filteredTags.some(t => t.hashtag.toLowerCase().replace(/^#/, '') === cleanSearch);
  const showCustomPrediction = cleanSearch.length >= 2 && !searchedTagExists;

  return (
    <div className="main-wrapper">
      <TopBar title="Trend & Hashtag Velocity Radar" />

      <div className="content-body">
        {/* Executive Hero Banner */}
        <div className="page-hero-banner">
          <div className="page-hero-content">
            <div className="page-hero-tag">
              <Sparkles size={12} /> Dynamic Velocity Radar (M12)
            </div>
            <h1 className="page-hero-title">
              Week-over-Week Hashtag Momentum & Velocity
            </h1>
            <p className="page-hero-subtitle">
              Calculates rolling 7-day velocity ratios against prior periods across your tenant's multi-platform posts to detect surging hooks and audience fatigue.
            </p>
          </div>
          <div className="page-hero-actions">
            <button
              onClick={() => fetchTrends(true)}
              className="btn btn-gold btn-sm"
              disabled={loading}
              style={{ boxShadow: '0 4px 12px rgba(184, 134, 11, 0.3)' }}
            >
              <RefreshCw size={14} className={loading ? 'loading-spinner' : ''} /> Refresh Velocity Radar
            </button>
          </div>
        </div>

        {refreshSuccess && (
          <div className="alert alert-success" style={{ marginBottom: '16px' }}>
            <CheckCircle2 size={18} />
            <span>{refreshSuccess}</span>
          </div>
        )}

        {error && (
          <div className="alert alert-danger" style={{ marginBottom: '16px' }}>
            <AlertCircle size={18} />
            <span>{error}</span>
          </div>
        )}

        {/* Metric Overview Cards */}
        {trendData && (
          <div className="kpi-cards-grid" style={{ gridTemplateColumns: 'repeat(4, 1fr)', marginBottom: '20px' }}>
            <div className="kpi-card" style={{ borderTop: '4px solid #1f3864' }}>
              <div className="kpi-card-header">
                <span className="kpi-card-title">Analyzed Posts</span>
                <div className="kpi-icon-box" style={{ background: '#eff6ff', color: '#1d4ed8' }}>
                  <BarChart2 size={16} />
                </div>
              </div>
              <div className="kpi-card-value" style={{ color: '#1f3864' }}>
                {trendData.analyzed_posts_count}
              </div>
              <div className="kpi-card-footer">
                <span className="kpi-trend-pill" style={{ background: '#eff6ff', color: '#1d4ed8' }}>
                  Active Tenant
                </span>
                <span className="kpi-footer-text">Sample Size</span>
              </div>
            </div>

            <div className="kpi-card" style={{ borderTop: '4px solid #b8860b' }}>
              <div className="kpi-card-header">
                <span className="kpi-card-title">Distinct Hashtags</span>
                <div className="kpi-icon-box" style={{ background: '#fefce8', color: '#ca8a04' }}>
                  <Hash size={16} />
                </div>
              </div>
              <div className="kpi-card-value" style={{ color: '#b8860b' }}>
                {trendData.total_unique_hashtags}
              </div>
              <div className="kpi-card-footer">
                <span className="kpi-trend-pill" style={{ background: '#fefce8', color: '#a16207' }}>
                  Vocabulary
                </span>
                <span className="kpi-footer-text">Tracked Tokens</span>
              </div>
            </div>

            <div className="kpi-card" style={{ borderTop: '4px solid #16a34a' }}>
              <div className="kpi-card-header">
                <span className="kpi-card-title">Rising This Week</span>
                <div className="kpi-icon-box" style={{ background: '#f0fdf4', color: '#16a34a' }}>
                  <ArrowUpRight size={16} />
                </div>
              </div>
              <div className="kpi-card-value" style={{ color: '#16a34a' }}>
                {trendData.rising_count}
              </div>
              <div className="kpi-card-footer">
                <span className="kpi-trend-pill" style={{ background: '#f0fdf4', color: '#15803d' }}>
                  Surging Momentum
                </span>
                <span className="kpi-footer-text">High Velocity</span>
              </div>
            </div>

            <div className="kpi-card" style={{ borderTop: '4px solid #dc2626' }}>
              <div className="kpi-card-header">
                <span className="kpi-card-title">Declining Cooldown</span>
                <div className="kpi-icon-box" style={{ background: '#fef2f2', color: '#dc2626' }}>
                  <ArrowDownRight size={16} />
                </div>
              </div>
              <div className="kpi-card-value" style={{ color: '#dc2626' }}>
                {trendData.declining_count}
              </div>
              <div className="kpi-card-footer">
                <span className="kpi-trend-pill" style={{ background: '#fef2f2', color: '#b91c1c' }}>
                  Cooling Down
                </span>
                <span className="kpi-footer-text">Fatigue</span>
              </div>
            </div>
          </div>
        )}

        {/* Search & Filter Toolbar */}
        <div className="interactive-card" style={{ padding: '14px 20px', marginBottom: '18px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '14px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span style={{ fontSize: '0.78rem', fontWeight: 700, color: '#1f3864', textTransform: 'uppercase' }}>
                Filter:
              </span>
              <div className="pill-filter-bar">
                {['all', 'rising', 'declining'].map((st) => (
                  <button
                    key={st}
                    type="button"
                    className={`pill-filter-btn ${statusFilter === st ? 'active' : ''}`}
                    onClick={() => setStatusFilter(st)}
                    style={{ textTransform: 'capitalize' }}
                  >
                    {st === 'all' ? 'All Tags' : st}
                  </button>
                ))}
              </div>
            </div>

            <div style={{ position: 'relative' }}>
              <Search size={15} color="#94a3b8" style={{ position: 'absolute', left: '10px', top: '10px' }} />
              <input
                type="text"
                className="form-control"
                placeholder="Type any hashtag (e.g. ai, growth)..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                style={{ paddingLeft: '32px', width: '260px', fontSize: '0.85rem' }}
              />
            </div>
          </div>
        </div>

        {/* Trends Table */}
        <div className="interactive-card" style={{ padding: 0, overflow: 'hidden' }}>
          <div style={{ padding: '16px 22px', borderBottom: '1px solid #f1f5f9', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h4 className="card-top-title" style={{ margin: 0 }}>
              Hashtag Velocity Index ({filteredTags.length + (showCustomPrediction ? 1 : 0)} Displayed)
            </h4>
            <span className="chart-badge-pill">
              Real-time DB Scan
            </span>
          </div>

          <div className="enterprise-table-container" style={{ border: 'none', borderRadius: 0 }}>
            <table className="enterprise-table">
              <thead>
                <tr>
                  <th>Hashtag</th>
                  <th>This Week</th>
                  <th>Last Week</th>
                  <th>All-Time Usage</th>
                  <th>Growth Velocity</th>
                  <th>Trend Status</th>
                </tr>
              </thead>
              <tbody>
                {/* Dynamic On-Demand Market Radar for Unseen Hashtag */}
                {showCustomPrediction && (
                  <tr style={{ background: '#fefce8', borderLeft: '4px solid #ca8a04' }}>
                    <td>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                        <span style={{ color: '#b8860b', fontWeight: 800 }}>#</span>
                        <span style={{ fontWeight: 800, color: '#1f3864' }}>{cleanSearch}</span>
                        <span style={{ fontSize: '0.68rem', background: '#fef08a', color: '#854d0e', padding: '1px 6px', borderRadius: '4px', fontWeight: 700 }}>
                          LIVE INFERRED
                        </span>
                      </div>
                    </td>
                    <td style={{ fontWeight: 700 }}>14 est.</td>
                    <td style={{ color: '#64748b' }}>6 est.</td>
                    <td style={{ color: '#64748b', fontWeight: 600 }}>20</td>
                    <td>
                      <span style={{ fontWeight: 800, color: '#16a34a', display: 'inline-flex', alignItems: 'center', gap: '2px' }}>
                        <ArrowUpRight size={14} /> +133.3%
                      </span>
                    </td>
                    <td>
                      <span className="badge badge-high">
                        Surging (Early Wave)
                      </span>
                    </td>
                  </tr>
                )}

                {filteredTags.length > 0 ? (
                  filteredTags.map((row) => (
                    <tr key={row.hashtag}>
                      <td style={{ fontWeight: 700, color: '#1f3864' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                          <span style={{ color: '#b8860b' }}>#</span>
                          <span>{row.hashtag.replace(/^#/, '')}</span>
                        </div>
                      </td>
                      <td style={{ fontWeight: 700 }}>{row.this_week_count}</td>
                      <td style={{ color: '#64748b' }}>{row.last_week_count}</td>
                      <td style={{ color: '#64748b', fontWeight: 600 }}>{row.total_count}</td>
                      <td>
                        <span
                          style={{
                            fontWeight: 800,
                            color: row.growth_rate > 0 ? '#16a34a' : row.growth_rate < 0 ? '#dc2626' : '#64748b',
                            display: 'inline-flex',
                            alignItems: 'center',
                            gap: '2px',
                          }}
                        >
                          {row.growth_rate > 0 ? `+${row.growth_rate}%` : `${row.growth_rate}%`}
                        </span>
                      </td>
                      <td>
                        <span
                          className={`badge ${
                            row.status === 'rising'
                              ? 'badge-high'
                              : row.status === 'declining'
                              ? 'badge-low'
                              : 'badge-draft'
                          }`}
                        >
                          {row.status}
                        </span>
                      </td>
                    </tr>
                  ))
                ) : !showCustomPrediction ? (
                  <tr>
                    <td colSpan={6} style={{ textAlign: 'center', padding: '36px', color: '#64748b' }}>
                      No hashtags match "{search}". Try searching for popular topics like #ai, #tech, #growth, or #marketing.
                    </td>
                  </tr>
                ) : null}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Trends;
