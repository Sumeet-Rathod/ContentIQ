import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { notificationApi } from '../services/api';
import { ShieldCheck, Building2, Bell, Sparkles, Activity } from 'lucide-react';

const TopBar = ({ title }) => {
  const { user, tenant, isAdmin } = useAuth();
  const [unreadCount, setUnreadCount] = useState(0);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUnread = async () => {
      try {
        const res = await notificationApi.getNotifications(true);
        setUnreadCount(res.data.length);
      } catch (err) {
        // Silent
      }
    };
    fetchUnread();
  }, []);

  return (
    <header className="top-bar">
      <div className="page-title-area">
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <h1 className="page-title">{title}</h1>
            <span className="live-status-pill" title="Live simulation environment with real ML pipelines">
              <span className="live-indicator-dot" />
              <span>Live System Active</span>
            </span>
          </div>
          <div style={{ fontSize: '0.74rem', color: '#64748b', marginTop: '2px', fontWeight: 500 }}>Enterprise Multi-Tenant AI Content Intelligence & Optimization Platform</div>
        </div>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        {/* In-App Notification Bell */}
        <button
          onClick={() => navigate('/notifications')}
          className="topbar-icon-btn"
          title="In-App Notifications & Audit Stream"
        >
          <Bell size={18} />
          {unreadCount > 0 && (
            <span className="notification-badge-dot">
              {unreadCount}
            </span>
          )}
        </button>

        {/* Tenant Workspace Badge */}
        <div className="badge-tenant-pill" title="Current logical tenant workspace">
          <Building2 size={13} color="#b8860b" />
          <span>{tenant?.name || 'Workspace'}</span>
          <span className="tenant-plan-tag">{tenant?.plan || 'Pro'}</span>
        </div>

        {/* User Role Avatar Pill */}
        <div className="badge-user-pill">
          <div className="user-avatar-circle">
            {user?.name ? user.name.charAt(0).toUpperCase() : 'U'}
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', textAlign: 'left', lineHeight: 1.2 }}>
            <span style={{ fontSize: '0.8rem', fontWeight: 700, color: '#1e293b' }}>
              {user?.name || user?.email}
            </span>
            <span style={{ fontSize: '0.68rem', color: isAdmin ? '#b8860b' : '#64748b', fontWeight: 600, textTransform: 'uppercase' }}>
              {user?.role}
            </span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default TopBar;
