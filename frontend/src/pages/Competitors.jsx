import React, { useState, useEffect } from 'react';
import { feedbackApi } from '../services/api';
import TopBar from '../components/TopBar';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Cell,
  CartesianGrid
} from 'recharts';
import {
  Users2,
  Plus,
  TrendingUp,
  AlertCircle,
  CheckCircle2,
  Instagram,
  Linkedin,
  Youtube,
  Sparkles,
  Trophy,
  ArrowUpRight,
  ArrowDownRight,
  Info,
  Calculator,
  Eye,
  Lock
} from 'lucide-react';

const Competitors = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Form State
  const [handle, setHandle] = useState('');
  const [platform, setPlatform] = useState('instagram');
  const [followers, setFollowers] = useState('');
  const [rate, setRate] = useState('');
  const [addLoading, setAddLoading] = useState(false);

  // Public Sampler Calculator State
  const [showCalculator, setShowCalculator] = useState(false);
  const [calcFollowers, setCalcFollowers] = useState('25000');
  const [calcLikes, setCalcLikes] = useState('750');
  const [calcComments, setCalcComments] = useState('110');

  const fetchCompetitors = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await feedbackApi.getCompetitors();
      setData(res.data);
    } catch (err) {
      setError('Failed to fetch competitor benchmarks: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCompetitors();
  }, []);

  const handleAddCompetitor = async (e) => {
    e.preventDefault();
    if (!handle || !rate) {
      alert('Please provide competitor handle and engagement rate.');
      return;
    }
    setAddLoading(true);
    setError('');
    setSuccess('');

    try {
      await feedbackApi.addCompetitor({
        handle: handle.startsWith('@') ? handle : `@${handle}`,
        platform,
        follower_count: parseInt(followers, 10) || 10000,
        engagement_rate: parseFloat(rate),
      });
      setSuccess(`Added benchmark for ${handle}!`);
      setHandle('');
      setFollowers('');
      setRate('');
      fetchCompetitors();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to save competitor.');
    } finally {
      setAddLoading(false);
    }
  };

  const calculateSampledER = () => {
    const f = parseFloat(calcFollowers) || 1;
    const l = parseFloat(calcLikes) || 0;
    const c = parseFloat(calcComments) || 0;
    return (((l + c) / f) * 100).toFixed(2);
  };

  const applyCalculatedER = () => {
    setFollowers(calcFollowers);
    setRate(calculateSampledER());
    setShowCalculator(false);
  };

  const quickAddPreset = (h, p, f, r) => {
    setHandle(h);
    setPlatform(p);
    setFollowers(f);
    setRate(r);
  };

  const getPlatformIcon = (plt) => {
    switch (plt?.toLowerCase()) {
      case 'instagram': return <Instagram size={14} color="#e1306c" />;
      case 'linkedin': return <Linkedin size={14} color="#0077b5" />;
      case 'youtube': return <Youtube size={14} color="#ef4444" />;
      default: return null;
    }
  };

  return (
    <div className="main-wrapper">
      <TopBar title="Competitor Benchmarking & Market Intelligence" />

      <div className="content-body">
        {/* Executive Hero Banner */}
        <div className="page-hero-banner">
          <div className="page-hero-content">
            <div className="page-hero-tag">
              <Sparkles size={12} /> Market Intelligence Deck
            </div>
            <h1 className="page-hero-title">
              Competitor Market Positioning & Share of Engagement
            </h1>
            <p className="page-hero-subtitle">
              Benchmark your tenant's cross-platform engagement rates against key industry competitors to discover market whitespace and organic traction advantages.
            </p>
          </div>
          <div className="page-hero-actions">
            {data && (
              <span className="kpi-trend-pill" style={{ background: 'rgba(184, 134, 11, 0.25)', color: '#fde047', border: '1px solid rgba(184, 134, 11, 0.4)', fontSize: '0.8rem', padding: '6px 12px' }}>
                Your Average: {data.tenant_average_engagement}% ER
              </span>
            )}
          </div>
        </div>

        {/* Methodology Disclosure Alert */}
        <div className="interactive-card" style={{ padding: '14px 18px', background: '#f8fafc', borderLeft: '4px solid #1f3864', marginBottom: '18px' }}>
          <div style={{ display: 'flex', alignItems: 'flex-start', gap: '10px' }}>
            <Info size={18} color="#1f3864" style={{ flexShrink: 0, marginTop: '2px' }} />
            <div style={{ fontSize: '0.82rem', color: '#475569', lineHeight: 1.5 }}>
              <strong style={{ color: '#1f3864' }}>How Competitor Benchmarks Are Calculated Without Private Credentials:</strong>
              <br />
              Commercial intelligence platforms (e.g. Rival IQ, Sprout Social) sample <em>publicly visible</em> post metrics. 
              The industry standard formula is:{' '}
              <span style={{ background: '#e2e8f0', padding: '2px 6px', borderRadius: '4px', fontWeight: 700, color: '#1e293b' }}>
                ER = [(Public Likes + Public Comments) ÷ Public Follower Count] × 100
              </span>. Zero private passwords or internal credentials required.
            </div>
          </div>
        </div>

        {error && (
          <div className="alert alert-danger" style={{ marginBottom: '16px' }}>
            <AlertCircle size={18} />
            <span>{error}</span>
          </div>
        )}

        {success && (
          <div className="alert alert-success" style={{ marginBottom: '16px' }}>
            <CheckCircle2 size={18} />
            <span>{success}</span>
          </div>
        )}

        {/* Comparison Chart Card */}
        {data && (
          <div className="interactive-card" style={{ marginBottom: '24px' }}>
            <div className="card-top-header">
              <div>
                <h3 className="card-top-title">
                  Cross-Tenant Engagement Rate Benchmark (%)
                </h3>
                <div className="card-top-subtitle">
                  Your tenant average (<b>{data.tenant_average_engagement}%</b>) vs competitor verified performance
                </div>
              </div>
              <span className="chart-badge-pill">
                Active Benchmark
              </span>
            </div>

            <div style={{ width: '100%', height: 270 }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={data.comparison_chart} margin={{ top: 10, right: 20, left: 0, bottom: 20 }}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                  <XAxis dataKey="name" tick={{ fontSize: 11, fill: '#475569', fontWeight: 600 }} interval={0} />
                  <YAxis tick={{ fontSize: 11, fill: '#64748b' }} unit="%" />
                  <Tooltip formatter={(val) => [`${val}%`, 'Engagement Rate']} />
                  <Bar dataKey="rate" radius={[6, 6, 0, 0]}>
                    {data.comparison_chart.map((entry, idx) => (
                      <Cell key={`cell-${idx}`} fill={entry.is_tenant ? '#b8860b' : '#1f3864'} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}

        {/* Add Competitor & Table Grid */}
        <div style={{ display: 'grid', gridTemplateColumns: '1.25fr 0.75fr', gap: '24px' }}>
          {/* Competitors List */}
          <div className="interactive-card" style={{ padding: 0, overflow: 'hidden' }}>
            <div style={{ padding: '16px 22px', borderBottom: '1px solid #f1f5f9' }}>
              <h4 className="card-top-title" style={{ margin: 0 }}>
                Tracked Industry Competitors ({data?.competitors?.length || 0})
              </h4>
            </div>

            <div className="enterprise-table-container" style={{ border: 'none', borderRadius: 0 }}>
              <table className="enterprise-table">
                <thead>
                  <tr>
                    <th>Competitor Handle</th>
                    <th>Platform</th>
                    <th>Followers</th>
                    <th>Engagement</th>
                    <th>Performance Delta</th>
                  </tr>
                </thead>
                <tbody>
                  {data?.competitors?.length > 0 ? (
                    data.competitors.map((c) => {
                      const diff = data.tenant_average_engagement - c.engagement_rate;
                      const isWinning = diff >= 0;
                      return (
                        <tr key={c.id}>
                          <td style={{ fontWeight: 700, color: '#1f3864' }}>{c.handle}</td>
                          <td>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                              {getPlatformIcon(c.platform)}
                              <span style={{ textTransform: 'capitalize', fontSize: '0.82rem' }}>{c.platform}</span>
                            </div>
                          </td>
                          <td style={{ color: '#64748b', fontWeight: 600 }}>{c.follower_count.toLocaleString()}</td>
                          <td style={{ fontWeight: 800, color: '#1f3864' }}>{c.engagement_rate}%</td>
                          <td>
                            {isWinning ? (
                              <span style={{ color: '#16a34a', fontWeight: 700, fontSize: '0.78rem', display: 'inline-flex', alignItems: 'center', gap: '3px', background: '#f0fdf4', padding: '3px 8px', borderRadius: '6px' }}>
                                <ArrowUpRight size={13} /> +{diff.toFixed(1)}% Higher
                              </span>
                            ) : (
                              <span style={{ color: '#dc2626', fontWeight: 700, fontSize: '0.78rem', display: 'inline-flex', alignItems: 'center', gap: '3px', background: '#fef2f2', padding: '3px 8px', borderRadius: '6px' }}>
                                <ArrowDownRight size={13} /> {Math.abs(diff).toFixed(1)}% Below
                              </span>
                            )}
                          </td>
                        </tr>
                      );
                    })
                  ) : (
                    <tr>
                      <td colSpan={5} style={{ textAlign: 'center', padding: '36px', color: '#64748b' }}>
                        No competitors tracked yet. Add rival handles on the right to track market benchmarks.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>

          {/* Add Competitor Form */}
          <div className="interactive-card">
            <div className="card-top-header">
              <div>
                <h4 className="card-top-title">Add Competitor Benchmark</h4>
                <div className="card-top-subtitle">Track a new brand or channel handle</div>
              </div>
              <button
                type="button"
                onClick={() => setShowCalculator(!showCalculator)}
                className="btn btn-secondary btn-sm"
                style={{ fontSize: '0.74rem', padding: '4px 8px' }}
              >
                <Calculator size={13} /> {showCalculator ? 'Hide Calculator' : 'Public Sampler'}
              </button>
            </div>

            {/* Public Sampler Mini-Calculator */}
            {showCalculator && (
              <div style={{ background: '#f8fafc', padding: '14px', borderRadius: '10px', border: '1px solid #e2e8f0', marginBottom: '16px' }}>
                <div style={{ fontSize: '0.76rem', fontWeight: 700, color: '#1f3864', marginBottom: '8px' }}>
                  Public Metrics Sampler (Average across last 5 posts):
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '8px', marginBottom: '10px' }}>
                  <div>
                    <label style={{ fontSize: '0.7rem', color: '#64748b' }}>Public Followers</label>
                    <input
                      type="number"
                      className="form-control"
                      style={{ fontSize: '0.8rem', padding: '4px 6px' }}
                      value={calcFollowers}
                      onChange={(e) => setCalcFollowers(e.target.value)}
                    />
                  </div>
                  <div>
                    <label style={{ fontSize: '0.7rem', color: '#64748b' }}>Avg. Likes</label>
                    <input
                      type="number"
                      className="form-control"
                      style={{ fontSize: '0.8rem', padding: '4px 6px' }}
                      value={calcLikes}
                      onChange={(e) => setCalcLikes(e.target.value)}
                    />
                  </div>
                  <div>
                    <label style={{ fontSize: '0.7rem', color: '#64748b' }}>Avg. Comments</label>
                    <input
                      type="number"
                      className="form-control"
                      style={{ fontSize: '0.8rem', padding: '4px 6px' }}
                      value={calcComments}
                      onChange={(e) => setCalcComments(e.target.value)}
                    />
                  </div>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ fontSize: '0.82rem', fontWeight: 800, color: '#1f3864' }}>
                    Computed ER: <span style={{ color: '#16a34a' }}>{calculateSampledER()}%</span>
                  </span>
                  <button type="button" onClick={applyCalculatedER} className="btn btn-gold btn-sm" style={{ fontSize: '0.74rem', padding: '3px 8px' }}>
                    Apply to Form
                  </button>
                </div>
              </div>
            )}

            {/* Quick Presets */}
            <div style={{ marginBottom: '14px' }}>
              <span style={{ fontSize: '0.74rem', color: '#64748b', fontWeight: 700, display: 'block', marginBottom: '6px' }}>
                ⚡ 1-Click Industry Benchmarks:
              </span>
              <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                <button
                  type="button"
                  onClick={() => quickAddPreset('@Canva', 'instagram', '48000', '3.8')}
                  className="sample-preset-chip"
                >
                  + @Canva (IG)
                </button>
                <button
                  type="button"
                  onClick={() => quickAddPreset('@NotionHQ', 'linkedin', '65000', '4.2')}
                  className="sample-preset-chip"
                >
                  + @NotionHQ (LI)
                </button>
                <button
                  type="button"
                  onClick={() => quickAddPreset('@Figma', 'youtube', '92000', '2.9')}
                  className="sample-preset-chip"
                >
                  + @Figma (YT)
                </button>
              </div>
            </div>

            <form onSubmit={handleAddCompetitor}>
              <div className="form-group">
                <label className="form-label" style={{ fontWeight: 700 }}>Competitor Handle</label>
                <input
                  type="text"
                  className="form-control"
                  placeholder="e.g. @innovatetech"
                  value={handle}
                  onChange={(e) => setHandle(e.target.value)}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label" style={{ fontWeight: 700 }}>Social Platform</label>
                <select
                  className="form-control"
                  value={platform}
                  onChange={(e) => setPlatform(e.target.value)}
                >
                  <option value="instagram">Instagram</option>
                  <option value="linkedin">LinkedIn</option>
                  <option value="youtube">YouTube</option>
                </select>
              </div>

              <div className="form-group">
                <label className="form-label" style={{ fontWeight: 700 }}>Follower Count</label>
                <input
                  type="number"
                  className="form-control"
                  placeholder="e.g. 24000"
                  value={followers}
                  onChange={(e) => setFollowers(e.target.value)}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label" style={{ fontWeight: 700 }}>Benchmark Engagement Rate (%)</label>
                <input
                  type="number"
                  step="0.01"
                  className="form-control"
                  placeholder="e.g. 4.2"
                  value={rate}
                  onChange={(e) => setRate(e.target.value)}
                  required
                />
              </div>

              <button
                type="submit"
                className="btn btn-gold"
                style={{ width: '100%', padding: '10px' }}
                disabled={addLoading}
              >
                {addLoading ? <span className="loading-spinner"></span> : <><Plus size={16} /> Track Competitor</>}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Competitors;
