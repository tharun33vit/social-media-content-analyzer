import React from 'react';

export default function LoadingState({ fileName, currentStage = 2 }) {
  const steps = [
    { id: 1, label: 'Uploading file securely' },
    { id: 2, label: 'Extracting text and document structure' },
    { id: 3, label: 'Calculating metrics & engagement readiness score' },
    { id: 4, label: 'Generating qualitative review & recommendations' },
  ];

  return (
    <div className="loading-card" id="loading-state-container">
      <h2 className="loading-title">Analyzing Content</h2>
      <p className="loading-subtitle">
        Processing <strong>{fileName || 'document'}</strong>
      </p>

      <div className="loading-steps">
        {steps.map((step) => {
          let statusClass = '';
          let indicator = null;

          if (step.id < currentStage) {
            statusClass = 'completed';
            indicator = (
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" style={{ color: 'var(--score-high)' }}>
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
            );
          } else if (step.id === currentStage) {
            statusClass = 'active';
            indicator = <div className="spinner" />;
          } else {
            statusClass = 'pending';
            indicator = <span style={{ color: 'var(--text-dim)' }}>○</span>;
          }

          return (
            <div key={step.id} className={`loading-step ${statusClass}`}>
              <div className="step-indicator">{indicator}</div>
              <span>{step.label}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
