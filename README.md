# Social Media Content Analyzer

A full-stack, production-grade application designed to analyze uploaded social media content (PDF documents and image screenshots/scans), compute an objective 100-point **Engagement Readiness Score**, deliver structured editorial critiques via Google Gemini, and generate downloadable assessment reports in **PDF** and **Word (.docx)** formats.

## 🚀 Live Demo

👉 **[Open the Social Media Content Analyzer](https://social-media-content-analyzer-frontend-y19w.onrender.com)**

> The free Render instance may take up to a minute to wake up after inactivity.

---

## Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [How It Works](#how-it-works)
- [PDF Extraction & Image OCR](#pdf-extraction--image-ocr)
- [AI Analysis (Google Gemini Integration)](#ai-analysis-google-gemini-integration)
- [Scoring Methodology (/100 Breakdown)](#scoring-methodology-100-breakdown)
- [Report Generation (PDF & DOCX)](#report-generation-pdf--docx)
- [Project Structure](#project-structure)
- [Local Setup & Installation](#local-setup--installation)
- [Environment Variables](#environment-variables)
- [Tesseract OCR Installation](#tesseract-ocr-installation)
- [Running Locally](#running-locally)
- [Running Tests](#running-tests)
- [API Endpoints](#api-endpoints)
- [Deployment Guide](#deployment-guide)
- [Privacy & Security Considerations](#privacy--security-considerations)
- [Known Limitations & Future Roadmap](#known-limitations--future-roadmap)
- [Approach Write-Up (<=200 words)](#approach-write-up-200-words)

---

## Overview

The **Social Media Content Analyzer** helps creators, founders, and marketing professionals review and optimize social media posts before publishing. The application accepts PDFs or screenshot images, extracts text structure, computes objective readability and social engagement metrics, layers contextual AI insights, and outputs actionable recommendations with a refined post rewrite.

---

## Key Features

- **Multi-Format Ingestion**: Supports PDF documents, PNG, JPG, JPEG, and WebP images.
- **Robust Text Extraction**: High-fidelity text extraction via **PyMuPDF** (`fitz`) and optical character recognition via **Tesseract OCR** (`pytesseract`).
- **Hybrid Analysis Architecture**: Fast deterministic metric calculation combined with Google Gemini semantic analysis.
- **Transparent 100-Point Scoring Engine**: Evaluated across 7 clear heuristic dimensions with full score breakdown.
- **Resilient Fallback Mechanism**: Seamlessly falls back to a deterministic rule-based analysis engine if the Gemini API key is missing, rate-limited, or unavailable.
- **Strategic Post Rewrite**: Generates an improved version that preserves original facts and voice without clickbait or hallucinations.
- **Professional Report Generation**: Generates styled **PDF reports** (via ReportLab) and editable **Word reports** (via `python-docx`).
- **Clean Editorial UI/UX**: Human-designed, distraction-free interface built with React + Vite, featuring stage-based loading indicators, copy-to-clipboard interactions, and responsive layouts.

---

## Architecture

The system utilizes a clean hybrid pipeline that separates deterministic data extraction from qualitative AI interpretation:

```
[ User Upload (PDF / PNG / JPG / WebP) ]
                   │
                   ▼
       [ Backend Validation ] (Magic bytes, extension, size limit <= 10MB)
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
 [ PDF Extractor ]     [ Image OCR Service ]
 (PyMuPDF / fitz)      (Pillow + Tesseract)
         └─────────┬─────────┘
                   ▼
         [ Extracted Text ]
                   │
         ┌─────────┴─────────────────────┐
         ▼                               ▼
[ Deterministic Analyzer ]      [ Gemini LLM Service ]
• Word/Char/Sentence count       • google-genai structured output
• Hashtag/Mention/URL counts    • Semantic strengths & weaknesses
• Question & CTA detection      • Hook, clarity, audience, tone
• Readability indicator         • Actionable recommendations
• /100 Engagement Score         • Context-preserving rewritten post
         │                               │
         │                      (Fallback if error/no key)
         └─────────┬─────────────────────┘
                   ▼
        [ Unified Analysis Result ]
                   │
         ┌─────────┴─────────────────────┐
         ▼                               ▼
  [ Frontend Results View ]     [ Report Generator ]
  • Hero Score + breakdown       • Downloadable PDF (ReportLab)
  • Metric snapshot grid         • Downloadable DOCX (python-docx)
  • AI Review & Recommendations
  • Improved post + Copy action
```

---

## Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend** | Python 3.12, FastAPI, Uvicorn | High-performance asynchronous REST API |
| **Data Validation** | Pydantic v2, Pydantic Settings | Strict schema validation and config management |
| **PDF Extraction** | PyMuPDF (`pymupdf` / `fitz`) | Multi-page text extraction and boundary parsing |
| **Image OCR** | Pillow, Pytesseract, Tesseract OCR | Image preprocessing and optical character recognition |
| **AI / LLM** | Google `google-genai` SDK | Structured semantic critique using `gemini-3.6-flash` |
| **PDF Reports** | ReportLab | Programmatic PDF report design with custom layouts |
| **Word Reports** | `python-docx` | Native Microsoft Word (.docx) report generation |
| **Testing** | Pytest, HTTPX | Unit, integration, and endpoint automated test suite |
| **Frontend** | React 19, Vite | Fast, responsive single-page user interface |
| **Styling** | Vanilla CSS (CSS Variables) | Bespoke design system without heavy UI framework bloat |

---

## How It Works

1. **Upload & Validate**: The user uploads a PDF or image via drag-and-drop or file picker. The backend validates file size (max 10MB), extension, and binary magic-byte signatures.
2. **Text Extraction**: The backend routes PDFs to PyMuPDF and images to Pillow + Tesseract OCR.
3. **Deterministic Analysis**: The backend calculates word count, character count, sentence count, paragraph count, hashtag/mention/URL frequency, question detection, CTA detection, and Flesch Reading Ease score.
4. **100-Point Score Calculation**: Evaluates the 7 structured dimensions to calculate the Engagement Readiness Score.
5. **Gemini Semantic Layer**: The backend calls Gemini (`gemini-3.6-flash`) via `google-genai` with structured JSON schema output to receive qualitative strengths, weaknesses, dimensional reviews, suggestions, and a refined rewrite.
6. **Results & Downloads**: The frontend displays interactive score gauges, metric chips, critique cards, and enables one-click copy and instant PDF / DOCX report downloads.

---

## PDF Extraction & Image OCR

- **PDF Documents (`pdf_extractor.py`)**:
  - Processes single and multi-page PDFs using PyMuPDF.
  - Extracts text from all pages while preserving line breaks, paragraph structure, and page boundaries.
  - Gracefully detects scanned or empty PDFs (zero selectable text) and alerts the user with an actionable recommendation to upload an image format instead.
- **Images & Screenshots (`ocr_service.py`)**:
  - Validates image integrity and converts to optimized grayscale with auto-contrast adjustment for maximum optical character definition.
  - Leverages Tesseract OCR engine via `pytesseract`.
  - Handles missing Tesseract binaries gracefully, returning a friendly error message without exposing internal stack traces.

---

## AI Analysis (Google Gemini Integration)

- **Official SDK**: Built using Google's official `google-genai` Python SDK.
- **Model Configuration**: Configured with `gemini-3.6-flash` by default. Model name is dynamically configurable via the `GEMINI_MODEL` environment variable.
- **Strict Structured Output**: Uses Pydantic schema validation (`StructuredGeminiAnalysis`) via `response_schema` to guarantee consistent JSON response contracts:
  - `overall_assessment` (2–3 sentence executive summary)
  - `strengths` (2–4 key strengths)
  - `areas_for_improvement` (2–4 improvement areas)
  - `hook_analysis`, `clarity_analysis`, `engagement_analysis`, `cta_analysis`, `audience_analysis`, `tone`
  - `suggestions` (3–5 items, each containing `title`, `issue`, `recommendation`, `reason`)
  - `improved_post` (Context-preserving rewrite)
- **Zero-Failure Fallback**: If `GEMINI_API_KEY` is not provided, or if the API encounters a rate limit, network timeout, or error, the application automatically invokes `generate_rule_based_fallback()`. The user receives complete, structured recommendations and a rewritten post without system downtime.

---

## Scoring Methodology (/100 Breakdown)

The **Content & Engagement Score** (or *Engagement Readiness Score*) is calculated deterministically on the backend to maintain analytical consistency:

| Dimension | Max Points | Evaluation Criteria |
| :--- | :---: | :--- |
| **1. Hook / Opening** | **20 pts** | First line length (ideal: 25–110 characters), intrigue/question triggers, numbers, and punchy lead-in phrasing. |
| **2. Clarity & Readability** | **20 pts** | Average sentence length (ideal: 8–18 words/sentence) and Flesch Reading Ease index (target: 60–85). |
| **3. Engagement Potential** | **20 pts** | Presence of questions (1–3 optimal), conversational trigger words ("thoughts?", "agree?"), and reader-directed pronouns ("you", "your", "we"). |
| **4. Call-to-Action (CTA)** | **15 pts** | Detection of explicit CTA keywords ("comment below", "link in bio", "save for later", "dm", "sign up") and strategic bottom-half placement. |
| **5. Content Structure** | **10 pts** | Visual spacing, paragraph breaks (>=2 paragraphs), scannable lists/bullet points, and avoidance of dense text walls. |
| **6. Hashtag Strategy** | **5 pts** | Hashtag density (1–5 hashtags ideal: 5 pts; >8: penalized; 0: standard partial credit). |
| **7. Audience & Format Fit** | **10 pts** | Optimal word count for modern social feeds (40–260 words optimal) and balanced URL/mention usage. |
| **Total** | **100 pts** | *Analytical heuristic indicating engagement readiness, not a guarantee of impressions or likes.* |

---

## Report Generation (PDF & DOCX)

Both report formats are generated natively on the backend directly from the analysis payload:

1. **PDF Report (`report_generator.py`)**:
   - Built with **ReportLab**.
   - Features structured header metadata, visual score banner, two-column metrics table, editorial critique side-by-side boxes (Strengths vs. Improvements), dimensional evaluations, numbered recommendation cards, and the complete rewritten post.
2. **Word Report (`report_generator.py`)**:
   - Built with **`python-docx`**.
   - Includes styled title headings, shaded metadata tables, metrics snapshot, bulleted critique lists, recommendation breakdown with strategic rationale, and a styled callout box for the rewritten post.

---

## Project Structure

```
social-media-content-analyzer/
│
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── analyze.py          # POST /api/analyze endpoint
│   │   │   └── reports.py          # POST /api/report/pdf & /api/report/docx endpoints
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── pdf_extractor.py    # PyMuPDF text extractor
│   │   │   ├── ocr_service.py      # Pillow + Tesseract OCR pipeline
│   │   │   ├── content_analyzer.py # Deterministic metrics & /100 score engine
│   │   │   ├── gemini_analyzer.py  # google-genai SDK structured analyzer & fallback
│   │   │   └── report_generator.py # ReportLab PDF & python-docx Word builders
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   └── validation.py       # File size, magic bytes, MIME validation
│   │   ├── config.py               # Pydantic Settings
│   │   └── main.py                 # FastAPI app, CORS middleware, /health probe
│   ├── tests/
│   │   ├── conftest.py             # Shared fixtures (TestClient, sample files, payload)
│   │   ├── test_health.py          # Health check tests
│   │   ├── test_validation.py      # File validation tests (empty, size, magic bytes)
│   │   ├── test_pdf_extractor.py   # PDF parsing & scanned PDF tests
│   │   ├── test_ocr_service.py     # OCR handler & missing Tesseract tests
│   │   ├── test_content_analyzer.py# Metric & score calculation unit tests
│   │   ├── test_gemini_analyzer.py # Gemini structured output & fallback tests (mocked)
│   │   ├── test_reports.py         # PDF & DOCX generation validation
│   │   └── test_api_analyze.py     # Integration endpoint tests
│   ├── requirements.txt            # Minimal backend dependencies
│   └── .env.example                # Environment configuration template
│
├── frontend/
│   ├── public/
│   │   └── favicon.svg             # Application favicon
│   ├── src/
│   │   ├── components/
│   │   │   ├── UploadZone.jsx      # Drag & drop upload area with validation
│   │   │   ├── LoadingState.jsx    # Real stage-based progress indicator
│   │   │   ├── ScoreCard.jsx       # 100-point score gauge with category breakdown
│   │   │   ├── ContentMetrics.jsx  # Compact metric chips grid
│   │   │   ├── AIReview.jsx        # Overall assessment, strengths, improvements
│   │   │   ├── Suggestions.jsx     # Actionable recommendation cards
│   │   │   ├── ImprovedPost.jsx    # Rewritten post preview with 1-click Copy
│   │   │   └── ReportActions.jsx   # PDF / DOCX download buttons & reset action
│   │   ├── services/
│   │   │   └── api.js              # Fetch client for backend API
│   │   ├── styles/
│   │   │   ├── variables.css       # Design tokens (colors, typography, shadows)
│   │   │   ├── main.css            # Base resets and container layout
│   │   │   └── components.css      # Component styles
│   │   ├── App.jsx                 # Main state flow manager
│   │   ├── index.css               # Global stylesheet entry
│   │   └── main.jsx                # React root mount
│   ├── index.html                  # HTML template with SEO meta tags
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
│
├── demo_samples/                   # Sample test PDF and PNG assets
├── tests_e2e.py                    # Live end-to-end integration test script
├── .gitignore                      # Complete ignore rules for env, node_modules, etc.
├── LICENSE                         # MIT License
└── README.md                       # Complete documentation
```

---

## Local Setup & Installation

### Prerequisites
- **Python**: Version 3.10, 3.11, or 3.12
- **Node.js**: Version 18+ (Node 20 or 22 recommended)
- **Tesseract OCR**: (Required for image OCR analysis)

---

### Step 1: Clone Repository & Configure Backend

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment (optional but recommended)
python -m venv venv
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# On macOS/Linux:
source venv/bin/activate

# Install backend dependencies
pip install -r requirements.txt

# Create .env file from example
copy .env.example .env      # Windows
# or: cp .env.example .env  # macOS/Linux
```

Configure your `.env` file:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
GEMINI_MODEL=gemini-3.6-flash
MAX_UPLOAD_SIZE_MB=10
CORS_ORIGINS=http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173
```
*(Note: If `GEMINI_API_KEY` is left blank, the application will automatically operate in deterministic rule-based analysis mode without crashing).*

---

### Step 2: Configure Frontend

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install

# Create .env file from example
copy .env.example .env      # Windows
# or: cp .env.example .env  # macOS/Linux
```

---

## Environment Variables

### Backend (`backend/.env`)

| Variable | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `GEMINI_API_KEY` | String | *None* | Google Gemini API key. If unset, fallback mode is used. |
| `GEMINI_MODEL` | String | `gemini-3.6-flash` | Gemini model name (e.g. `gemini-3.6-flash`). |
| `MAX_UPLOAD_SIZE_MB`| Integer| `10` | Maximum allowed file upload size in megabytes. |
| `CORS_ORIGINS` | String | `http://localhost:5173,...` | Comma-separated list of allowed CORS origins. |
| `TESSERACT_CMD` | String | *None* | Custom binary path to `tesseract.exe` if not in PATH. |

### Frontend (`frontend/.env`)

| Variable | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `VITE_API_BASE_URL` | String | `http://localhost:8000` | Backend API URL for requests. |

---

## Tesseract OCR Installation

### Windows
1. Download the official installer from [UB-Mannheim Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki).
2. Run the installer (default path: `C:\Program Files\Tesseract-OCR\tesseract.exe`).
3. Add `C:\Program Files\Tesseract-OCR` to your system `PATH` environment variable, or configure `TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe` in `backend/.env`.

### macOS
```bash
brew install tesseract
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update && sudo apt install -y tesseract-ocr
```

---

## Running Locally

### Start Backend API Server
```bash
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
API will be live at: `http://127.0.0.1:8000`  
API Interactive Docs: `http://127.0.0.1:8000/docs`

### Start Frontend Application
```bash
cd frontend
npm run dev -- --port 5173
```
Frontend will be accessible at: `http://127.0.0.1:5173`

---

## Running Tests

### Automated Backend Tests (Pytest)
```bash
# Run full suite (28 test cases)
pytest backend/tests -v
```

### Live End-to-End Test (with running server)
```bash
python tests_e2e.py
```

### Build Frontend Verification
```bash
cd frontend
npm run build
```

---

## API Endpoints

### 1. Ingest & Analyze Content
- **Endpoint**: `POST /api/analyze`
- **Content-Type**: `multipart/form-data`
- **Payload**: `file` (Binary document or image)
- **Response**:
```json
{
  "file_info": {
    "filename": "draft.pdf",
    "file_type": "pdf",
    "size_bytes": 14200,
    "extraction_method": "PyMuPDF Text Extraction",
    "page_count": 1,
    "char_count": 420
  },
  "extracted_text": "...",
  "metrics": {
    "word_count": 68,
    "character_count": 420,
    "sentence_count": 5,
    "paragraph_count": 3,
    "hashtag_count": 3,
    "hashtags": ["#SaaS", "#Growth", "#Tech"],
    "has_question": true,
    "has_cta": true,
    "readability_score": 72.4,
    "readability_grade": "Easy / Conversational"
  },
  "score": {
    "total_score": 88,
    "verdict": "High engagement readiness with a compelling hook, balanced structure, and clear action path.",
    "breakdown": {
      "hook_opening": { "score": 18, "max": 20, "label": "Hook & Opening" },
      "clarity_readability": { "score": 19, "max": 20, "label": "Clarity & Readability" },
      "engagement_potential": { "score": 18, "max": 20, "label": "Engagement Potential" },
      "call_to_action": { "score": 13, "max": 15, "label": "Call-to-Action" },
      "content_structure": { "score": 9, "max": 10, "label": "Content Structure" },
      "hashtag_strategy": { "score": 5, "max": 5, "label": "Hashtag Strategy" },
      "audience_format": { "score": 6, "max": 10, "label": "Audience & Format Fit" }
    },
    "disclaimer": "This score is an analytical heuristic for engagement readiness, not a guarantee of impressions, reach, or likes."
  },
  "ai_review": {
    "ai_status": "success",
    "overall_assessment": "...",
    "strengths": ["..."],
    "areas_for_improvement": ["..."],
    "hook_analysis": "...",
    "clarity_analysis": "...",
    "engagement_analysis": "...",
    "cta_analysis": "...",
    "audience_analysis": "...",
    "tone": "Professional & Educational",
    "suggestions": [
      {
        "title": "Sharpen Hook",
        "issue": "...",
        "recommendation": "...",
        "reason": "..."
      }
    ],
    "improved_post": "..."
  }
}
```

### 2. Download PDF Report
- **Endpoint**: `POST /api/report/pdf`
- **Content-Type**: `application/json`
- **Payload**: Full analysis JSON object
- **Response**: Binary stream with `Content-Type: application/pdf`

### 3. Download Word Report
- **Endpoint**: `POST /api/report/docx`
- **Content-Type**: `application/json`
- **Payload**: Full analysis JSON object
- **Response**: Binary stream with `Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document`

### 4. Health Check
- **Endpoint**: `GET /health`
- **Response**:
```json
{
  "status": "healthy",
  "service": "Social Media Content Analyzer",
  "version": "1.0.0",
  "gemini_configured": true,
  "tesseract_available": true
}
```

---

## Deployment Guide

### Backend Deployment (e.g. Render, Railway, Fly.io, or VPS)
1. Configure Python 3.12 environment with `pip install -r requirements.txt`.
2. Ensure `tesseract-ocr` system package is installed on the host container.
3. Configure environment variables in the host dashboard:
   - `GEMINI_API_KEY`
   - `GEMINI_MODEL=gemini-3.6-flash`
   - `CORS_ORIGINS=https://your-frontend-domain.com`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Frontend Deployment (e.g. Vercel, Netlify, Cloudflare Pages)
1. Build command: `npm run build`
2. Output directory: `dist`
3. Configure environment variable:
   - `VITE_API_BASE_URL=https://your-backend-api-domain.com`

---

## Privacy & Security Considerations

- **No Permanent Storage**: Uploaded files and extracted texts are processed entirely in-memory and are never written to a persistent database.
- **Backend Key Isolation**: `GEMINI_API_KEY` is loaded strictly on the backend and is never sent to or accessible by the browser client.
- **Safe Logging**: The backend never logs secret API keys or full user document payloads.
- **Transparent LLM Transmission**: When Gemini analysis is active, extracted document text is transmitted to Google's official Gemini API endpoint for qualitative processing.

---

## Known Limitations & Future Roadmap

- **Scanned PDF Optical OCR**: Scanned PDFs with no selectable text currently prompt the user to upload the document as a standard image (PNG/JPG) for OCR. Adding direct PDF-to-image OCR rendering is planned for v1.1.
- **Multi-Image Batch Ingestion**: Ingesting multi-image carousels in a single batch upload is targeted for a future release.
- **Platform-Specific Format Targeters**: Direct profile selectors for character count limits (e.g., X 280 chars vs. LinkedIn 3,000 chars vs. Threads).

---

## Approach Write-Up (<=200 words)

This application implements a resilient, hybrid architecture designed for production reliability, objective measurement, and qualitative depth. Rather than relying solely on non-deterministic LLM generations, the system establishes a deterministic foundation using PyMuPDF and Tesseract OCR for robust document extraction, paired with an algorithmic analyzer calculating objective metrics (readability, structure, hook length, and call-to-action signals). These metrics drive a transparent, 100-point Content & Engagement Readiness Score calculated entirely on the backend.

On top of this foundation, Google Gemini (`gemini-3.6-flash` via the official `google-genai` SDK) provides contextual qualitative critique, identifying nuanced strengths, areas for improvement, actionable suggestions, and an authentic, fact-preserving post rewrite using strict Pydantic JSON schemas. If the Gemini API key is omitted, rate-limited, or encounters network timeouts, the system automatically falls back to an integrated rule-based analysis engine without service disruption.

The frontend adopts a restrained, editorial developer-tool aesthetic built with React and modern CSS, avoiding generic AI tropes. Real multi-stage loading indicators communicate processing progress, and native backend PDF (ReportLab) and Word (.docx) generators produce downloadable assessment reports directly from the analysis payload.
