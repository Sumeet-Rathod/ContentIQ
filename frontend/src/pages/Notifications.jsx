import React, { useState, useEffect } from 'react';
import { notificationApi } from '../services/api';
import TopBar from '../components/TopBar';
import {
  Bell,
  CheckCircle2,
  Clock,
  AlertTriangle,
  Sparkles,
  CheckCheck,
  RefreshCw,
  Send,
  Eye,
  Check
} from 'lucide-react';

const Notifications = () => {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [unreadOnly, setUnreadOnly] = useState(false);
  const [error, setError] = useState('');

  const fetchNotifications = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await notificationApi.getNotifications(unreadOnly);
      setNotifications(res.data);
    } catch (err) {
      setError('Failed to load notifications.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNotifications();
  }, [unreadOnly]);

  const handleMarkRead = async (id) => {
    try {
      await notificationApi.markRead(id);
      setNotifications(
        notifications.map((n) => (n.id === id ? { ...n, is_read: true } : n))
      );
    } catch (err) {
      // Silent fail
    }
  };

  const handleMarkAllRead = async () => {
    try {
      await notificationApi.markAllRead();
      setNotifications(notifications.map((n) => ({ ...n, is_read: true })));
    } catch (err) {
      // Silent fail
    }
  };

  const getNotificationIcon = (type) => {
    switch (type) {
      case 'upcoming_post':
        return <Clock size={18} color="#0369a1" />;
      case 'low_prediction':
        return <AlertTriangle size={18} color="#dc2626" />;
      case 'published_confirmation':
        return <Send size={18} color="#16a34a" />;
      case 'retrain_alert':
        return <Sparkles size={18} color="#b8860b" />;
      default:
        return <Bell size={18} color="#1f3864" />;
    }
  };

  const unreadCount = notifications.filter((n) => !n.is_read).length;

  return (
    <div className="main-wrapper">
      <TopBar title="Tenant Event Stream & Real-Time Alerts" />

      <div className="content-body">
        {/* Executive Hero Banner */}
        <div className="page-hero-banner">
          <div className="page-hero-content">
            <div className="page-hero-tag">
              <Bell size={12} /> Event Stream & Alerting Engine
            </div>
            <h1 className="page-hero-title">
              Tenant Notifications & Operational Telemetry
            </h1>
            <p className="page-hero-subtitle">
              Live asynchronous notification pipeline capturing scheduled post releases, LightGBM active learning model retrains, and cross-channel feedback anomalies.
            </p>
          </div>
          <div className="page-hero-actions">
            <span className="kpi-trend-pill" style={{ background: unreadCount > 0 ? 'rgba(184, 134, 11, 0.25)' : 'rgba(22, 163, 74, 0.25)', color: unreadCount > 0 ? '#fde047' : '#86efac', border: '1px solid rgba(255,255,255,0.2)', padding: '6px 12px' }}>
              {unreadCount} Unread Alerts
            </span>
          </div>
        </div>

        {/* Toolbar Card */}
        <div className="interactive-card" style={{ padding: '14px 20px', marginBottom: '18px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '14px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span style={{ fontSize: '0.78rem', fontWeight: 700, color: '#1f3864', textTransform: 'uppercase' }}>
                View Filter:
              </span>
              <div className="pill-filter-bar">
                <button
                  type="button"
                  className={`pill-filter-btn ${!unreadOnly ? 'active' : ''}`}
                  onClick={() => setUnreadOnly(false)}
                >
                  All Alerts ({notifications.length})
                </button>
                <button
                  type="button"
                  className={`pill-filter-btn ${unreadOnly ? 'active' : ''}`}
                  onClick={() => setUnreadOnly(true)}
                >
                  Unread Only ({unreadCount})
                </button>
              </div>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <button
                onClick={fetchNotifications}
                className="btn btn-secondary btn-sm"
                title="Refresh Stream"
              >
                <RefreshCw size={14} className={loading ? 'loading-spinner' : ''} /> Refresh
              </button>
              <button
                onClick={handleMarkAllRead}
                className="btn btn-gold btn-sm"
                disabled={unreadCount === 0}
              >
                <CheckCheck size={14} /> Mark All as Read
              </button>
            </div>
          </div>
        </div>

        {/* Notifications Stream Container */}
        <div className="interactive-card" style={{ padding: 0, overflow: 'hidden' }}>
          <div style={{ padding: '16px 22px', borderBottom: '1px solid #f1f5f9', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h4 className="card-top-title" style={{ margin: 0 }}>
              Live Telemetry Stream ({notifications.length} Events)
            </h4>
            <span className="chart-badge-pill">
              ● Active Stream
            </span>
          </div>

          {loading ? (
            <div style={{ textAlign: 'center', padding: '60px' }}>
              <div className="loading-spinner"></div>
            </div>
          ) : notifications.length > 0 ? (
            <div style={{ display: 'flex', flexDirection: 'column' }}>
              {notifications.map((n) => (
                <div
                  key={n.id}
                  style={{
                    padding: '18px 22px',
                    borderBottom: '1px solid #f1f5f9',
                    backgroundColor: n.is_read ? '#ffffff' : '#fcf8e3',
                    display: 'flex',
                    alignItems: 'flex-start',
                    justifyContent: 'space-between',
                    gap: '16px',
                    transition: 'background 0.15s ease',
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'flex-start', gap: '16px' }}>
                    <div
                      style={{
                        padding: '10px',
                        borderRadius: '10px',
                        background: '#ffffff',
                        border: '1px solid #e2e8f0',
                        boxShadow: '0 2px 4px rgba(0,0,0,0.04)',
                        marginTop: '2px',
                      }}
                    >
                      {getNotificationIcon(n.type)}
                    </div>
                    <div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <span style={{ fontWeight: 800, color: '#1f3864', fontSize: '0.94rem' }}>
                          {n.title}
                        </span>
                        {!n.is_read && (
                          <span
                            style={{
                              background: '#b8860b',
                              color: '#fff',
                              fontSize: '0.65rem',
                              fontWeight: 800,
                              borderRadius: '4px',
                              padding: '2px 7px',
                              textTransform: 'uppercase',
                              letterSpacing: '0.5px',
                            }}
                          >
                            New
                          </span>
                        )}
                      </div>
                      <p style={{ fontSize: '0.86rem', color: '#475569', marginTop: '4px', lineHeight: 1.45 }}>
                        {n.message}
                      </p>
                      <span style={{ fontSize: '0.74rem', color: '#94a3b8', marginTop: '6px', display: 'inline-block', fontWeight: 500 }}>
                        {new Date(n.created_at).toLocaleString()}
                      </span>
                    </div>
                  </div>

                  {!n.is_read && (
                    <button
                      onClick={() => handleMarkRead(n.id)}
                      className="btn btn-secondary btn-sm"
                      style={{ fontSize: '0.75rem', padding: '4px 10px', flexShrink: 0 }}
                      title="Mark as Read"
                    >
                      <Check size={13} /> Mark Read
                    </button>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <div style={{ textAlign: 'center', padding: '60px 20px', color: '#64748b' }}>
              <Bell size={48} color="#94a3b8" style={{ marginBottom: '14px' }} />
              <h3 style={{ fontSize: '1.2rem', fontWeight: 700, color: '#1f3864', marginBottom: '6px' }}>
                All Caught Up!
              </h3>
              <p style={{ maxWidth: '360px', margin: '0 auto', fontSize: '0.88rem' }}>
                No active notifications or unread alerts in this workspace. New post triggers and ML retrain events will appear here in real time.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Notifications;
