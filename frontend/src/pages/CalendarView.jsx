import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { postsApi, feedbackApi } from '../services/api';
import { useAuth } from '../context/AuthContext';
import TopBar from '../components/TopBar';
import {
  Calendar as CalendarIcon,
  ChevronLeft,
  ChevronRight,
  Plus,
  Filter,
  Instagram,
  Linkedin,
  Youtube,
  Trash2,
  Edit,
  Clock,
  X,
  MessageSquare,
  BarChart2,
  Send,
  Smile,
  Frown,
  Meh,
  Sparkles,
  Layers,
  CheckCircle2,
  AlertCircle,
  FileText
} from 'lucide-react';

const CalendarView = () => {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedPost, setSelectedPost] = useState(null);

  // Filters
  const [platformFilter, setPlatformFilter] = useState('all');
  const [statusFilter, setStatusFilter] = useState('all');

  // Modal Sub-features: Comments & Metrics
  const [activeModalTab, setActiveModalTab] = useState('details'); // 'details' | 'comments' | 'metrics'
  const [commentsData, setCommentsData] = useState(null);
  const [commentText, setCommentText] = useState('');
  const [commentAuthor, setCommentAuthor] = useState('');
  const [commentLoading, setCommentLoading] = useState(false);

  // Metrics Form
  const [likes, setLikes] = useState('');
  const [commentsCount, setCommentsCount] = useState('');
  const [shares, setShares] = useState('');
  const [reach, setReach] = useState('');
  const [metricsSaving, setMetricsSaving] = useState(false);

  const { isClient } = useAuth();
  const navigate = useNavigate();

  const fetchPosts = async () => {
    setLoading(true);
    setError('');
    try {
      const params = {};
      if (platformFilter !== 'all') params.platform = platformFilter;
      if (statusFilter !== 'all') params.status = statusFilter;

      const res = await postsApi.getPosts(params);
      setPosts(res.data);
    } catch (err) {
      setError('Failed to fetch scheduled posts: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPosts();
  }, [currentDate, platformFilter, statusFilter]);

  // Load comments when a post is clicked
  useEffect(() => {
    if (selectedPost) {
      fetchComments(selectedPost.id);
      setLikes(selectedPost.likes || '');
      setCommentsCount(selectedPost.comments_count || selectedPost.comments || '');
      setShares(selectedPost.shares || '');
      setReach(selectedPost.reach || '');
    } else {
      setCommentsData(null);
    }
  }, [selectedPost]);

  const fetchComments = async (postId) => {
    try {
      const res = await feedbackApi.getComments(postId);
      setCommentsData(res.data);
    } catch (err) {
      // Silent fail
    }
  };

  const handleAddComment = async (e) => {
    e.preventDefault();
    if (!commentText.trim()) return;
    setCommentLoading(true);
    try {
      await feedbackApi.addComment({
        post_id: selectedPost.id,
        author: commentAuthor || 'Audience Member',
        text: commentText,
      });
      setCommentText('');
      fetchComments(selectedPost.id);
    } catch (err) {
      alert('Failed to post comment: ' + (err.response?.data?.detail || err.message));
    } finally {
      setCommentLoading(false);
    }
  };

  const handleSaveMetrics = async (e) => {
    e.preventDefault();
    setMetricsSaving(true);
    try {
      await feedbackApi.logMetrics({
        post_id: selectedPost.id,
        likes: parseInt(likes, 10) || 0,
        comments: parseInt(commentsCount, 10) || 0,
        shares: parseInt(shares, 10) || 0,
        reach: parseInt(reach, 10) || 100,
      });
      alert('Metrics logged! Post marked as Published with updated engagement rate.');
      fetchPosts();
      setSelectedPost(null);
    } catch (err) {
      alert('Failed to save metrics: ' + (err.response?.data?.detail || err.message));
    } finally {
      setMetricsSaving(false);
    }
  };

  const handleDeletePost = async (postId) => {
    if (!window.confirm('Are you sure you want to delete this scheduled post?')) return;
    try {
      await postsApi.deletePost(postId);
      setSelectedPost(null);
      fetchPosts();
    } catch (err) {
      alert('Failed to delete post: ' + (err.response?.data?.detail || err.message));
    }
  };

  // Calendar calculations
  const year = currentDate.getFullYear();
  const month = currentDate.getMonth();

  const firstDayIndex = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const monthName = currentDate.toLocaleString('default', { month: 'long' });

  const prevMonth = () => setCurrentDate(new Date(year, month - 1, 1));
  const nextMonth = () => setCurrentDate(new Date(year, month + 1, 1));
  const goToToday = () => setCurrentDate(new Date());

  const getPostsForDay = (day) => {
    const formattedDay = String(day).padStart(2, '0');
    const formattedMonth = String(month + 1).padStart(2, '0');
    const targetDateStr = `${year}-${formattedMonth}-${formattedDay}`;

    return posts.filter((p) => {
      if (!p.scheduled_time) return false;
      const cleanTime = String(p.scheduled_time).split('T')[0].split(' ')[0];
      return cleanTime === targetDateStr;
    });
  };

  const handleDayClick = (dayNumber) => {
    if (isClient) return;
    const formattedDay = String(dayNumber).padStart(2, '0');
    const formattedMonth = String(month + 1).padStart(2, '0');
    const targetDateStr = `${year}-${formattedMonth}-${formattedDay}`;
    navigate('/compose', { state: { date: targetDateStr } });
  };

  const getPlatformIcon = (platform) => {
    switch (platform?.toLowerCase()) {
      case 'instagram':
        return <Instagram size={13} color="#e1306c" />;
      case 'linkedin':
        return <Linkedin size={13} color="#0077b5" />;
      case 'youtube':
        return <Youtube size={13} color="#ff0000" />;
      default:
        return null;
    }
  };

  const scheduledCount = posts.filter((p) => p.status === 'scheduled').length;
  const publishedCount = posts.filter((p) => p.status === 'published').length;
  const draftPosts = posts.filter((p) => p.status === 'draft' || !p.scheduled_time);

  return (
    <div className="main-wrapper">
      <TopBar title="Editorial Calendar & Scheduling Hub" />

      <div className="content-body">
        {/* Executive Hero Banner */}
        <div className="page-hero-banner">
          <div className="page-hero-content">
            <div className="page-hero-tag">
              <CalendarIcon size={12} /> Editorial Pipeline Deck
            </div>
            <h1 className="page-hero-title">
              Content Release Calendar & Publication Queue
            </h1>
            <p className="page-hero-subtitle">
              Orchestrate multi-channel publication pipelines across Instagram, LinkedIn, and YouTube with live status telemetry and post feedback capture.
            </p>
          </div>
          <div className="page-hero-actions">
            <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
              <span className="kpi-trend-pill" style={{ background: 'rgba(22, 163, 74, 0.25)', color: '#86efac', border: '1px solid rgba(22, 163, 74, 0.4)' }}>
                {scheduledCount} Scheduled
              </span>
              <span className="kpi-trend-pill" style={{ background: 'rgba(184, 134, 11, 0.25)', color: '#fde047', border: '1px solid rgba(184, 134, 11, 0.4)' }}>
                {publishedCount} Published
              </span>
            </div>
            {!isClient && (
              <button
                onClick={() => navigate('/compose')}
                className="btn btn-gold btn-sm"
                style={{ boxShadow: '0 4px 12px rgba(184, 134, 11, 0.3)' }}
              >
                <Plus size={15} /> Compose Post
              </button>
            )}
          </div>
        </div>

        {/* Calendar Navigation & Filter Deck */}
        <div className="interactive-card" style={{ padding: '14px 20px', marginBottom: '18px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '14px' }}>
            {/* Month Switcher */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <button onClick={prevMonth} className="btn btn-secondary btn-sm" title="Previous Month">
                <ChevronLeft size={16} />
              </button>
              <h2 style={{ fontSize: '1.25rem', fontWeight: 800, minWidth: '190px', textAlign: 'center', color: '#1f3864', letterSpacing: '-0.3px', margin: 0 }}>
                {monthName} {year}
              </h2>
              <button onClick={nextMonth} className="btn btn-secondary btn-sm" title="Next Month">
                <ChevronRight size={16} />
              </button>
              <button onClick={goToToday} className="btn btn-secondary btn-sm" style={{ fontWeight: 700, fontSize: '0.78rem' }}>
                Today
              </button>
            </div>

            {/* Filter Pills */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', flexWrap: 'wrap' }}>
              {/* Platform Pills */}
              <div className="pill-filter-bar">
                {['all', 'instagram', 'linkedin', 'youtube'].map((p) => (
                  <button
                    key={p}
                    type="button"
                    className={`pill-filter-btn ${platformFilter === p ? 'active' : ''}`}
                    onClick={() => setPlatformFilter(p)}
                    style={{ textTransform: 'capitalize' }}
                  >
                    {p === 'all' ? 'All Platforms' : p}
                  </button>
                ))}
              </div>

              {/* Status Pills */}
              <div className="pill-filter-bar">
                {['all', 'scheduled', 'draft', 'published'].map((s) => (
                  <button
                    key={s}
                    type="button"
                    className={`pill-filter-btn ${statusFilter === s ? 'active' : ''}`}
                    onClick={() => setStatusFilter(s)}
                    style={{ textTransform: 'capitalize' }}
                  >
                    {s === 'all' ? 'All Status' : s}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {error && (
          <div className="alert alert-danger" style={{ marginBottom: '16px' }}>
            <AlertCircle size={18} />
            <span>{error}</span>
          </div>
        )}

        {/* Calendar Grid Container */}
        <div className="interactive-card" style={{ padding: 0, overflow: 'hidden', marginBottom: '20px' }}>
          <div className="calendar-grid">
            {['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'].map((d) => (
              <div key={d} className="calendar-header-day" style={{ fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.6px', fontSize: '0.74rem' }}>
                {d}
              </div>
            ))}

            {Array.from({ length: firstDayIndex }).map((_, i) => (
              <div key={`empty-${i}`} className="calendar-cell other-month" />
            ))}

            {Array.from({ length: daysInMonth }).map((_, i) => {
              const dayNumber = i + 1;
              const dayPosts = getPostsForDay(dayNumber);
              const isToday =
                new Date().getDate() === dayNumber &&
                new Date().getMonth() === month &&
                new Date().getFullYear() === year;

              return (
                <div
                  key={`day-${dayNumber}`}
                  className={`calendar-cell ${isToday ? 'today' : ''}`}
                  style={isToday ? { background: '#fefce8', borderColor: '#eab308' } : {}}
                  onClick={() => handleDayClick(dayNumber)}
                  title="Click date cell to schedule a new post on this day"
                >
                  <div
                    className="calendar-cell-date"
                    style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      fontWeight: isToday ? 800 : 700,
                      color: isToday ? '#854d0e' : '#475569',
                    }}
                  >
                    <span>{dayNumber}</span>
                    {isToday && (
                      <span
                        style={{
                          background: '#ca8a04',
                          color: '#ffffff',
                          padding: '1px 6px',
                          borderRadius: '9999px',
                          fontSize: '0.65rem',
                          fontWeight: 700,
                        }}
                      >
                        TODAY
                      </span>
                    )}
                  </div>

                  <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '4px', marginTop: '4px' }}>
                    {dayPosts.map((post) => (
                      <div
                        key={post.id}
                        className={`calendar-post-pill ${post.platform}`}
                        onClick={(e) => {
                          e.stopPropagation();
                          setSelectedPost(post);
                          setActiveModalTab('details');
                        }}
                        title={post.caption}
                        style={{ cursor: 'pointer', transition: 'all 0.15s ease' }}
                      >
                        <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                          {getPlatformIcon(post.platform)}
                          <span style={{ fontWeight: 700, fontSize: '0.72rem' }}>
                            {post.scheduled_hour !== null && post.scheduled_hour !== undefined
                              ? `${String(post.scheduled_hour).padStart(2, '0')}:00`
                              : ''}
                          </span>
                          <span style={{ textOverflow: 'ellipsis', overflow: 'hidden', whiteSpace: 'nowrap' }}>
                            {post.caption}
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Unscheduled Drafts Dock */}
        {draftPosts.length > 0 && (
          <div className="interactive-card" style={{ padding: '18px 22px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <FileText size={17} color="#b8860b" />
                <h4 className="card-top-title" style={{ margin: 0 }}>
                  Unscheduled Drafts ({draftPosts.length})
                </h4>
              </div>
              <span className="chart-badge-pill">Click draft to edit or assign date</span>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '12px' }}>
              {draftPosts.slice(0, 6).map((dp) => (
                <div
                  key={dp.id}
                  onClick={() => navigate(`/compose/${dp.id}`)}
                  style={{
                    padding: '12px 14px',
                    borderRadius: '8px',
                    background: '#f8fafc',
                    border: '1px solid #e2e8f0',
                    cursor: 'pointer',
                    transition: 'all 0.15s ease',
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                      {getPlatformIcon(dp.platform)}
                      <span style={{ fontSize: '0.76rem', fontWeight: 700, textTransform: 'capitalize', color: '#1f3864' }}>{dp.platform}</span>
                    </div>
                    <span className="badge badge-draft" style={{ fontSize: '0.68rem', padding: '1px 6px' }}>Draft</span>
                  </div>
                  <div style={{ fontSize: '0.84rem', color: '#334155', textOverflow: 'ellipsis', overflow: 'hidden', whiteSpace: 'nowrap' }}>
                    {dp.caption}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Post Detail & Telemetry Modal */}
        {selectedPost && (
          <div className="modal-overlay" onClick={() => setSelectedPost(null)}>
            <div className="modal-card" style={{ maxWidth: '780px', borderRadius: '16px' }} onClick={(e) => e.stopPropagation()}>
              <div className="card-header" style={{ marginBottom: '14px', borderBottom: '1px solid #f1f5f9', paddingBottom: '12px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  {getPlatformIcon(selectedPost.platform)}
                  <h3 className="card-title" style={{ textTransform: 'capitalize', margin: 0, fontSize: '1.15rem' }}>
                    {selectedPost.platform} Post Inspection
                  </h3>
                  <span className={`badge badge-${selectedPost.status}`}>
                    {selectedPost.status}
                  </span>
                  {selectedPost.actual_tier && (
                    <span className={`badge badge-${selectedPost.actual_tier}`}>
                      Actual: {selectedPost.actual_tier} ({selectedPost.engagement_rate}%)
                    </span>
                  )}
                </div>
                <button
                  onClick={() => setSelectedPost(null)}
                  style={{ background: 'none', border: 'none', cursor: 'pointer', color: '#64748b' }}
                >
                  <X size={20} />
                </button>
              </div>

              {/* Modal Sub-tabs */}
              <div className="pill-filter-bar" style={{ marginBottom: '16px' }}>
                <button
                  type="button"
                  className={`pill-filter-btn ${activeModalTab === 'details' ? 'active' : ''}`}
                  onClick={() => setActiveModalTab('details')}
                >
                  Overview & Details
                </button>
                <button
                  type="button"
                  className={`pill-filter-btn ${activeModalTab === 'comments' ? 'active' : ''}`}
                  onClick={() => setActiveModalTab('comments')}
                >
                  <MessageSquare size={14} /> Comments & Sentiment ({commentsData?.comments?.length || 0})
                </button>
                <button
                  type="button"
                  className={`pill-filter-btn ${activeModalTab === 'metrics' ? 'active' : ''}`}
                  onClick={() => setActiveModalTab('metrics')}
                >
                  <BarChart2 size={14} /> Log Actual Telemetry
                </button>
              </div>

              {/* TAB 1: DETAILS */}
              {activeModalTab === 'details' && (
                <div>
                  <div style={{ marginBottom: '14px' }}>
                    <label className="form-label" style={{ fontWeight: 700 }}>Caption Copy:</label>
                    <div style={{ padding: '14px', background: '#f8fafc', borderRadius: '10px', border: '1px solid #e2e8f0', fontSize: '0.92rem', whiteSpace: 'pre-wrap', lineHeight: 1.5 }}>
                      {selectedPost.caption}
                    </div>
                  </div>

                  {selectedPost.hashtags && selectedPost.hashtags.length > 0 && (
                    <div style={{ marginBottom: '14px' }}>
                      <label className="form-label" style={{ fontWeight: 700 }}>Hashtags:</label>
                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                        {selectedPost.hashtags.map((tag, idx) => (
                          <span key={idx} style={{ background: '#eff6ff', color: '#1d4ed8', border: '1px solid #bfdbfe', padding: '3px 9px', borderRadius: '6px', fontSize: '0.8rem', fontWeight: 600 }}>
                            {tag}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {selectedPost.media_url && (
                    <div style={{ marginBottom: '14px' }}>
                      <label className="form-label" style={{ fontWeight: 700 }}>Media Asset:</label>
                      <div style={{ background: '#0f172a', borderRadius: '8px', padding: '6px', textAlign: 'center' }}>
                        <img
                          src={selectedPost.media_url}
                          alt="Post asset"
                          style={{ maxHeight: '180px', maxWidth: '100%', objectFit: 'contain', borderRadius: '4px' }}
                          onError={(e) => { e.target.style.display = 'none'; }}
                        />
                      </div>
                    </div>
                  )}

                  <div className="form-row" style={{ marginBottom: '18px' }}>
                    <div>
                      <label className="form-label" style={{ fontWeight: 700 }}>Scheduled Timestamp:</label>
                      <div style={{ fontSize: '0.88rem', color: '#1f3864', fontWeight: 600 }}>
                        {selectedPost.scheduled_time || 'None (Immediate / Draft)'}
                      </div>
                    </div>
                    <div>
                      <label className="form-label" style={{ fontWeight: 700 }}>Peak Slot Derived Hour:</label>
                      <div style={{ fontSize: '0.88rem', color: '#1f3864', fontWeight: 600 }}>
                        {selectedPost.scheduled_hour !== null ? `${selectedPost.scheduled_hour}:00` : 'Not Set'}
                      </div>
                    </div>
                  </div>

                  {/* Actions */}
                  {!isClient && (
                    <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px', paddingTop: '12px', borderTop: '1px solid #f1f5f9' }}>
                      <button
                        onClick={() => handleDeletePost(selectedPost.id)}
                        className="btn btn-secondary btn-sm"
                        style={{ color: '#dc2626', borderColor: '#fca5a5' }}
                      >
                        <Trash2 size={15} /> Delete Post
                      </button>
                      <button
                        onClick={() => navigate(`/compose/${selectedPost.id}`)}
                        className="btn btn-primary btn-sm"
                      >
                        <Edit size={15} /> Edit in Studio
                      </button>
                    </div>
                  )}
                </div>
              )}

              {/* TAB 2: COMMENTS & SENTIMENT */}
              {activeModalTab === 'comments' && (
                <div>
                  {commentsData?.sentiment_summary && (
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '10px', marginBottom: '14px' }}>
                      <div style={{ background: '#f0fdf4', border: '1px solid #bbf7d0', padding: '10px', borderRadius: '8px', textAlign: 'center' }}>
                        <div style={{ fontSize: '0.74rem', color: '#166534', fontWeight: 700 }}>Positive Sentiment</div>
                        <div style={{ fontSize: '1.2rem', fontWeight: 800, color: '#15803d' }}>
                          {commentsData.sentiment_summary.positive_pct}%
                        </div>
                      </div>
                      <div style={{ background: '#f8fafc', border: '1px solid #e2e8f0', padding: '10px', borderRadius: '8px', textAlign: 'center' }}>
                        <div style={{ fontSize: '0.74rem', color: '#475569', fontWeight: 700 }}>Neutral</div>
                        <div style={{ fontSize: '1.2rem', fontWeight: 800, color: '#334155' }}>
                          {commentsData.sentiment_summary.neutral_pct}%
                        </div>
                      </div>
                      <div style={{ background: '#fef2f2', border: '1px solid #fecaca', padding: '10px', borderRadius: '8px', textAlign: 'center' }}>
                        <div style={{ fontSize: '0.74rem', color: '#991b1b', fontWeight: 700 }}>Negative</div>
                        <div style={{ fontSize: '1.2rem', fontWeight: 800, color: '#b91c1c' }}>
                          {commentsData.sentiment_summary.negative_pct}%
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Add Comment Form */}
                  <form onSubmit={handleAddComment} style={{ display: 'flex', gap: '8px', marginBottom: '14px' }}>
                    <input
                      type="text"
                      className="form-control"
                      placeholder="Comment text (e.g. Amazing insights!)..."
                      value={commentText}
                      onChange={(e) => setCommentText(e.target.value)}
                      style={{ flex: 2 }}
                    />
                    <input
                      type="text"
                      className="form-control"
                      placeholder="Author..."
                      value={commentAuthor}
                      onChange={(e) => setCommentAuthor(e.target.value)}
                      style={{ flex: 1 }}
                    />
                    <button type="submit" className="btn btn-gold btn-sm" disabled={commentLoading}>
                      <Send size={14} /> Add
                    </button>
                  </form>

                  {/* Comments List */}
                  <div style={{ maxHeight: '220px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                    {commentsData?.comments && commentsData.comments.length > 0 ? (
                      commentsData.comments.map((c, i) => (
                        <div key={i} style={{ background: '#f8fafc', padding: '10px 12px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
                          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2px' }}>
                            <span style={{ fontWeight: 700, fontSize: '0.82rem', color: '#1f3864' }}>{c.author}</span>
                            <span style={{ fontSize: '0.72rem', color: c.sentiment_score >= 0.2 ? '#16a34a' : c.sentiment_score <= -0.2 ? '#dc2626' : '#64748b', fontWeight: 700 }}>
                              {c.sentiment_score >= 0.2 ? 'Positive' : c.sentiment_score <= -0.2 ? 'Negative' : 'Neutral'} ({c.sentiment_score})
                            </span>
                          </div>
                          <div style={{ fontSize: '0.85rem', color: '#334155' }}>{c.text}</div>
                        </div>
                      ))
                    ) : (
                      <div style={{ textAlign: 'center', padding: '24px', color: '#94a3b8', fontSize: '0.85rem' }}>
                        No audience comments logged yet. Use the form above to log real audience comments for VADER sentiment tracking!
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* TAB 3: METRICS */}
              {activeModalTab === 'metrics' && (
                <form onSubmit={handleSaveMetrics}>
                  <p style={{ fontSize: '0.82rem', color: '#64748b', marginBottom: '14px' }}>
                    Log actual engagement telemetry once the post has been live on social media. ContentIQ will calculate the actual engagement rate and retrain ML models via Active Learning!
                  </p>
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '12px', marginBottom: '16px' }}>
                    <div>
                      <label className="form-label">Likes</label>
                      <input
                        type="number"
                        className="form-control"
                        placeholder="e.g. 240"
                        value={likes}
                        onChange={(e) => setLikes(e.target.value)}
                      />
                    </div>
                    <div>
                      <label className="form-label">Comments</label>
                      <input
                        type="number"
                        className="form-control"
                        placeholder="e.g. 45"
                        value={commentsCount}
                        onChange={(e) => setCommentsCount(e.target.value)}
                      />
                    </div>
                    <div>
                      <label className="form-label">Shares / Reposts</label>
                      <input
                        type="number"
                        className="form-control"
                        placeholder="e.g. 18"
                        value={shares}
                        onChange={(e) => setShares(e.target.value)}
                      />
                    </div>
                    <div>
                      <label className="form-label">Total Reach / Impressions</label>
                      <input
                        type="number"
                        className="form-control"
                        placeholder="e.g. 5200"
                        value={reach}
                        onChange={(e) => setReach(e.target.value)}
                        required
                      />
                    </div>
                  </div>
                  <button
                    type="submit"
                    className="btn btn-gold"
                    style={{ width: '100%', padding: '10px' }}
                    disabled={metricsSaving}
                  >
                    {metricsSaving ? <span className="loading-spinner"></span> : <><BarChart2 size={16} /> Save Telemetry & Update Status to Published</>}
                  </button>
                </form>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default CalendarView;
