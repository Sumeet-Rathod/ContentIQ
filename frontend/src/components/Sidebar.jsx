import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  LayoutDashboard,
  Calendar,
  PenSquare,
  BarChart3,
  TrendingUp,
  Sparkles,
  Image as ImageIcon,
  LineChart,
  Split,
  Users2,
  Bell,
  Users,
  LogOut,
  Shield,
  Eye,
  Edit3,
  CheckCircle2
} from 'lucide-react';

const Sidebar = () => {
  const { user, tenant, logout, isAdmin, isEditor, isClient } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  // Base navigation items
  const allNavLinks = [
    { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard, roles: ['admin', 'editor', 'client'] },
    { to: '/calendar', label: 'Calendar', icon: Calendar, roles: ['admin', 'editor', 'client'] },
    { to: '/compose', label: 'Compose Post', icon: PenSquare, roles: ['admin', 'editor'] },
    { to: '/analytics', label: 'Analytics', icon: BarChart3, roles: ['admin', 'editor', 'client'] },
    { to: '/trends', label: 'Trends Radar', icon: TrendingUp, roles: ['admin', 'editor'] },
    { to: '/recommendations', label: 'Topic Recs', icon: Sparkles, roles: ['admin', 'editor'] },
    { to: '/thumbnail', label: 'Thumbnail Scorer', icon: ImageIcon, roles: ['admin', 'editor'] },
    { to: '/forecast', label: 'Follower Forecast', icon: LineChart, roles: ['admin', 'editor', 'client'] },
    { to: '/ab-tests', label: 'A/B Testing', icon: Split, roles: ['admin', 'editor'] },
    { to: '/competitors', label: 'Competitors', icon: Users2, roles: ['admin', 'editor', 'client'] },
    { to: '/notifications', label: 'Notifications', icon: Bell, roles: ['admin', 'editor', 'client'] },
    { to: '/team', label: 'Team & Roles', icon: Users, roles: ['admin'] },
  ];

  // Filter links by current user's role
  const userRole = user?.role || 'editor';
  const visibleNavLinks = allNavLinks.filter((item) => item.roles.includes(userRole));

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="brand-badge-wrapper">
          <div className="brand-badge">IQ</div>
          <span className="brand-dot-pulse" />
        </div>
        <div>
          <div className="brand-title">ContentIQ</div>
          <div className="brand-tenant">{tenant?.name || 'Workspace'}</div>
        </div>
      </div>

      <nav className="sidebar-nav">
        <div className="nav-section-title">
          {isClient ? 'Client Portal (Read-Only)' : 'Enterprise Modules'}
        </div>
        {visibleNavLinks.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
            >
              <span className="nav-item-icon">
                <Icon size={17} />
              </span>
              <span className="nav-item-label">{item.label}</span>
            </NavLink>
          );
        })}
      </nav>

      <div className="sidebar-footer">
        <div className="user-profile-brief">
          <span className="user-name">{user?.name || user?.email}</span>
          <span
            className="user-role-badge"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '4px',
              padding: '2px 8px',
              borderRadius: '6px',
              fontSize: '0.7rem',
              fontWeight: 700,
              textTransform: 'uppercase',
              background: isAdmin ? 'rgba(184, 134, 11, 0.25)' : isClient ? 'rgba(100, 116, 139, 0.25)' : 'rgba(31, 56, 100, 0.4)',
              color: isAdmin ? '#fcd34d' : isClient ? '#cbd5e1' : '#93c5fd',
              marginTop: '3px',
              border: isAdmin ? '1px solid rgba(184, 134, 11, 0.4)' : '1px solid rgba(255, 255, 255, 0.1)',
            }}
          >
            {isAdmin && <Shield size={11} />}
            {isEditor && <Edit3 size={11} />}
            {isClient && <Eye size={11} />}
            {user?.role}
          </span>
        </div>
        <button onClick={handleLogout} className="btn-logout" title="Sign out of ContentIQ">
          <LogOut size={16} />
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;
