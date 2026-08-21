import React, { useState } from 'react';

export default function ImprovedPost({ improvedPost = '' }) {
  const [copied, setCopied] = useState(false);

  if (!improvedPost || !improvedPost.trim()) return null;

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(improvedPost);
      setCopied(true);
      setTimeout(() => setCopied(false), 2500);
    } catch {
      // Fallback copy
      const textArea = document.createElement('textarea');
      textArea.value = improvedPost;
      document.body.appendChild(textArea);
      textArea.select();
      document.execCommand('copy');
      document.body.removeChild(textArea);
      setCopied(true);
      setTimeout(() => setCopied(false), 2500);
    }
  };

  return (
    <div className="card" id="improved-post-section">
      <div className="card-title">
        <span>Improved Post (Strategic Rewrite)</span>
        <span className="meta-chip">Context-Preserving</span>
      </div>

      <div className="improved-post-box">
        {improvedPost}
      </div>

      <div className="improved-post-footer">
        <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
          Preserves original premise with improved hook, cadence, and action clarity.
        </span>

        <button
          type="button"
          id="btn-copy-improved-post"
          className={`btn-copy ${copied ? 'copied' : ''}`}
          onClick={handleCopy}
        >
          {copied ? (
            <>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Copied to Clipboard</span>
            </>
          ) : (
            <>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
              </svg>
              <span>Copy to Clipboard</span>
            </>
          )}
        </button>
      </div>
    </div>
  );
}
