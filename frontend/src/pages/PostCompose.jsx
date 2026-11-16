import React, { useState, useEffect } from 'react';
import { useNavigate, useParams, useLocation } from 'react-router-dom';
import { postsApi, predictionApi } from '../services/api';
import { useAuth } from '../context/AuthContext';
import TopBar from '../components/TopBar';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Cell
} from 'recharts';
import {
  PenSquare,
  Save,
  Clock,
  Instagram,
  Linkedin,
  Youtube,
  Hash,
  Image as ImageIcon,
  AlertCircle,
  CheckCircle2,
  ArrowLeft,
  Sparkles,
  TrendingUp,
  BrainCircuit,
  Smile,
  BookOpen,
  Zap,
  ArrowUpRight,
  Info,
  Smartphone,
  Eye,
  Sliders,
  Heart,
  MessageCircle,
  Share2,
  Bookmark
} from 'lucide-react';

const PostCompose = () => {
  const { id } = useParams();
  const location = useLocation();
  const isEditMode = Boolean(id);

  const [platform, setPlatform] = useState('instagram');
  const [caption, setCaption] = useState('');
  const [hashtagInput, setHashtagInput] = useState('');
  const [hashtags, setHashtags] = useState([]);
  const [mediaUrl, setMediaUrl] = useState('');
  const [scheduledTime, setScheduledTime] = useState('');
  const [status, setStatus] = useState('draft');

  const [activeTab, setActiveTab] = useState('ai_diagnostics'); // 'ai_diagnostics' | 'device_preview'
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // ML Prediction States (M3, M4, M8)
  const [predicting, setPredicting] = useState(false);
  const [predictionData, setPredictionData] = useState(null);
  const [bestTimeData, setBestTimeData] = useState(null);

  const { isClient, user, tenant } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (isEditMode) {
      loadPostForEdit(id);
    } else if (location.state) {
      if (location.state.suggestedCaption) setCaption(location.state.suggestedCaption);
      if (location.state.suggestedPlatform) setPlatform(location.state.suggestedPlatform);
      if (location.state.suggestedHashtags) setHashtags(location.state.suggestedHashtags);
      if (location.state.date) {
        setScheduledTime(`${location.state.date}T15:00`);
      } else {
        setDefaultScheduleTime();
      }
    } else {
      setDefaultScheduleTime();
    }
  }, [id, location]);

  const setDefaultScheduleTime = () => {
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    const year = tomorrow.getFullYear();
    const month = String(tomorrow.getMonth() + 1).padStart(2, '0');
    const day = String(tomorrow.getDate()).padStart(2, '0');
    setScheduledTime(`${year}-${month}-${day}T15:00`);
  };

  const loadPostForEdit = async (postId) => {
    setLoading(true);
    try {
      const res = await postsApi.getPost(postId);
      const p = res.data;
      setPlatform(p.platform);
      setCaption(p.caption);
      setHashtags(p.hashtags || []);
      setMediaUrl(p.media_url || '');
      setScheduledTime(p.scheduled_time || '');
      setStatus(p.status || 'draft');
    } catch (err) {
      setError('Could not load post details: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  const handleAddHashtag = (e) => {
    if (e.key === 'Enter' || e.key === ',') {
      e.preventDefault();
      const val = hashtagInput.trim().replace(/^#/, '');
      if (val && !hashtags.includes(`#${val}`)) {
        setHashtags([...hashtags, `#${val}`]);
        setHashtagInput('');
      }
    }
  };

  const removeHashtag = (tagToRemove) => {
    setHashtags(hashtags.filter((t) => t !== tagToRemove));
  };

  const appendQuickTag = (tag) => {
    const formatted = tag.startsWith('#') ? tag : `#${tag}`;
    if (!hashtags.includes(formatted)) {
      setHashtags([...hashtags, formatted]);
    }
  };

  // Plain integer 0-23 derived hour
  const derivedHour = scheduledTime && scheduledTime.includes('T')
    ? parseInt(scheduledTime.split('T')[1].split(':')[0], 10)
    : 12;

  // Run M3, M4, M8 AI scoring & optimization
  const handleAnalyzeAI = async () => {
    if (!caption.trim()) {
      setError('Please write or select a caption first to analyze.');
      return;
    }
    setPredicting(true);
    setError('');

    try {
      const reqPayload = {
        caption,
        platform,
        hour: derivedHour,
        weekday: new Date().getDay() || 2,
        hashtags,
      };

      const [scoreRes, bestTimeRes] = await Promise.all([
        predictionApi.scorePost(reqPayload),
        predictionApi.getBestTime({ ...reqPayload, current_hour: derivedHour }),
      ]);

      setPredictionData(scoreRes.data);
      setBestTimeData(bestTimeRes.data);
      setActiveTab('ai_diagnostics');
    } catch (err) {
      setError('Prediction failed: ' + (err.response?.data?.detail || err.message));
    } finally {
      setPredicting(false);
    }
  };

  // Apply best hour directly to the datetime picker
  const handleApplyHour = (newHour) => {
    if (!scheduledTime) {
      const today = new Date().toISOString().split('T')[0];
      setScheduledTime(`${today}T${String(newHour).padStart(2, '0')}:00`);
    } else {
      const datePart = scheduledTime.split('T')[0];
      setScheduledTime(`${datePart}T${String(newHour).padStart(2, '0')}:00`);
    }
  };

  // Apply hashtag suggestion
  const handleApplyHashtags = (targetCount) => {
    const defaultSuggestions = ['#growth', '#marketing', '#digital', '#trending', '#innovation'];
    const current = [...hashtags];
    while (current.length < targetCount && defaultSuggestions.length > 0) {
      const tag = defaultSuggestions.shift();
      if (!current.includes(tag)) current.push(tag);
    }
    setHashtags(current.slice(0, targetCount));
  };

  // Preset templates for instant viva demonstration
  const loadPreset = (presetKey) => {
    if (presetKey === 'tech_launch') {
      setPlatform('linkedin');
      setCaption('Excited to announce the breakthrough release of our real-time AI multimodal reasoning platform! 🚀 We reduced latency by 45% while achieving 99.4% precision on multi-tenant benchmarks. Here is how our engineering team scaled production inference.');
      setHashtags(['#ArtificialIntelligence', '#MachineLearning', '#CloudEngineering', '#TechLeadership']);
      setMediaUrl('https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&auto=format&fit=crop&q=80');
    } else if (presetKey === 'creator_hook') {
      setPlatform('instagram');
      setCaption('Stop scrolling! 💡 3 psychological hooks that generated 2.4M organic views in 14 days without spending a single dollar on ad campaigns. Save this post for your next content batch session.');
      setHashtags(['#ContentCreator', '#ViralMarketing', '#GrowthHacking', '#SocialMediaTips']);
      setMediaUrl('https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800&auto=format&fit=crop&q=80');
    } else if (presetKey === 'video_masterclass') {
      setPlatform('youtube');
      setCaption('Complete Masterclass: Fine-tuning Transformer & LightGBM Ensemble Models on High-Dimensional Tabular & Vision Datasets. Watch until the end for our open-source benchmark repo!');
      setHashtags(['#DataScience', '#MachineLearningTutorial', '#DeepLearning', '#PythonDev']);
      setMediaUrl('https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800&auto=format&fit=crop&q=80');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (isClient) {
      setError('Client account is in Observer Mode (Read-Only). Post creation is restricted to Editors and Administrators.');
      return;
    }
    if (!caption.trim()) {
      setError('Please provide a caption.');
      return;
    }

    setLoading(true);
    setError('');
    setSuccess('');

    const payload = {
      platform,
      caption,
      hashtags,
      media_url: mediaUrl.trim() || null,
      scheduled_time: scheduledTime || null,
      status,
    };

    try {
      if (isEditMode) {
        await postsApi.updatePost(id, payload);
        setSuccess('Post updated successfully in multi-tenant queue!');
      } else {
        await postsApi.createPost(payload);
        setSuccess('Post successfully created and scheduled on calendar!');
      }
      setTimeout(() => navigate('/calendar'), 1000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to save post.');
    } finally {
      setLoading(false);
    }
  };

  const chartData = predictionData?.explainability?.contributions?.slice(0, 6).map((c) => ({
    name: c.feature.replace('platform_', '').replace('_', ' '),
    importance: Math.round(c.importance * 100),
  })) || [];

  return (
    <div className="main-wrapper">
      <TopBar title={isEditMode ? 'Edit Scheduled Post' : 'AI Content Studio & Optimizer'} />

      <div className="content-body">
        {/* Executive Hero Banner */}
        <div className="page-hero-banner">
          <div className="page-hero-content">
            <div className="page-hero-tag">
              <Sparkles size={12} /> ML Pre-Flight Optimization Studio (M3, M4, M8)
            </div>
            <h1 className="page-hero-title">
              {isEditMode ? 'Refine & Re-Optimize Post' : 'Intelligent Multi-Modal Composer'}
            </h1>
            <p className="page-hero-subtitle">
              Simulate viral engagement tiers, sweep 24 posting hours with LightGBM, and visualize live social card mockups before publishing.
            </p>
          </div>
          <div className="page-hero-actions">
            <button
              onClick={() => navigate('/calendar')}
              className="btn btn-secondary btn-sm"
              style={{ background: 'rgba(255,255,255,0.15)', color: '#ffffff', borderColor: 'rgba(255,255,255,0.25)' }}
            >
              <ArrowLeft size={15} /> Back to Calendar
            </button>
          </div>
        </div>

        {/* Quick Viva Preset Templates */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '18px', flexWrap: 'wrap' }}>
          <span style={{ fontSize: '0.78rem', fontWeight: 700, color: '#1f3864', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
            ⚡ 1-Click Viva Templates:
          </span>
          <button type="button" onClick={() => loadPreset('tech_launch')} className="sample-preset-chip">
            🚀 LinkedIn Tech Launch
          </button>
          <button type="button" onClick={() => loadPreset('creator_hook')} className="sample-preset-chip">
            ✨ Instagram Viral Hook
          </button>
          <button type="button" onClick={() => loadPreset('video_masterclass')} className="sample-preset-chip">
            🎬 YouTube Video Masterclass
          </button>
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

        {isClient && (
          <div className="alert alert-warning" style={{ background: '#fef3c7', borderColor: '#fde68a', color: '#92400e', marginBottom: '16px' }}>
            <Info size={18} />
            <span>
              <b>Client Observer Mode (Read-Only):</b> You can simulate AI predictions and switch preview tabs, but post mutations are restricted to Editors & Admins.
            </span>
          </div>
        )}

        <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 0.8fr', gap: '24px' }}>
          {/* Left Column: Form Card */}
          <div className="interactive-card">
            <div className="card-top-header">
              <div>
                <h3 className="card-top-title">
                  {isEditMode ? 'Modify Post Content' : 'Post Content Studio'}
                </h3>
                <div className="card-top-subtitle">
                  Fill in post copy, media URL, and target platform below
                </div>
              </div>
              <button
                type="button"
                onClick={handleAnalyzeAI}
                className="btn btn-gold btn-sm"
                disabled={predicting}
                style={{ boxShadow: '0 4px 12px rgba(184, 134, 11, 0.25)' }}
              >
                {predicting ? <span className="loading-spinner"></span> : <><BrainCircuit size={15} /> Predict & Optimize with AI</>}
              </button>
            </div>

            <form onSubmit={handleSubmit}>
              {/* Platform Selector */}
              <div className="form-group">
                <label className="form-label" style={{ fontWeight: 700, color: '#1e293b' }}>
                  Target Social Platform
                </label>
                <div className="platform-selector-grid">
                  <button
                    type="button"
                    onClick={() => setPlatform('instagram')}
                    className={`platform-pill-btn ${platform === 'instagram' ? 'active-instagram' : ''}`}
                  >
                    <Instagram size={18} color={platform === 'instagram' ? '#be185d' : '#e1306c'} />
                    <span>Instagram</span>
                  </button>
                  <button
                    type="button"
                    onClick={() => setPlatform('linkedin')}
                    className={`platform-pill-btn ${platform === 'linkedin' ? 'active-linkedin' : ''}`}
                  >
                    <Linkedin size={18} color={platform === 'linkedin' ? '#0369a1' : '#0077b5'} />
                    <span>LinkedIn</span>
                  </button>
                  <button
                    type="button"
                    onClick={() => setPlatform('youtube')}
                    className={`platform-pill-btn ${platform === 'youtube' ? 'active-youtube' : ''}`}
                  >
                    <Youtube size={18} color={platform === 'youtube' ? '#b91c1c' : '#ef4444'} />
                    <span>YouTube</span>
                  </button>
                </div>
              </div>

              {/* Caption */}
              <div className="form-group">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                  <label className="form-label" style={{ marginBottom: 0, fontWeight: 700 }}>
                    Post Caption & Hook
                  </label>
                  <div style={{ display: 'flex', gap: '8px', fontSize: '0.74rem' }}>
                    <span style={{ color: '#64748b' }}>{caption.length} chars</span>
                    <span style={{ color: '#cbd5e1' }}>•</span>
                    <span style={{ color: '#64748b' }}>{caption.trim() ? caption.trim().split(/\s+/).length : 0} words</span>
                  </div>
                </div>
                <textarea
                  className="form-control"
                  rows={5}
                  placeholder="Draft your compelling social copy here, or click a 1-click template above..."
                  value={caption}
                  onChange={(e) => setCaption(e.target.value)}
                  style={{ fontSize: '0.92rem', lineHeight: 1.5, borderColor: '#cbd5e1' }}
                  required
                />
              </div>

              {/* Hashtags Input & Suggested Chips */}
              <div className="form-group">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                  <label className="form-label" style={{ marginBottom: 0, fontWeight: 700 }}>
                    Hashtags ({hashtags.length} added)
                  </label>
                  <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Press Enter or comma to add</span>
                </div>
                <div style={{ position: 'relative' }}>
                  <input
                    type="text"
                    className="form-control"
                    placeholder="Type hashtag and press Enter (e.g. ai, marketing)..."
                    value={hashtagInput}
                    onChange={(e) => setHashtagInput(e.target.value)}
                    onKeyDown={handleAddHashtag}
                    style={{ paddingLeft: '32px' }}
                  />
                  <Hash size={16} color="#94a3b8" style={{ position: 'absolute', left: '10px', top: '11px' }} />
                </div>

                {/* Added Hashtags */}
                {hashtags.length > 0 && (
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', marginTop: '10px' }}>
                    {hashtags.map((tag) => (
                      <span
                        key={tag}
                        style={{
                          background: '#eff6ff',
                          color: '#1d4ed8',
                          border: '1px solid #bfdbfe',
                          padding: '3px 10px',
                          borderRadius: '6px',
                          fontSize: '0.78rem',
                          fontWeight: 600,
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: '6px',
                        }}
                      >
                        {tag}
                        <button
                          type="button"
                          onClick={() => removeHashtag(tag)}
                          style={{
                            background: 'none',
                            border: 'none',
                            cursor: 'pointer',
                            color: '#93c5fd',
                            fontSize: '0.9rem',
                            padding: 0,
                            lineHeight: 1,
                          }}
                        >
                          &times;
                        </button>
                      </span>
                    ))}
                  </div>
                )}

                {/* Quick Add Suggestions */}
                <div style={{ marginTop: '8px', display: 'flex', alignItems: 'center', gap: '6px', flexWrap: 'wrap' }}>
                  <span style={{ fontSize: '0.72rem', color: '#64748b', fontWeight: 600 }}>Suggested:</span>
                  {['#Growth', '#DataScience', '#AI', '#Innovation', '#Trending'].map((tag) => (
                    <button
                      key={tag}
                      type="button"
                      onClick={() => appendQuickTag(tag)}
                      style={{
                        background: '#f8fafc',
                        border: '1px solid #e2e8f0',
                        borderRadius: '4px',
                        padding: '2px 7px',
                        fontSize: '0.72rem',
                        color: '#475569',
                        cursor: 'pointer',
                      }}
                    >
                      + {tag}
                    </button>
                  ))}
                </div>
              </div>

              {/* Media URL */}
              <div className="form-group">
                <label className="form-label" style={{ fontWeight: 700 }}>
                  Media Asset URL (Image / Cover Asset)
                </label>
                <div style={{ position: 'relative' }}>
                  <input
                    type="url"
                    className="form-control"
                    placeholder="https://images.unsplash.com/photo-..."
                    value={mediaUrl}
                    onChange={(e) => setMediaUrl(e.target.value)}
                    style={{ paddingLeft: '32px' }}
                  />
                  <ImageIcon size={16} color="#94a3b8" style={{ position: 'absolute', left: '10px', top: '11px' }} />
                </div>
              </div>

              {/* Scheduled Time & Status */}
              <div className="form-row">
                <div className="form-group">
                  <label className="form-label" style={{ fontWeight: 700 }}>
                    Scheduled Time
                  </label>
                  <input
                    type="datetime-local"
                    className="form-control"
                    value={scheduledTime}
                    onChange={(e) => setScheduledTime(e.target.value)}
                  />
                  <div style={{ fontSize: '0.74rem', color: '#64748b', marginTop: '4px' }}>
                    Derived Hour Slot: <span style={{ fontWeight: 700, color: '#1f3864' }}>{derivedHour !== null ? `${derivedHour}:00` : '12:00'}</span>
                  </div>
                </div>

                <div className="form-group">
                  <label className="form-label" style={{ fontWeight: 700 }}>
                    Workflow Status
                  </label>
                  <select
                    className="form-control"
                    value={status}
                    onChange={(e) => setStatus(e.target.value)}
                  >
                    <option value="draft">Draft (Private)</option>
                    <option value="scheduled">Scheduled (Active Queue)</option>
                    <option value="published">Published</option>
                  </select>
                </div>
              </div>

              <button
                type="submit"
                className="btn btn-gold"
                style={{ width: '100%', marginTop: '8px', padding: '12px', fontSize: '0.95rem' }}
                disabled={loading || isClient}
              >
                {loading ? <span className="loading-spinner"></span> : <><Save size={18} /> {isEditMode ? 'Update Scheduled Post' : 'Save & Enqueue Post'}</>}
              </button>
            </form>
          </div>

          {/* Right Column: AI Diagnostics or Live Social Device Preview */}
          <div>
            {/* View Tab Switcher */}
            <div className="pill-filter-bar" style={{ marginBottom: '16px' }}>
              <button
                type="button"
                className={`pill-filter-btn ${activeTab === 'ai_diagnostics' ? 'active' : ''}`}
                onClick={() => setActiveTab('ai_diagnostics')}
                style={{ flex: 1, justifyContent: 'center' }}
              >
                <BrainCircuit size={15} /> AI Pre-Flight Diagnostics
              </button>
              <button
                type="button"
                className={`pill-filter-btn ${activeTab === 'device_preview' ? 'active' : ''}`}
                onClick={() => setActiveTab('device_preview')}
                style={{ flex: 1, justifyContent: 'center' }}
              >
                <Smartphone size={15} /> Live Social Preview
              </button>
            </div>

            {/* TAB 1: AI DIAGNOSTICS */}
            {activeTab === 'ai_diagnostics' && (
              <div>
                {predictionData ? (
                  <div>
                    {/* Score & Tier Card (M3) */}
                    <div
                      className="interactive-card"
                      style={{
                        marginBottom: '16px',
                        borderTop: `4px solid ${predictionData.tier === 'high' ? '#16a34a' : predictionData.tier === 'medium' ? '#ca8a04' : '#dc2626'}`,
                      }}
                    >
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
                        <div>
                          <div style={{ fontSize: '0.74rem', textTransform: 'uppercase', color: '#64748b', fontWeight: 700, letterSpacing: '0.5px' }}>
                            LightGBM Predicted Tier
                          </div>
                          <div
                            style={{
                              fontSize: '1.65rem',
                              fontWeight: 900,
                              textTransform: 'uppercase',
                              letterSpacing: '-0.5px',
                              color: predictionData.tier === 'high' ? '#16a34a' : predictionData.tier === 'medium' ? '#ca8a04' : '#dc2626',
                            }}
                          >
                            {predictionData.tier} Potential
                          </div>
                        </div>
                        <div style={{ textAlign: 'right' }}>
                          <div style={{ fontSize: '0.74rem', color: '#64748b', fontWeight: 600 }}>Confidence</div>
                          <div style={{ fontSize: '1.35rem', fontWeight: 800, color: '#1f3864' }}>
                            {Math.round(predictionData.confidence * 100)}%
                          </div>
                        </div>
                      </div>

                      {/* Sentiment & Readability Badges */}
                      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                        <div style={{ padding: '10px 12px', background: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.74rem', color: '#64748b' }}>
                            <Smile size={14} color="#b8860b" />
                            <span>VADER Sentiment</span>
                          </div>
                          <div style={{ fontWeight: 700, fontSize: '0.92rem', marginTop: '3px', color: predictionData.sentiment >= 0 ? '#16a34a' : '#dc2626' }}>
                            {predictionData.sentiment >= 0.25 ? 'Positive' : predictionData.sentiment <= -0.2 ? 'Negative' : 'Neutral'} ({predictionData.sentiment})
                          </div>
                        </div>

                        <div style={{ padding: '10px 12px', background: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.74rem', color: '#64748b' }}>
                            <BookOpen size={14} color="#1f3864" />
                            <span>Flesch Readability</span>
                          </div>
                          <div style={{ fontWeight: 700, fontSize: '0.92rem', marginTop: '3px', color: '#1f3864' }}>
                            {predictionData.readability} / 100
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Top 3 Best Hours (M4) */}
                    {bestTimeData && (
                      <div className="interactive-card" style={{ marginBottom: '16px' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                            <Clock size={16} color="#b8860b" />
                            <h4 style={{ fontSize: '0.92rem', fontWeight: 700, color: '#1f3864', margin: 0 }}>
                              Top 3 Peak Posting Slots
                            </h4>
                          </div>
                          <span className="chart-badge-pill">24-hr Sweep</span>
                        </div>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                          {bestTimeData.top_hours.map((th, idx) => (
                            <div
                              key={th.hour}
                              style={{
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'space-between',
                                padding: '8px 12px',
                                background: idx === 0 ? '#fcf8e3' : '#f8fafc',
                                border: idx === 0 ? '1px solid rgba(184, 134, 11, 0.4)' : '1px solid #e2e8f0',
                                borderRadius: '8px',
                              }}
                            >
                              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                                <span style={{ fontWeight: 800, fontSize: '0.9rem', color: '#1f3864' }}>
                                  #{idx + 1} {th.hour_label}
                                </span>
                                <span className={`badge badge-${th.predicted_tier}`}>
                                  {Math.round(th.high_probability * 100)}% High Prob
                                </span>
                              </div>
                              <button
                                type="button"
                                onClick={() => handleApplyHour(th.hour)}
                                className="btn btn-secondary btn-sm"
                                style={{ fontSize: '0.75rem', padding: '3px 8px' }}
                              >
                                Apply Slot
                              </button>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Actionable Suggestions (M4) */}
                    {predictionData.suggestions && predictionData.suggestions.length > 0 && (
                      <div className="interactive-card" style={{ marginBottom: '16px' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '12px' }}>
                          <Zap size={16} color="#b8860b" />
                          <h4 style={{ fontSize: '0.92rem', fontWeight: 700, color: '#1f3864', margin: 0 }}>
                            AI Optimization Recommendations
                          </h4>
                        </div>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                          {predictionData.suggestions.map((sug, i) => (
                            <div
                              key={i}
                              style={{
                                padding: '10px 12px',
                                background: '#eff6ff',
                                border: '1px solid #bfdbfe',
                                borderRadius: '8px',
                                fontSize: '0.82rem',
                              }}
                            >
                              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
                                <span style={{ fontWeight: 700, color: '#1e40af' }}>{sug.title}</span>
                                <span style={{ fontWeight: 700, color: '#16a34a' }}>{sug.impact}</span>
                              </div>
                              <div style={{ color: '#475569', marginBottom: '8px', lineHeight: 1.4 }}>{sug.explanation}</div>
                              {sug.action === 'set_hour' && (
                                <button
                                  type="button"
                                  onClick={() => handleApplyHour(sug.recommended_value)}
                                  className="btn btn-primary btn-sm"
                                  style={{ fontSize: '0.74rem', padding: '3px 8px' }}
                                >
                                  Apply {String(sug.recommended_value).padStart(2, '0')}:00
                                </button>
                              )}
                              {sug.action === 'adjust_hashtags' && (
                                <button
                                  type="button"
                                  onClick={() => handleApplyHashtags(sug.recommended_value)}
                                  className="btn btn-primary btn-sm"
                                  style={{ fontSize: '0.74rem', padding: '3px 8px' }}
                                >
                                  Set Optimal Tags ({sug.recommended_value})
                                </button>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Feature Importance (M8) */}
                    <div className="interactive-card">
                      <div className="card-top-header">
                        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                          <TrendingUp size={16} color="#1f3864" />
                          <h4 className="card-top-title">Feature Explainability</h4>
                        </div>
                        <span className="chart-badge-pill">M8 TreeSHAP</span>
                      </div>
                      <div style={{ width: '100%', height: 170 }}>
                        <ResponsiveContainer width="100%" height="100%">
                          <BarChart data={chartData} layout="vertical" margin={{ top: 5, right: 20, left: 15, bottom: 5 }}>
                            <XAxis type="number" hide />
                            <YAxis type="category" dataKey="name" tick={{ fontSize: 11, fill: '#475569' }} width={95} />
                            <Tooltip formatter={(value) => [`${value}%`, 'Importance']} />
                            <Bar dataKey="importance" fill="#1f3864" radius={[0, 4, 4, 0]}>
                              {chartData.map((_, index) => (
                                <Cell key={`cell-${index}`} fill={index === 0 ? '#b8860b' : '#1f3864'} />
                              ))}
                            </Bar>
                          </BarChart>
                        </ResponsiveContainer>
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="interactive-card" style={{ textAlign: 'center', padding: '50px 20px', color: '#64748b' }}>
                    <BrainCircuit size={48} color="#94a3b8" style={{ marginBottom: '14px' }} />
                    <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#1f3864', marginBottom: '6px' }}>
                      Pre-Flight AI Inactive
                    </h3>
                    <p style={{ fontSize: '0.85rem', maxWidth: '300px', margin: '0 auto 16px' }}>
                      Click "Predict & Optimize with AI" above to run LightGBM scoring and 24-hour best-time sweeps.
                    </p>
                    <button type="button" onClick={handleAnalyzeAI} className="btn btn-gold btn-sm" disabled={predicting}>
                      Run AI Diagnostic
                    </button>
                  </div>
                )}
              </div>
            )}

            {/* TAB 2: LIVE SOCIAL DEVICE PREVIEW */}
            {activeTab === 'device_preview' && (
              <div className="device-mockup-wrapper">
                <div className="device-mockup-header">
                  <div className="device-user-badge">
                    <div className="device-avatar">
                      {user?.name ? user.name[0].toUpperCase() : 'A'}
                    </div>
                    <div>
                      <div style={{ fontSize: '0.88rem', fontWeight: 700, color: '#1e293b' }}>
                        {tenant?.name || 'ContentIQ Workspace'}
                      </div>
                      <div style={{ fontSize: '0.72rem', color: '#64748b' }}>
                        @{platform}_creator • Verified Tenant
                      </div>
                    </div>
                  </div>
                  <span className={`badge badge-${status}`}>
                    {platform.toUpperCase()}
                  </span>
                </div>

                {mediaUrl && (
                  <div className="device-media-box">
                    <img
                      src={mediaUrl}
                      alt="Post preview"
                      style={{ width: '100%', maxHeight: '240px', objectFit: 'cover' }}
                      onError={(e) => { e.target.style.display = 'none'; }}
                    />
                  </div>
                )}

                <div className="device-mockup-body">
                  <div className="device-caption-text">
                    {caption || <span style={{ color: '#94a3b8', fontStyle: 'italic' }}>Your post caption will be rendered here dynamically as you type...</span>}
                  </div>

                  {hashtags.length > 0 && (
                    <div style={{ marginTop: '8px' }}>
                      {hashtags.map((tag) => (
                        <span key={tag} className="device-hashtag-tag">
                          {tag}
                        </span>
                      ))}
                    </div>
                  )}
                </div>

                <div className="device-mockup-footer">
                  <div style={{ display: 'flex', gap: '14px', alignItems: 'center' }}>
                    <span style={{ display: 'flex', alignItems: 'center', gap: '4px', cursor: 'pointer' }}>
                      <Heart size={16} /> 1.4k
                    </span>
                    <span style={{ display: 'flex', alignItems: 'center', gap: '4px', cursor: 'pointer' }}>
                      <MessageCircle size={16} /> 84
                    </span>
                    <span style={{ display: 'flex', alignItems: 'center', gap: '4px', cursor: 'pointer' }}>
                      <Share2 size={16} /> 32
                    </span>
                  </div>
                  <Bookmark size={16} style={{ cursor: 'pointer' }} />
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default PostCompose;
