import React from 'react';

export default function AIReview({ aiReview }) {
  if (!aiReview) return null;

  const {
    ai_status = 'success',
    ai_notice = '',
    overall_assessment = '',
    strengths = [],
    areas_for_improvement = [],
    hook_analysis = '',
    clarity_analysis = '',
    engagement_analysis = '',
    cta_analysis = '',
    audience_analysis = '',
    tone = '',
  } = aiReview;

  const dimensions = [
    { name: 'Hook / Opening', desc: hook_analysis },
    { name: 'Clarity & Cadence', desc: clarity_analysis },
    { name: 'Engagement Prompts', desc: engagement_analysis },
    { name: 'Call to Action', desc: cta_analysis },
    { name: 'Audience & Tone', desc: tone ? `Tone: ${tone}. ${audience_analysis || ''}` : audience_analysis },
  ].filter((d) => Boolean(d.desc));

  return (
    <div className="card" id="ai-review-section">
      <div className="card-title">
        <span>Editorial & Semantic Analysis</span>
        <span className="meta-chip">
          {ai_status === 'success' ? 'Gemini Analysis' : 'Built-in Rule Analysis'}
        </span>
      </div>

      {ai_status === 'fallback' && ai_notice && (
        <div id="ai-fallback-banner" className="ai-notice-banner">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          <span>{ai_notice}</span>
        </div>
      )}

      {overall_assessment && (
        <p className="assessment-narrative">{overall_assessment}</p>
      )}

      <div className="strengths-weaknesses-grid">
        <div className="sw-column">
          <div className="sw-title strength">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
            Key Strengths
          </div>
          <ul className="sw-list">
            {strengths.map((s, idx) => (
              <li key={idx}>{s}</li>
            ))}
          </ul>
        </div>

        <div className="sw-column">
          <div className="sw-title improvement">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="8" x2="12" y2="12"></line>
              <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
            Areas for Improvement
          </div>
          <ul className="sw-list">
            {areas_for_improvement.map((w, idx) => (
              <li key={idx}>{w}</li>
            ))}
          </ul>
        </div>
      </div>

      {dimensions.length > 0 && (
        <div className="dimension-cards">
          {dimensions.map((dim, idx) => (
            <div key={idx} className="dimension-item">
              <div className="dim-name">{dim.name}</div>
              <div className="dim-desc">{dim.desc}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
