/**
 * API service for communicating with the backend FastAPI endpoints.
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

/**
 * Upload and analyze a document or image file.
 * @param {File} file - The uploaded File object.
 * @returns {Promise<Object>} The analysis payload.
 */
export async function analyzeContent(file) {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE_URL}/api/analyze`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    let errorDetail = 'Failed to analyze content.';
    try {
      const errorJson = await response.json();
      if (errorJson.detail) {
        errorDetail = errorJson.detail;
      }
    } catch {
      errorDetail = `Server responded with status ${response.status}: ${response.statusText}`;
    }
    throw new Error(errorDetail);
  }

  return await response.json();
}

/**
 * Download a generated PDF report.
 * @param {Object} payload - The complete analysis payload.
 */
export async function downloadPdfReport(payload) {
  const response = await fetch(`${API_BASE_URL}/api/report/pdf`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    let errorDetail = 'Failed to generate PDF report.';
    try {
      const err = await response.json();
      if (err.detail) errorDetail = err.detail;
    } catch {
      // fallback to statusText
    }
    throw new Error(errorDetail);
  }

  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  const filename = `Social_Media_Analysis_${new Date().toISOString().slice(0, 10)}.pdf`;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  window.URL.revokeObjectURL(url);
  a.remove();
}

/**
 * Download a generated Word (.docx) report.
 * @param {Object} payload - The complete analysis payload.
 */
export async function downloadDocxReport(payload) {
  const response = await fetch(`${API_BASE_URL}/api/report/docx`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    let errorDetail = 'Failed to generate Word report.';
    try {
      const err = await response.json();
      if (err.detail) errorDetail = err.detail;
    } catch {
      // fallback
    }
    throw new Error(errorDetail);
  }

  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  const filename = `Social_Media_Analysis_${new Date().toISOString().slice(0, 10)}.docx`;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  window.URL.revokeObjectURL(url);
  a.remove();
}

/**
 * Check backend service health.
 */
export async function checkHealth() {
  const response = await fetch(`${API_BASE_URL}/health`);
  if (!response.ok) {
    throw new Error('Backend health check failed.');
  }
  return await response.json();
}
