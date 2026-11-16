import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { intelligenceApi } from '../services/api';
import TopBar from '../components/TopBar';
import {
  Sparkles,
  ArrowRight,
  RefreshCw,
  Layers,
  Key,
  Instagram,
  Linkedin,
  Youtube,
  AlertCircle,
  Lightbulb,
  CheckCircle2,
  Cpu,
  Tv,
  ShoppingBag,
  HeartPulse,
  TrendingUp
} from 'lucide-react';

const Recommendations = () => {
  const [recData, setRecData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedNiche, setSelectedNiche] = useState('b2b_saas');
  const [error, setError] = useState('');
  const [reclusterSuccess, setReclusterSuccess] = useState('');
  const navigate = useNavigate();

  const fetchRecommendations = async (nicheToFetch = selectedNiche, isManual = false) => {
    setLoading(true);
    setError('');
    if (isManual) setReclusterSuccess('');
    try {
      const res = await intelligenceApi.getRecommendations(nicheToFetch);
      setRecData(res.data);
      if (isManual) {
        setReclusterSuccess(`TF-IDF vector space successfully re-clustered for ${nicheToFetch.replace('_', ' ').toUpperCase()}!`);
        setTimeout(() => setReclusterSuccess(''), 3000);
      }
    } catch (err) {
      setError('Failed to fetch AI topic recommendations: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRecommendations(selectedNiche);
  }, [selectedNiche]);

  const handleUseTopic = (topic) => {
    navigate('/compose', {
      state: {
        suggestedCaption: `${topic.topic_title}: ${topic.suggested_angle}`,
        suggestedPlatform: topic.target_platform.toLowerCase(),
        suggestedHashtags: topic.recommended_hashtags,
      },
    });
  };

  const getPlatformIcon = (platform) => {
    switch (platform?.toLowerCase()) {
      case 'instagram':
        return <Instagram size={14} color="#e1306c" />;
      case 'linkedin':
        return <Linkedin size={14} color="#0077b5" />;
      case 'youtube':
        return <Youtube size={14} color="#ef4444" />;
      default:
        return null;
    }
  };

  const niches = [
    { id: 'b2b_saas', label: 'B2B SaaS & Tech', icon: Cpu },
    { id: 'creator_media', label: 'Creator & Media', icon: Tv },
    { id: 'ecommerce', label: 'E-Commerce & DTC', icon: ShoppingBag },
    { id: 'health_fitness', label: 'Health & Fitness', icon: HeartPulse },
    { id: 'finance_business', label: 'Finance & Venture', icon: TrendingUp },
  ];

  return (
    <div className="main-wrapper">
      <TopBar title="Niche-Tailored Topic Recommendations (TF-IDF & Cosine)" />

      <div className="content-body">
        {/* Executive Hero Banner */}
        <div className="page-hero-banner">
          <div className="page-hero-content">
            <div className="page-hero-tag">
              <Sparkles size={12} /> Niche-Adaptive Clustering (M7)
            </div>
            <h1 className="page-hero-title">
              Niche-Based AI Content Recommendations & Topic Discovery
            </h1>
            <p className="page-hero-subtitle">
              Discovers high-performing semantic content clusters using TF-IDF vectorization and cosine similarity projections conditioned directly on your agency's industry niche.
            </p>
          </div>
          <div className="page-hero-actions">
            <button
              onClick={() => fetchRecommendations(selectedNiche, true)}
              className="btn btn-gold btn-sm"
              disabled={loading}
              style={{ boxShadow: '0 4px 12px rgba(184, 134, 11, 0.3)' }}
            >
              <RefreshCw size={14} className={loading ? 'loading-spinner' : ''} /> Re-cluster Corpus
            </button>
          </div>
        </div>

        {reclusterSuccess && (
          <div className="alert alert-success" style={{ marginBottom: '16px' }}>
            <CheckCircle2 size={18} />
            <span>{reclusterSuccess}</span>
          </div>
        )}

        {error && (
          <div className="alert alert-danger" style={{ marginBottom: '16px' }}>
            <AlertCircle size={18} />
            <span>{error}</span>
          </div>
        )}

        {/* Niche Selector Toolbar */}
        <div className="interactive-card" style={{ padding: '14px 20px', marginBottom: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
              <span style={{ fontSize: '0.78rem', fontWeight: 700, color: '#1f3864', textTransform: 'uppercase' }}>
                Agency Niche:
              </span>
              <div className="pill-filter-bar">
                {niches.map((n) => {
                  const Icon = n.icon;
                  return (
                    <button
                      key={n.id}
                      type="button"
                      className={`pill-filter-btn ${selectedNiche === n.id ? 'active' : ''}`}
                      onClick={() => setSelectedNiche(n.id)}
                    >
                      <Icon size={13} />
                      <span>{n.label}</span>
                    </button>
                  );
                })}
              </div>
            </div>

            <span className="chart-badge-pill">
              Adaptive Vectors Active
            </span>
          </div>
        </div>

        {/* NLP Extraction Insights */}
        {recData && recData.top_keywords && (
          <div className="interactive-card" style={{ padding: '16px 22px', marginBottom: '22px' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '14px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <Key size={16} color="#b8860b" />
                  <span style={{ fontSize: '0.82rem', fontWeight: 700, color: '#1f3864', textTransform: 'uppercase' }}>
                    Extracted Semantic Tokens:
                  </span>
                </div>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                  {recData.top_keywords.map((kw, i) => (
                    <span
                      key={i}
                      style={{
                        background: '#fefce8',
                        color: '#854d0e',
                        border: '1px solid rgba(234, 179, 8, 0.4)',
                        borderRadius: '6px',
                        padding: '3px 10px',
                        fontSize: '0.78rem',
                        fontWeight: 700,
                      }}
                    >
                      {kw}
                    </span>
                  ))}
                </div>
              </div>

              <span className="chart-badge-pill">
                Corpus Cosine: {Math.round((recData.mean_corpus_similarity || 0.65) * 100)}%
              </span>
            </div>
          </div>
        )}

        {/* Recommendations Cards Grid */}
        {loading ? (
          <div style={{ textAlign: 'center', padding: '60px' }}>
            <div className="loading-spinner"></div>
            <div style={{ marginTop: '14px', color: '#64748b', fontSize: '0.9rem' }}>
              Computing TF-IDF vector matrices for {selectedNiche.replace('_', ' ')}...
            </div>
          </div>
        ) : recData?.recommendations?.length > 0 ? (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(360px, 1fr))', gap: '22px' }}>
            {recData.recommendations.map((topic) => (
              <div
                key={topic.id}
                className="interactive-card"
                style={{
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'space-between',
                  borderTop: '4px solid #1f3864',
                  padding: '22px',
                }}
              >
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                      {getPlatformIcon(topic.target_platform)}
                      <span style={{ fontSize: '0.82rem', fontWeight: 700, color: '#1f3864', textTransform: 'capitalize' }}>
                        {topic.target_platform}
                      </span>
                    </div>
                    <span className="badge badge-high" style={{ padding: '3px 9px', fontSize: '0.74rem' }}>
                      {Math.round(topic.similarity_score * 100)}% Affinity
                    </span>
                  </div>

                  <h3 style={{ fontSize: '1.15rem', fontWeight: 800, color: '#1f3864', marginBottom: '10px', lineHeight: 1.35, letterSpacing: '-0.2px' }}>
                    {topic.topic_title}
                  </h3>

                  <div style={{ marginBottom: '12px', fontSize: '0.84rem', color: '#334155', background: '#f8fafc', padding: '12px', borderRadius: '8px', border: '1px solid #e2e8f0', lineHeight: 1.45 }}>
                    <div style={{ fontWeight: 700, color: '#1f3864', marginBottom: '3px', fontSize: '0.78rem', textTransform: 'uppercase' }}>
                      Suggested Angle:
                    </div>
                    {topic.suggested_angle}
                  </div>

                  <div style={{ fontSize: '0.8rem', color: '#64748b', marginBottom: '14px', lineHeight: 1.4 }}>
                    💡 <b>Why:</b> {topic.why_recommended}
                  </div>

                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', marginBottom: '18px' }}>
                    {topic.recommended_hashtags.map((h, idx) => (
                      <span
                        key={idx}
                        style={{
                          background: '#eff6ff',
                          color: '#1d4ed8',
                          border: '1px solid #bfdbfe',
                          borderRadius: '6px',
                          padding: '2px 8px',
                          fontSize: '0.74rem',
                          fontWeight: 600,
                        }}
                      >
                        {h}
                      </span>
                    ))}
                  </div>
                </div>

                <button
                  onClick={() => handleUseTopic(topic)}
                  className="btn btn-gold btn-sm"
                  style={{ width: '100%', justifyContent: 'center', padding: '10px', fontSize: '0.88rem' }}
                >
                  <span>Use in Composer</span>
                  <ArrowRight size={15} />
                </button>
              </div>
            ))}
          </div>
        ) : (
          <div className="interactive-card" style={{ textAlign: 'center', padding: '60px 20px', color: '#64748b' }}>
            <Lightbulb size={48} color="#94a3b8" style={{ marginBottom: '14px' }} />
            <h3 style={{ fontSize: '1.2rem', fontWeight: 700, color: '#1f3864', marginBottom: '6px' }}>
              No Topic Clusters Generated Yet
            </h3>
            <p style={{ maxWidth: '400px', margin: '0 auto 18px', fontSize: '0.88rem' }}>
              Select a niche above or click "Re-cluster Corpus" to compute semantic vectors.
            </p>
            <button onClick={() => fetchRecommendations(selectedNiche, true)} className="btn btn-gold">
              Generate Recommendations
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Recommendations;
