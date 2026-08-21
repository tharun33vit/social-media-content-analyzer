import React from 'react';

export default function Suggestions({ suggestions = [] }) {
  if (!suggestions || suggestions.length === 0) return null;

  return (
    <div className="card" id="actionable-suggestions-section">
      <div className="card-title">
        <span>Actionable Recommendations</span>
        <span className="meta-chip">{suggestions.length} Improvements</span>
      </div>

      <div className="suggestions-list">
        {suggestions.map((sug, idx) => (
          <div key={idx} className="suggestion-card">
            <div className="suggestion-header">
              <span className="suggestion-index">
                {String(idx + 1).padStart(2, '0')}
              </span>
              <h3 className="suggestion-title">{sug.title}</h3>
            </div>

            <div className="suggestion-body">
              <div>
                <span className="sug-row-label">Issue: </span>
                <span>{sug.issue}</span>
              </div>
              <div>
                <span className="sug-row-label">Recommendation: </span>
                <span>{sug.recommendation}</span>
              </div>
              {sug.reason && (
                <div className="sug-reason">
                  <strong>Why it matters:</strong> {sug.reason}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
