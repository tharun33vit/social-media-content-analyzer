import React from 'react';

export default function ScoreCard({ scoreData }) {
  if (!scoreData) return null;

  const { total_score = 0, verdict = '', breakdown = {}, disclaimer = '' } = scoreData;

  const breakdownItems = Object.entries(breakdown).map(([key, item]) => ({
    key,
    label: item.label,
    score: item.score,
    max: item.max,
    percentage: Math.min(100, Math.round((item.score / item.max) * 100)),
  }));

  return (
    <div className="card" id="score-card-section">
      <div className="card-title">
        <span>Content & Engagement Readiness</span>
        <span className="meta-chip">100-Point Heuristic</span>
      </div>

      <div className="score-card-layout">
        <div className="score-hero-box">
          <div className="score-hero-number">{total_score}</div>
          <div className="score-hero-denom">/ 100</div>
          <div className="score-hero-label">Readiness Score</div>
        </div>

        <div className="score-details-area">
          {verdict && <p className="score-verdict-text">{verdict}</p>}

          <div className="breakdown-bars">
            {breakdownItems.map((dim) => (
              <div key={dim.key} className="breakdown-row">
                <div className="breakdown-labels">
                  <span>{dim.label}</span>
                  <span className="breakdown-val">
                    {dim.score} / {dim.max}
                  </span>
                </div>
                <div className="bar-track">
                  <div
                    className="bar-fill"
                    style={{
                      width: `${dim.percentage}%`,
                    }}
                  />
                </div>
              </div>
            ))}
          </div>

          {disclaimer && <p className="score-disclaimer">{disclaimer}</p>}
        </div>
      </div>
    </div>
  );
}
