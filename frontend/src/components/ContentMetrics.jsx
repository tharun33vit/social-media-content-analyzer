import React from 'react';

export default function ContentMetrics({ metrics }) {
  if (!metrics) return null;

  const items = [
    { label: 'Words', value: metrics.word_count, sub: `${metrics.character_count} chars` },
    { label: 'Sentences', value: metrics.sentence_count, sub: `~${metrics.average_sentence_length} w/sent` },
    { label: 'Paragraphs', value: metrics.paragraph_count, sub: 'Structure' },
    { label: 'Hashtags', value: metrics.hashtag_count, sub: metrics.hashtags?.length > 0 ? metrics.hashtags.slice(0, 2).join(' ') : 'None' },
    { label: 'Mentions', value: metrics.mention_count, sub: metrics.mentions?.length > 0 ? metrics.mentions.slice(0, 2).join(' ') : 'None' },
    { label: 'URLs / Links', value: metrics.url_count, sub: metrics.url_count > 0 ? 'Detected' : 'None' },
    { label: 'Question Hook', value: metrics.has_question ? 'Yes' : 'No', sub: `${metrics.question_count} questions` },
    { label: 'Call to Action', value: metrics.has_cta ? 'Detected' : 'None', sub: metrics.detected_ctas?.length > 0 ? metrics.detected_ctas[0] : 'Missing' },
    { label: 'Readability', value: metrics.readability_score, sub: metrics.readability_grade },
  ];

  return (
    <div className="card" id="content-metrics-section">
      <div className="card-title">
        <span>Content Metrics Snapshot</span>
        <span className="meta-chip">Deterministic</span>
      </div>

      <div className="metrics-grid">
        {items.map((item, idx) => (
          <div key={idx} className="metric-box">
            <span className="metric-label">{item.label}</span>
            <span className="metric-value">{item.value}</span>
            <span className="metric-sub">{item.sub}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
