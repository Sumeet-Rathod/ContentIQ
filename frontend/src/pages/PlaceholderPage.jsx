import React from 'react';
import TopBar from '../components/TopBar';
import { Sparkles, Calendar, ArrowRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const PlaceholderPage = ({ moduleName, phase, description }) => {
  const navigate = useNavigate();

  return (
    <div className="main-wrapper">
      <TopBar title={moduleName} />

      <div className="content-body">
        <div className="card" style={{ maxWidth: '700px', margin: '40px auto', textAlign: 'center', padding: '40px 24px' }}>
          <div
            style={{
              width: '60px',
              height: '60px',
              borderRadius: '50%',
              backgroundColor: '#fcf8e3',
              color: '#b8860b',
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              marginBottom: '16px',
            }}
          >
            <Sparkles size={28} />
          </div>

          <h2 style={{ fontSize: '1.4rem', fontWeight: 700, color: '#1f3864', marginBottom: '8px' }}>
            {moduleName}
          </h2>

          <div
            style={{
              display: 'inline-block',
              background: '#e0f2fe',
              color: '#0369a1',
              padding: '4px 12px',
              borderRadius: '9999px',
              fontSize: '0.8rem',
              fontWeight: 600,
              marginBottom: '16px',
            }}
          >
            Scheduled for {phase}
          </div>

          <p style={{ color: '#64748b', fontSize: '0.95rem', lineHeight: 1.6, marginBottom: '24px' }}>
            {description}
          </p>

          <div style={{ display: 'flex', justifyContent: 'center', gap: '12px' }}>
            <button onClick={() => navigate('/calendar')} className="btn btn-primary">
              <Calendar size={16} /> Open Content Calendar
            </button>
            <button onClick={() => navigate('/compose')} className="btn btn-gold">
              Schedule New Post <ArrowRight size={16} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PlaceholderPage;
