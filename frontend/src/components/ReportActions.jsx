import React, { useState } from 'react';
import { downloadDocxReport, downloadPdfReport } from '../services/api';

export default function ReportActions({ analysisData, onReset }) {
  const [downloadingPdf, setDownloadingPdf] = useState(false);
  const [downloadingDocx, setDownloadingDocx] = useState(false);
  const [reportError, setReportError] = useState(null);

  const handleDownloadPdf = async () => {
    if (!analysisData || downloadingPdf) return;
    setDownloadingPdf(true);
    setReportError(null);
    try {
      await downloadPdfReport(analysisData);
    } catch (err) {
      setReportError(err.message || 'Failed to download PDF report.');
    } finally {
      setDownloadingPdf(false);
    }
  };

  const handleDownloadDocx = async () => {
    if (!analysisData || downloadingDocx) return;
    setDownloadingDocx(true);
    setReportError(null);
    try {
      await downloadDocxReport(analysisData);
    } catch (err) {
      setReportError(err.message || 'Failed to download Word report.');
    } finally {
      setDownloadingDocx(false);
    }
  };

  return (
    <div className="report-actions-container" id="report-actions-section">
      <div className="report-actions-bar">
        <div className="action-buttons-group">
          <button
            type="button"
            id="btn-download-pdf"
            className="btn-primary"
            onClick={handleDownloadPdf}
            disabled={downloadingPdf}
          >
            {downloadingPdf ? (
              <>
                <div className="spinner" style={{ borderTopColor: '#fff' }} />
                <span>Generating PDF...</span>
              </>
            ) : (
              <>
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                  <polyline points="7 10 12 15 17 10"></polyline>
                  <line x1="12" y1="15" x2="12" y2="3"></line>
                </svg>
                <span>Download PDF Report</span>
              </>
            )}
          </button>

          <button
            type="button"
            id="btn-download-docx"
            className="btn-secondary"
            onClick={handleDownloadDocx}
            disabled={downloadingDocx}
          >
            {downloadingDocx ? (
              <>
                <div className="spinner" />
                <span>Generating Word...</span>
              </>
            ) : (
              <>
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                  <polyline points="14 2 14 8 20 8"></polyline>
                  <line x1="16" y1="13" x2="8" y2="13"></line>
                  <line x1="16" y1="17" x2="8" y2="17"></line>
                  <polyline points="10 9 9 9 8 9"></polyline>
                </svg>
                <span>Download Word Report</span>
              </>
            )}
          </button>
        </div>

        <button
          type="button"
          id="btn-analyze-another"
          className="btn-outline"
          onClick={onReset}
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="1 4 1 10 7 10"></polyline>
            <path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"></path>
          </svg>
          <span>Analyze Another File</span>
        </button>
      </div>

      {reportError && (
        <div className="error-banner" style={{ marginTop: '12px' }}>
          <span>{reportError}</span>
          <button type="button" onClick={() => setReportError(null)}>✕</button>
        </div>
      )}
    </div>
  );
}
