import React, { useState, useRef } from 'react';

const ALLOWED_EXTENSIONS = ['.pdf', '.png', '.jpg', '.jpeg', '.webp'];
const MAX_FILE_SIZE_MB = 10;
const MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024;

export default function UploadZone({ onFileSelected, isAnalyzing, error, onClearError }) {
  const [isDragOver, setIsDragOver] = useState(false);
  const [dragError, setDragError] = useState(null);
  const fileInputRef = useRef(null);

  const validateAndProcessFile = (file) => {
    if (!file) return;

    // Reset errors
    setDragError(null);
    if (onClearError) onClearError();

    // Check size
    if (file.size === 0) {
      setDragError('The selected file is empty. Please choose a valid document or image.');
      return;
    }

    if (file.size > MAX_FILE_SIZE_BYTES) {
      const sizeMb = (file.size / (1024 * 1024)).toFixed(1);
      setDragError(`File size (${sizeMb} MB) exceeds the maximum limit of ${MAX_FILE_SIZE_MB} MB.`);
      return;
    }

    // Check extension
    const fileName = file.name.toLowerCase();
    const isAllowed = ALLOWED_EXTENSIONS.some((ext) => fileName.endsWith(ext));
    if (!isAllowed) {
      setDragError(`Unsupported file format. Please upload a PDF or standard image (${ALLOWED_EXTENSIONS.join(', ')}).`);
      return;
    }

    onFileSelected(file);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(false);

    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      validateAndProcessFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileInputChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      validateAndProcessFile(e.target.files[0]);
    }
  };

  const displayError = dragError || error;

  return (
    <div className="upload-container">
      <h1 className="upload-heading">Review your content before you publish.</h1>
      <p className="upload-subheading">
        Upload a draft PDF document or image screenshot to extract text, measure engagement readiness, and receive structured editorial suggestions.
      </p>

      <div
        id="dropzone-upload"
        className={`dropzone ${isDragOver ? 'active' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current && fileInputRef.current.click()}
        role="button"
        tabIndex={0}
      >
        <input
          id="file-input-hidden"
          type="file"
          ref={fileInputRef}
          onChange={handleFileInputChange}
          accept=".pdf,.png,.jpg,.jpeg,.webp"
          style={{ display: 'none' }}
          disabled={isAnalyzing}
        />

        <div className="dropzone-icon-container">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="17 8 12 3 7 8"></polyline>
            <line x1="12" y1="3" x2="12" y2="15"></line>
          </svg>
        </div>

        <p className="dropzone-instruction">Drop your document or image here</p>
        <span className="dropzone-or">or click to browse from your device</span>

        <button
          type="button"
          id="btn-select-file"
          className="btn-choose-file"
          disabled={isAnalyzing}
          onClick={(e) => {
            e.stopPropagation();
            fileInputRef.current && fileInputRef.current.click();
          }}
        >
          Choose File
        </button>

        <div className="format-badges">
          <span className="format-badge">PDF</span>
          <span className="format-badge">PNG</span>
          <span className="format-badge">JPG</span>
          <span className="format-badge">JPEG</span>
          <span className="format-badge">WEBP</span>
          <span className="format-badge">Max {MAX_FILE_SIZE_MB}MB</span>
        </div>
      </div>

      {displayError && (
        <div id="upload-error-banner" className="error-banner">
          <span>{displayError}</span>
          <button
            type="button"
            onClick={() => {
              setDragError(null);
              if (onClearError) onClearError();
            }}
          >
            ✕
          </button>
        </div>
      )}
    </div>
  );
}
