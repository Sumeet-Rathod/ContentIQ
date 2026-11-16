import React, { useState, useRef } from 'react';
import { intelligenceApi } from '../services/api';
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
  Image as ImageIcon,
  UploadCloud,
  CheckCircle2,
  AlertCircle,
  Sparkles,
  Layers,
  SunMedium,
  Contrast,
  Focus,
  Palette,
  Eye,
  Grid,
  Zap,
  Check
} from 'lucide-react';

const ThumbnailScorer = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [scoreData, setScoreData] = useState(null);
  const [error, setError] = useState('');
  const [showGridOverlay, setShowGridOverlay] = useState(true);
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setScoreData(null);
      setError('');
    }
  };

  const executeAnalysis = async (fileToAnalyze) => {
    const file = fileToAnalyze || selectedFile;
    if (!file) {
      setError('Please select or generate an image file first.');
      return;
    }

    setLoading(true);
    setError('');
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await intelligenceApi.scoreThumbnail(formData);
      setScoreData(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to analyze thumbnail with OpenCV.');
    } finally {
      setLoading(false);
    }
  };

  // Helper to generate dynamic sample images on canvas for 1-click viva testing
  const loadQuickSample = (sampleType) => {
    const canvas = document.createElement('canvas');
    canvas.width = 1280;
    canvas.height = 720;
    const ctx = canvas.getContext('2d');

    if (sampleType === 'tech_high_contrast') {
      // Dark navy + gold high contrast banner
      const grad = ctx.createLinearGradient(0, 0, 1280, 720);
      grad.addColorStop(0, '#0f172a');
      grad.addColorStop(1, '#1e293b');
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, 1280, 720);

      // Gold accent header & visual hook
      ctx.fillStyle = '#b8860b';
      ctx.fillRect(80, 80, 16, 240);

      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 64px Inter, sans-serif';
      ctx.fillText('BREAKTHROUGH AI', 120, 150);
      ctx.fillStyle = '#d4af37';
      ctx.font = 'bold 48px Inter, sans-serif';
      ctx.fillText('Multimodal Optimization Engine', 120, 230);

      // Visual focal circle on rule-of-thirds intersection (approx x: 850, y: 360)
      ctx.beginPath();
      ctx.arc(880, 360, 160, 0, 2 * Math.PI);
      ctx.fillStyle = 'rgba(184, 134, 11, 0.3)';
      ctx.fill();
      ctx.lineWidth = 6;
      ctx.strokeStyle = '#d4af37';
      ctx.stroke();

      ctx.fillStyle = '#f8fafc';
      ctx.font = 'bold 36px Inter, sans-serif';
      ctx.fillText('99.4% ACCURACY', 720, 370);
    } else if (sampleType === 'vibrant_creative') {
      // Magenta / Purple gradient
      const grad = ctx.createLinearGradient(0, 0, 1280, 720);
      grad.addColorStop(0, '#4c1d95');
      grad.addColorStop(0.5, '#be185d');
      grad.addColorStop(1, '#fbbf24');
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, 1280, 720);

      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 72px Inter, sans-serif';
      ctx.fillText('VIRAL FORMULA ⚡', 100, 220);

      ctx.fillStyle = '#fef08a';
      ctx.font = 'bold 42px Inter, sans-serif';
      ctx.fillText('3 Secrets to 1M Views', 100, 310);
    } else {
      // Minimalist Clean Studio
      ctx.fillStyle = '#f8fafc';
      ctx.fillRect(0, 0, 1280, 720);

      ctx.fillStyle = '#1f3864';
      ctx.font = 'bold 58px Inter, sans-serif';
      ctx.fillText('ENTERPRISE DATA SUITE', 140, 240);

      ctx.fillStyle = '#64748b';
      ctx.font = '32px Inter, sans-serif';
      ctx.fillText('Automated Analytics & Reporting', 140, 320);

      ctx.fillStyle = '#b8860b';
      ctx.fillRect(140, 360, 180, 8);
    }

    canvas.toBlob((blob) => {
      if (blob) {
        const file = new File([blob], `${sampleType}.png`, { type: 'image/png' });
        setSelectedFile(file);
        setPreviewUrl(URL.createObjectURL(file));
        executeAnalysis(file);
      }
    }, 'image/png');
  };

  const metricColors = {
    Brightness: '#b8860b',
    Contrast: '#1f3864',
    Sharpness: '#16a34a',
    Colourfulness: '#d97706',
    Composition: '#0284c7',
  };

  return (
    <div className="main-wrapper">
      <TopBar title="Computer Vision Thumbnail Diagnostic Studio" />

      <div className="content-body">
        {/* Executive Hero Banner */}
        <div className="page-hero-banner">
          <div className="page-hero-content">
            <div className="page-hero-tag">
              <Sparkles size={12} /> OpenCV Image Intelligence (M5)
            </div>
            <h1 className="page-hero-title">
              Computer Vision Quality & Aesthetics Scorer
            </h1>
            <p className="page-hero-subtitle">
              Decompose thumbnails into quantitative multi-spectral metrics: Brightness distribution, Michelson Contrast, Laplacian Sharpness, Hasler-Süsstrunk Colourfulness, and Rule-of-Thirds compositional balance.
            </p>
          </div>
          <div className="page-hero-actions">
            <button
              onClick={() => fileInputRef.current?.click()}
              className="btn btn-gold btn-sm"
              style={{ boxShadow: '0 4px 12px rgba(184, 134, 11, 0.3)' }}
            >
              <UploadCloud size={15} /> Upload Custom Asset
            </button>
          </div>
        </div>

        {/* 1-Click Viva Testing Presets */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '18px', flexWrap: 'wrap' }}>
          <span style={{ fontSize: '0.78rem', fontWeight: 700, color: '#1f3864', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
            ⚡ 1-Click OpenCV Demo Samples:
          </span>
          <button
            type="button"
            onClick={() => loadQuickSample('tech_high_contrast')}
            className="sample-preset-chip"
            disabled={loading}
          >
            🌟 Tech High-Contrast Banner
          </button>
          <button
            type="button"
            onClick={() => loadQuickSample('vibrant_creative')}
            className="sample-preset-chip"
            disabled={loading}
          >
            🎨 Vibrant Gradient Hook
          </button>
          <button
            type="button"
            onClick={() => loadQuickSample('minimalist_studio')}
            className="sample-preset-chip"
            disabled={loading}
          >
            📐 Minimalist Corporate Studio
          </button>
        </div>

        {error && (
          <div className="alert alert-danger" style={{ marginBottom: '16px' }}>
            <AlertCircle size={18} />
            <span>{error}</span>
          </div>
        )}

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
          {/* Upload & Visual Preview Card */}
          <div className="interactive-card">
            <div className="card-top-header">
              <div>
                <h3 className="card-top-title">Thumbnail Asset Inspector</h3>
                <div className="card-top-subtitle">Drag-and-drop or select an image to inspect</div>
              </div>
              {previewUrl && (
                <button
                  type="button"
                  onClick={() => setShowGridOverlay(!showGridOverlay)}
                  className="btn btn-secondary btn-sm"
                  style={{ fontSize: '0.75rem', padding: '4px 10px' }}
                >
                  <Grid size={13} /> {showGridOverlay ? 'Hide 3x3 Grid' : 'Show 3x3 Grid'}
                </button>
              )}
            </div>

            <div
              style={{
                border: '2px dashed #cbd5e1',
                borderRadius: '12px',
                padding: '24px 16px',
                textAlign: 'center',
                backgroundColor: '#f8fafc',
                cursor: 'pointer',
                marginBottom: '16px',
                transition: 'all 0.2s ease',
              }}
              onClick={() => fileInputRef.current?.click()}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleFileChange}
                style={{ display: 'none' }}
              />

              <div
                style={{
                  width: '48px',
                  height: '48px',
                  borderRadius: '50%',
                  background: '#eff6ff',
                  color: '#1d4ed8',
                  display: 'inline-flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  marginBottom: '10px',
                }}
              >
                <UploadCloud size={24} />
              </div>

              <div style={{ fontWeight: 700, color: '#1f3864', fontSize: '0.92rem' }}>
                {selectedFile ? selectedFile.name : 'Click to Upload or Drag & Drop'}
              </div>
              <div style={{ fontSize: '0.78rem', color: '#64748b', marginTop: '4px' }}>
                Supports JPG, PNG, WebP (YouTube 1280x720, Instagram 1080x1080, LinkedIn 1200x627)
              </div>
            </div>

            {/* Visual Preview with Rule-of-Thirds Grid */}
            {previewUrl && (
              <div style={{ marginBottom: '16px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                  <label className="form-label" style={{ marginBottom: 0, fontWeight: 700 }}>
                    Live Visual Canvas:
                  </label>
                  <span style={{ fontSize: '0.74rem', color: '#64748b' }}>
                    {selectedFile?.name}
                  </span>
                </div>
                <div className="cv-preview-container">
                  <img
                    src={previewUrl}
                    alt="Thumbnail preview"
                    className="cv-preview-img"
                  />
                  {showGridOverlay && (
                    <div className="rule-of-thirds-grid">
                      <div className="rule-cell"></div>
                      <div className="rule-cell"></div>
                      <div className="rule-cell"></div>
                      <div className="rule-cell"></div>
                      <div className="rule-cell"></div>
                      <div className="rule-cell"></div>
                      <div className="rule-cell"></div>
                      <div className="rule-cell"></div>
                      <div className="rule-cell"></div>
                    </div>
                  )}
                </div>
                {showGridOverlay && (
                  <div style={{ fontSize: '0.72rem', color: '#94a3b8', textAlign: 'center', marginTop: '6px' }}>
                    📐 Gold dashed grid displays Rule-of-Thirds focal intersections for visual engagement optimization.
                  </div>
                )}
              </div>
            )}

            <button
              onClick={() => executeAnalysis()}
              className="btn btn-gold"
              style={{ width: '100%', padding: '12px' }}
              disabled={loading || !selectedFile}
            >
              {loading ? <span className="loading-spinner"></span> : <><Sparkles size={17} /> Analyze with OpenCV CV Engine</>}
            </button>
          </div>

          {/* Results Scorecard */}
          <div>
            {scoreData ? (
              <div className="interactive-card">
                <div className="card-top-header">
                  <div>
                    <div style={{ fontSize: '0.74rem', textTransform: 'uppercase', color: '#64748b', fontWeight: 700 }}>
                      OpenCV Overall Quality Score
                    </div>
                    <div
                      style={{
                        fontSize: '2.2rem',
                        fontWeight: 900,
                        letterSpacing: '-1px',
                        color: scoreData.overall_score >= 70 ? '#16a34a' : scoreData.overall_score >= 50 ? '#ca8a04' : '#dc2626',
                      }}
                    >
                      {scoreData.overall_score} <span style={{ fontSize: '1.1rem', fontWeight: 600, color: '#94a3b8' }}>/ 100</span>
                    </div>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <span className="chart-badge-pill" style={{ display: 'block', marginBottom: '4px' }}>
                      Verified Resolution
                    </span>
                    <span style={{ fontSize: '0.85rem', fontWeight: 800, color: '#1f3864' }}>
                      {scoreData.dimensions}
                    </span>
                  </div>
                </div>

                {/* Bar Chart of Metrics */}
                <h4 style={{ fontSize: '0.88rem', fontWeight: 700, color: '#1f3864', marginBottom: '10px' }}>
                  Computer Vision Sub-Scores (0-100)
                </h4>
                <div style={{ width: '100%', height: 180, marginBottom: '16px' }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={scoreData.metrics} layout="vertical" margin={{ top: 5, right: 25, left: 20, bottom: 5 }}>
                      <XAxis type="number" domain={[0, 100]} hide />
                      <YAxis type="category" dataKey="name" tick={{ fontSize: 11, fill: '#475569', fontWeight: 600 }} width={95} />
                      <Tooltip formatter={(value) => [`${value}%`, 'Score']} />
                      <Bar dataKey="percentage" radius={[0, 5, 5, 0]}>
                        {scoreData.metrics.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={metricColors[entry.name] || '#1f3864'} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>

                {/* Sub-Metric Summary Grid */}
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '10px', marginBottom: '18px' }}>
                  {scoreData.metrics.map((m) => (
                    <div
                      key={m.name}
                      style={{
                        background: '#f8fafc',
                        padding: '10px 8px',
                        borderRadius: '8px',
                        border: '1px solid #e2e8f0',
                        textAlign: 'center',
                      }}
                    >
                      <div style={{ fontSize: '0.72rem', color: '#64748b', fontWeight: 600 }}>{m.name}</div>
                      <div style={{ fontSize: '1.15rem', fontWeight: 800, color: '#1f3864', marginTop: '2px' }}>
                        {m.score}
                      </div>
                    </div>
                  ))}
                </div>

                {/* Recommendations */}
                <div>
                  <h4 style={{ fontSize: '0.88rem', fontWeight: 700, color: '#1f3864', marginBottom: '10px' }}>
                    CV Optimization Insights & Recommendations
                  </h4>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                    {scoreData.recommendations.map((rec, i) => (
                      <div
                        key={i}
                        style={{
                          display: 'flex',
                          alignItems: 'flex-start',
                          gap: '10px',
                          padding: '10px 12px',
                          background: '#fcf8e3',
                          border: '1px solid rgba(184, 134, 11, 0.35)',
                          borderRadius: '8px',
                          fontSize: '0.84rem',
                          color: '#1f3864',
                        }}
                      >
                        <Sparkles size={16} color="#b8860b" style={{ flexShrink: 0, marginTop: '2px' }} />
                        <span style={{ lineHeight: 1.4 }}>{rec}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <div className="interactive-card" style={{ textAlign: 'center', padding: '60px 20px', color: '#64748b' }}>
                <ImageIcon size={52} color="#94a3b8" style={{ marginBottom: '14px' }} />
                <h3 style={{ fontSize: '1.15rem', fontWeight: 700, color: '#1f3864', marginBottom: '6px' }}>
                  No Thumbnail Analyzed Yet
                </h3>
                <p style={{ fontSize: '0.88rem', maxWidth: '340px', margin: '0 auto 18px', lineHeight: 1.5 }}>
                  Select or drop a social media thumbnail on the left, or click one of the <b>1-Click Demo Samples</b> above to run OpenCV analysis.
                </p>
                <div style={{ display: 'inline-flex', gap: '8px' }}>
                  <button
                    type="button"
                    onClick={() => loadQuickSample('tech_high_contrast')}
                    className="btn btn-gold btn-sm"
                  >
                    ⚡ Test Tech Banner Sample
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ThumbnailScorer;
