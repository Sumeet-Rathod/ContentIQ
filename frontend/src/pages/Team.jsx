import React, { useState, useEffect } from 'react';
import { teamApi } from '../services/api';
import { useAuth } from '../context/AuthContext';
import TopBar from '../components/TopBar';
import {
  Users,
  UserPlus,
  Shield,
  ShieldAlert,
  AlertCircle,
  CheckCircle2,
  Sparkles,
  Lock,
  Mail,
  User
} from 'lucide-react';

const Team = () => {
  const [members, setMembers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Invite Form State
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [role, setRole] = useState('editor');
  const [inviteLoading, setInviteLoading] = useState(false);

  const { user, isAdmin, tenant } = useAuth();

  const fetchMembers = async () => {
    setLoading(true);
    try {
      const res = await teamApi.getMembers();
      setMembers(res.data);
    } catch (err) {
      setError('Failed to fetch workspace team members.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMembers();
  }, []);

  const handleInvite = async (e) => {
    e.preventDefault();
    if (!isAdmin) {
      setError('Only Admin can invite new members to this tenant.');
      return;
    }
    setInviteLoading(true);
    setError('');
    setSuccess('');

    try {
      await teamApi.inviteMember({ name, email, role });
      setSuccess(`Successfully invited ${name} as ${role}!`);
      setName('');
      setEmail('');
      setRole('editor');
      fetchMembers();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to invite team member.');
    } finally {
      setInviteLoading(false);
    }
  };

  const handleRoleChange = async (userId, newRole) => {
    if (!isAdmin) {
      setError('Only Admin can change user roles.');
      return;
    }
    try {
      await teamApi.updateRole(userId, newRole);
      setSuccess(`Role updated to ${newRole}`);
      fetchMembers();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to update member role.');
    }
  };

  const quickFillInvite = (sampleRole) => {
    const randomId = Math.floor(Math.random() * 900) + 100;
    setName(sampleRole === 'editor' ? `Content Creator ${randomId}` : `Client Observer ${randomId}`);
    setEmail(`member.${randomId}@agency.com`);
    setRole(sampleRole);
  };

  return (
    <div className="main-wrapper">
      <TopBar title="Team & Multi-Tenant Access Governance" />

      <div className="content-body">
        {/* Executive Hero Banner */}
        <div className="page-hero-banner">
          <div className="page-hero-content">
            <div className="page-hero-tag">
              <Shield size={12} /> Enterprise Multi-Tenancy & RBAC
            </div>
            <h1 className="page-hero-title">
              Workspace Team & Access Governance
            </h1>
            <p className="page-hero-subtitle">
              Manage tenant user accounts and enforce strict 3-tier Role-Based Access Control (Admin, Editor, Client Observer) with cryptographic tenant ID isolation.
            </p>
          </div>
          <div className="page-hero-actions">
            <span className="kpi-trend-pill" style={{ background: 'rgba(22, 163, 74, 0.25)', color: '#86efac', border: '1px solid rgba(22, 163, 74, 0.4)', padding: '6px 12px' }}>
              ● Tenant Isolation Active
            </span>
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

        <div style={{ display: 'grid', gridTemplateColumns: isAdmin ? '1.25fr 0.75fr' : '1fr', gap: '24px' }}>
          {/* Members Table */}
          <div className="interactive-card" style={{ padding: 0, overflow: 'hidden' }}>
            <div style={{ padding: '16px 22px', borderBottom: '1px solid #f1f5f9', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <h3 className="card-top-title" style={{ margin: 0 }}>
                  Active Members of {tenant?.name || 'Workspace'} ({members.length})
                </h3>
                <div className="card-top-subtitle">Scoped strictly to tenant ID {tenant?.id?.slice(0, 8)}...</div>
              </div>
              <span className="chart-badge-pill">
                RBAC Active
              </span>
            </div>

            <div className="enterprise-table-container" style={{ border: 'none', borderRadius: 0 }}>
              <table className="enterprise-table">
                <thead>
                  <tr>
                    <th>User Identity</th>
                    <th>Email Address</th>
                    <th>Current Role</th>
                    {isAdmin && <th>Manage Permissions</th>}
                  </tr>
                </thead>
                <tbody>
                  {members.map((m) => (
                    <tr key={m.id}>
                      <td>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                          <div className="device-avatar" style={{ width: '32px', height: '32px', fontSize: '0.8rem' }}>
                            {m.name ? m.name[0].toUpperCase() : 'U'}
                          </div>
                          <div>
                            <span style={{ fontWeight: 700, color: '#1f3864', display: 'block' }}>
                              {m.name} {m.id === user?.id && <span style={{ color: '#b8860b' }}>(You)</span>}
                            </span>
                          </div>
                        </div>
                      </td>
                      <td style={{ color: '#64748b', fontSize: '0.82rem' }}>{m.email}</td>
                      <td>
                        <span
                          className={`badge ${
                            m.role === 'admin'
                              ? 'badge-high'
                              : m.role === 'editor'
                              ? 'badge-medium'
                              : 'badge-draft'
                          }`}
                          style={{ textTransform: 'uppercase', fontSize: '0.72rem', letterSpacing: '0.5px' }}
                        >
                          {m.role}
                        </span>
                      </td>
                      {isAdmin && (
                        <td>
                          {m.id !== user?.id ? (
                            <select
                              className="form-control"
                              style={{ width: 'auto', padding: '4px 8px', fontSize: '0.8rem' }}
                              value={m.role}
                              onChange={(e) => handleRoleChange(m.id, e.target.value)}
                            >
                              <option value="admin">Admin (Full Access)</option>
                              <option value="editor">Editor (Create/Edit)</option>
                              <option value="client">Client (Read-Only)</option>
                            </select>
                          ) : (
                            <span style={{ fontSize: '0.78rem', color: '#94a3b8', fontWeight: 600 }}>Primary Owner</span>
                          )}
                        </td>
                      )}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Admin Invite Form */}
          {isAdmin ? (
            <div className="interactive-card">
              <div className="card-top-header">
                <div>
                  <h3 className="card-top-title">Invite New Team Member</h3>
                  <div className="card-top-subtitle">Provision tenant login credentials</div>
                </div>
              </div>

              {/* Quick Fill Presets */}
              <div style={{ marginBottom: '14px' }}>
                <span style={{ fontSize: '0.74rem', color: '#64748b', fontWeight: 700, display: 'block', marginBottom: '6px' }}>
                  ⚡ Quick Demo Presets:
                </span>
                <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                  <button
                    type="button"
                    onClick={() => quickFillInvite('editor')}
                    className="sample-preset-chip"
                  >
                    + Invite Sample Editor
                  </button>
                  <button
                    type="button"
                    onClick={() => quickFillInvite('client')}
                    className="sample-preset-chip"
                  >
                    + Invite Sample Client
                  </button>
                </div>
              </div>

              <form onSubmit={handleInvite}>
                <div className="form-group">
                  <label className="form-label" style={{ fontWeight: 700 }}>Full Name</label>
                  <div style={{ position: 'relative' }}>
                    <input
                      type="text"
                      className="form-control"
                      placeholder="e.g. Sarah Jenkins"
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      style={{ paddingLeft: '32px' }}
                      required
                    />
                    <User size={15} color="#94a3b8" style={{ position: 'absolute', left: '10px', top: '11px' }} />
                  </div>
                </div>

                <div className="form-group">
                  <label className="form-label" style={{ fontWeight: 700 }}>Corporate Email</label>
                  <div style={{ position: 'relative' }}>
                    <input
                      type="email"
                      className="form-control"
                      placeholder="e.g. sarah@agency.com"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      style={{ paddingLeft: '32px' }}
                      required
                    />
                    <Mail size={15} color="#94a3b8" style={{ position: 'absolute', left: '10px', top: '11px' }} />
                  </div>
                </div>

                <div className="form-group">
                  <label className="form-label" style={{ fontWeight: 700 }}>Assigned Role</label>
                  <select
                    className="form-control"
                    value={role}
                    onChange={(e) => setRole(e.target.value)}
                  >
                    <option value="editor">Editor (Can compose, analyze & schedule)</option>
                    <option value="client">Client Observer (Read-only access)</option>
                    <option value="admin">Administrator (Full tenant control)</option>
                  </select>
                </div>

                <button
                  type="submit"
                  className="btn btn-gold"
                  style={{ width: '100%', padding: '10px' }}
                  disabled={inviteLoading}
                >
                  {inviteLoading ? <span className="loading-spinner"></span> : <><UserPlus size={16} /> Send Workspace Invitation</>}
                </button>
              </form>
            </div>
          ) : (
            <div className="interactive-card" style={{ textAlign: 'center', padding: '40px 20px', color: '#64748b' }}>
              <Lock size={36} color="#94a3b8" style={{ marginBottom: '10px' }} />
              <h4 style={{ color: '#1f3864' }}>Role Management Restricted</h4>
              <p style={{ fontSize: '0.85rem' }}>Only workspace Administrators can invite new members or modify permissions.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Team;
