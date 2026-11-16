import React, { useState, useEffect } from 'react';
import { feedbackApi, postsApi } from '../services/api';
import TopBar from '../components/TopBar';
import {
  Split,
  Plus,
  Trophy,
  CheckCircle2,
  AlertCircle,
  TrendingUp,
  X,
  Layers,
  Sparkles,
  Zap,
  BarChart2,
  Check
} from 'lucide-react';

const ABTesting = () => {
  const [experiments, setExperiments] = useState([]);
  const [availablePosts, setAvailablePosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showCreateModal, setShowCreateModal] = useState(false);

  // Form State
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [selectedPostIds, setSelectedPostIds] = useState([]);
  const [createLoading, setCreateLoading] = useState(false);

  const fetchExperimentsAndPosts = async () => {
    setLoading(true);
    setError('');
    try {
      const [expRes, postRes] = await Promise.all([
        feedbackApi.getABTests(),
        postsApi.getPosts({ status: 'all' }),
      ]);
      setExperiments(expRes.data);
      setAvailablePosts(postRes.data);
    } catch (err) {
      setError('Failed to fetch A/B tests or posts.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchExperimentsAndPosts();
  }, []);

  const handleTogglePostSelect = (id) => {
    if (selectedPostIds.includes(id)) {
      setSelectedPostIds(selectedPostIds.filter((p) => p !== id));
    } else {
      if (selectedPostIds.length >= 3) {
        alert('A/B tests support up to 3 variants simultaneously.');
        return;
      }
      setSelectedPostIds([...selectedPostIds, id]);
    }
  };

  const handleCreateExperiment = async (e) => {
    e.preventDefault();
    if (selectedPostIds.length < 2) {
      alert('Please select at least 2 post variants to compare.');
      return;
    }
    setCreateLoading(true);
    try {
      await feedbackApi.createABTest({
        title,
        description,
        variant_post_ids: selectedPostIds,
      });
      setShowCreateModal(false);
      setTitle('');
      setDescription('');
      setSelectedPostIds([]);
      fetchExperimentsAndPosts();
    } catch (err) {
      alert('Failed to create experiment: ' + (err.response?.data?.detail || err.message));
    } finally {
      setCreateLoading(false);
    }
  };

  return (
    <div className="main-wrapper">
      <TopBar title="A/B Variant Testing & Optimization Arena" />

      <div className="content-body">
        {/* Executive Hero Banner */}
        <div className="page-hero-banner">
          <div className="page-hero-content">
            <div className="page-hero-tag">
              <Sparkles size={12} /> Statistical Hypothesis Testing (M13)
            </div>
            <h1 className="page-hero-title">
              A/B Content Variant Split-Testing Arena
            </h1>
            <p className="page-hero-subtitle">
              Pitting multi-variant headlines, creative thumbnails, and hashtag densities against real audience engagement to declare statistically significant winners.
            </p>
          </div>
          <div className="page-hero-actions">
            <button
              onClick={() => setShowCreateModal(true)}
              className="btn btn-gold btn-sm"
              style={{ boxShadow: '0 4px 12px rgba(184, 134, 11, 0.3)' }}
            >
              <Plus size={15} /> Launch New Experiment
            </button>
          </div>
        </div>

        {error && (
          <div className="alert alert-danger" style={{ marginBottom: '16px' }}>
            <AlertCircle size={18} />
            <span>{error}</span>
          </div>
        )}

        {/* Experiment Cards */}
        {loading ? (
          <div style={{ textAlign: 'center', padding: '60px' }}>
            <div className="loading-spinner"></div>
          </div>
        ) : experiments.length > 0 ? (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
            {experiments.map((exp) => (
              <div key={exp.id} className="interactive-card" style={{ padding: '24px' }}>
                <div className="card-top-header" style={{ marginBottom: '18px' }}>
                  <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <Split size={18} color="#b8860b" />
                      <h3 className="card-top-title" style={{ fontSize: '1.15rem' }}>
                        {exp.title}
                      </h3>
                    </div>
                    {exp.description && (
                      <p className="card-top-subtitle" style={{ marginLeft: '26px' }}>
                        {exp.description}
                      </p>
                    )}
                  </div>
                  <div>
                    {exp.winner_post_id ? (
                      <span className="badge badge-high" style={{ display: 'inline-flex', alignItems: 'center', gap: '5px', padding: '5px 12px', fontSize: '0.8rem', fontWeight: 700 }}>
                        <Trophy size={14} /> Statistical Winner Declared
                      </span>
                    ) : (
                      <span className="badge badge-scheduled" style={{ padding: '5px 12px', fontSize: '0.8rem' }}>
                        Experiment Active
                      </span>
                    )}
                  </div>
                </div>

                {/* Variants Grid */}
                <div style={{ display: 'grid', gridTemplateColumns: `repeat(${exp.variants.length}, 1fr)`, gap: '16px' }}>
                  {exp.variants.map((v, idx) => (
                    <div
                      key={v.post_id}
                      style={{
                        padding: '16px',
                        background: v.is_winner ? 'linear-gradient(180deg, #fefce8 0%, #ffffff 100%)' : '#f8fafc',
                        border: v.is_winner ? '2px solid #b8860b' : '1px solid #e2e8f0',
                        borderRadius: '12px',
                        boxShadow: v.is_winner ? '0 8px 20px -4px rgba(184, 134, 11, 0.15)' : 'none',
                        position: 'relative',
                        display: 'flex',
                        flexDirection: 'column',
                        justifyContent: 'space-between',
                      }}
                    >
                      <div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                          <span style={{ fontWeight: 800, color: '#1f3864', fontSize: '0.92rem' }}>
                            Variant {String.fromCharCode(65 + idx)} ({v.platform})
                          </span>
                          {v.is_winner && (
                            <span style={{ color: '#b8860b', fontWeight: 800, fontSize: '0.78rem', display: 'flex', alignItems: 'center', gap: '4px', background: '#fef3c7', padding: '2px 8px', borderRadius: '9999px' }}>
                              <Trophy size={13} /> TOP PERFORMER
                            </span>
                          )}
                        </div>

                        <p style={{ fontSize: '0.88rem', color: '#334155', fontStyle: 'italic', marginBottom: '14px', lineHeight: 1.45 }}>
                          "{v.caption}"
                        </p>
                      </div>

                      <div style={{ background: '#ffffff', padding: '12px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.82rem', marginBottom: '6px' }}>
                          <span style={{ color: '#64748b', fontWeight: 600 }}>Engagement Rate:</span>
                          <span style={{ fontWeight: 800, fontSize: '1rem', color: v.is_winner ? '#16a34a' : '#1f3864' }}>
                            {v.engagement_rate}%
                          </span>
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: '#64748b', borderTop: '1px solid #f1f5f9', paddingTop: '6px' }}>
                          <span>❤️ {v.likes}</span>
                          <span>💬 {v.comments}</span>
                          <span>👁️ {v.reach.toLocaleString()} reach</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="interactive-card" style={{ textAlign: 'center', padding: '60px 20px', color: '#64748b' }}>
            <Split size={48} color="#94a3b8" style={{ marginBottom: '14px' }} />
            <h3 style={{ fontSize: '1.2rem', fontWeight: 700, color: '#1f3864', marginBottom: '6px' }}>
              No Active A/B Experiments
            </h3>
            <p style={{ maxWidth: '400px', margin: '0 auto 18px', fontSize: '0.88rem', lineHeight: 1.5 }}>
              Group 2-3 content variants together to statistically measure which hook or caption drives maximum reach.
            </p>
            <button onClick={() => setShowCreateModal(true)} className="btn btn-gold">
              <Plus size={16} /> Create First A/B Test
            </button>
          </div>
        )}

        {/* Create Modal */}
        {showCreateModal && (
          <div className="modal-overlay" onClick={() => setShowCreateModal(false)}>
            <div className="modal-card" style={{ maxWidth: '640px', borderRadius: '16px' }} onClick={(e) => e.stopPropagation()}>
              <div className="card-header" style={{ borderBottom: '1px solid #f1f5f9', paddingBottom: '12px' }}>
                <h3 className="card-title" style={{ margin: 0 }}>Launch New A/B Content Experiment</h3>
                <button onClick={() => setShowCreateModal(false)} style={{ background: 'none', border: 'none', cursor: 'pointer', color: '#64748b' }}>
                  <X size={20} />
                </button>
              </div>

              <form onSubmit={handleCreateExperiment} style={{ marginTop: '16px' }}>
                <div className="form-group">
                  <label className="form-label" style={{ fontWeight: 700 }}>Experiment Title</label>
                  <input
                    type="text"
                    className="form-control"
                    placeholder="e.g. Emoji Hook vs Authoritative Hook"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    required
                  />
                </div>

                <div className="form-group">
                  <label className="form-label" style={{ fontWeight: 700 }}>Hypothesis / Description (Optional)</label>
                  <input
                    type="text"
                    className="form-control"
                    placeholder="Testing if shorter emojis increase Instagram engagement rate..."
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                  />
                </div>

                <div className="form-group">
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                    <label className="form-label" style={{ marginBottom: 0, fontWeight: 700 }}>
                      Select 2 or 3 Post Variants:
                    </label>
                    <span style={{ fontSize: '0.78rem', color: selectedPostIds.length >= 2 ? '#16a34a' : '#b8860b', fontWeight: 700 }}>
                      {selectedPostIds.length} of 3 selected
                    </span>
                  </div>

                  <div style={{ maxHeight: '220px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '8px', border: '1px solid #e2e8f0', borderRadius: '8px', padding: '8px' }}>
                    {availablePosts.map((p) => {
                      const isSelected = selectedPostIds.includes(p.id);
                      return (
                        <div
                          key={p.id}
                          onClick={() => handleTogglePostSelect(p.id)}
                          style={{
                            padding: '10px 12px',
                            borderRadius: '6px',
                            background: isSelected ? '#eff6ff' : '#ffffff',
                            border: isSelected ? '1.5px solid #2563eb' : '1px solid #e2e8f0',
                            cursor: 'pointer',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'space-between',
                            gap: '10px',
                          }}
                        >
                          <div style={{ flex: 1, overflow: 'hidden' }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '2px' }}>
                              <span style={{ fontWeight: 700, fontSize: '0.75rem', textTransform: 'uppercase', color: '#1f3864' }}>
                                {p.platform}
                              </span>
                              <span style={{ fontSize: '0.72rem', color: '#94a3b8' }}>
                                • {p.status}
                              </span>
                            </div>
                            <div style={{ fontSize: '0.84rem', color: '#334155', textOverflow: 'ellipsis', overflow: 'hidden', whiteSpace: 'nowrap' }}>
                              {p.caption}
                            </div>
                          </div>
                          {isSelected && (
                            <div style={{ width: '22px', height: '22px', borderRadius: '50%', background: '#2563eb', color: '#ffffff', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                              <Check size={14} />
                            </div>
                          )}
                        </div>
                      );
                    })}
                  </div>
                </div>

                <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px', marginTop: '20px' }}>
                  <button type="button" onClick={() => setShowCreateModal(false)} className="btn btn-secondary">
                    Cancel
                  </button>
                  <button type="submit" className="btn btn-gold" disabled={createLoading || selectedPostIds.length < 2}>
                    {createLoading ? <span className="loading-spinner"></span> : 'Launch Experiment'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ABTesting;
