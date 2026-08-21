import React, { useState } from 'react';
import './styles/main.css';
import './styles/components.css';

import UploadZone from './components/UploadZone';
import LoadingState from './components/LoadingState';
import ScoreCard from './components/ScoreCard';
import ContentMetrics from './components/ContentMetrics';
import AIReview from './components/AIReview';
import Suggestions from './components/Suggestions';
import ImprovedPost from './components/ImprovedPost';
import ReportActions from './components/ReportActions';

import { analyzeContent } from './services/api';

export default function App() {
  const [currentView, setCurrentView] = useState('upload'); // 'upload' | 'loading' | 'results'
  const [selectedFile, setSelectedFile] = useState(null);
  const [loadingStage, setLoadingStage] = useState(1);
  const [analysisData, setAnalysisData] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);

  const handleFileSelected = async (file) => {
    setSelectedFile(file);
    setCurrentView('loading');
    setLoadingStage(1);
    setErrorMessage(null);

    try {
      // Simulate real stage progression during extraction and analysis
      const stageTimer1 = setTimeout(() => setLoadingStage(2), 400);
      const stageTimer2 = setTimeout(() => setLoadingStage(3), 900);
      const stageTimer3 = setTimeout(() => setLoadingStage(4), 1500);

      const result = await analyzeContent(file);

      clearTimeout(stageTimer1);
      clearTimeout(stageTimer2);
      clearTimeout(stageTimer3);

      setAnalysisData(result);
      setCurrentView('results');
    } catch (err) {
      setErrorMessage(err.message || 'An error occurred while analyzing the document.');
      setCurrentView('upload');
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setAnalysisData(null);
    setErrorMessage(null);
    setCurrentView('upload');
  };

  return (
    <div className="app-container">
      {/* Header */}
      <header className="app-header">
        <div className="header-inner">
          <div className="brand-section">
            <div className="brand-title">
              <span>Social Media Content Analyzer</span>
              <span className="brand-badge">v1.0</span>
            </div>
            <span className="brand-tagline">Turn your content into clearer, stronger posts.</span>
          </div>

          {currentView === 'results' && (
            <button
              type="button"
              className="btn-outline"
              onClick={handleReset}
              style={{ padding: '6px 12px', fontSize: '12px' }}
            >
              New Analysis
            </button>
          )}
        </div>
      </header>

      {/* Main Container */}
      <main className="main-content">
        {currentView === 'upload' && (
          <UploadZone
            onFileSelected={handleFileSelected}
            isAnalyzing={false}
            error={errorMessage}
            onClearError={() => setErrorMessage(null)}
          />
        )}

        {currentView === 'loading' && (
          <LoadingState
            fileName={selectedFile?.name}
            currentStage={loadingStage}
          />
        )}

        {currentView === 'results' && analysisData && (
          <div className="results-view" id="analysis-results-root">
            {/* Top Bar with File Meta */}
            <div className="results-header">
              <div className="results-meta-title">
                <h2 className="filename-label">{analysisData.file_info?.filename}</h2>
                <span className="meta-chip">
                  {analysisData.file_info?.file_type?.toUpperCase()}
                </span>
                <span className="meta-chip">
                  {analysisData.file_info?.extraction_method}
                </span>
              </div>
            </div>

            {/* Results Grid */}
            <div className="results-grid">
              {/* 1. Score Card */}
              <ScoreCard scoreData={analysisData.score} />

              {/* 2. Content Metrics */}
              <ContentMetrics metrics={analysisData.metrics} />

              {/* 3. AI Editorial Review */}
              <AIReview aiReview={analysisData.ai_review} />

              {/* 4. Actionable Suggestions */}
              <Suggestions suggestions={analysisData.ai_review?.suggestions} />

              {/* 5. Improved Post Preview */}
              <ImprovedPost improvedPost={analysisData.ai_review?.improved_post} />

              {/* 6. Report Downloads & Reset */}
              <ReportActions
                analysisData={analysisData}
                onReset={handleReset}
              />
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <span>Social Media Content Analyzer · Professional Assessment & Optimization Tool</span>
      </footer>
    </div>
  );
}
