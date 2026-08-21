"""Main FastAPI application entrypoint."""

import logging
import shutil
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.routes.analyze import router as analyze_router
from app.routes.reports import router as reports_router

# Configure clean logging format
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Full-stack social media content analysis, engagement scoring, and report generation API.",
)

# Configure CORS
origins = settings.cors_origins_list
if not origins or "*" in origins:
    cors_origins = ["*"]
else:
    cors_origins = origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins if cors_origins != ["*"] else ["*"],
    allow_credentials=True if cors_origins != ["*"] else False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global exception handler to ensure clean error messages without exposing stack traces."""
    logger.error("Unhandled exception processing request '%s': %s", request.url.path, str(exc), exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An internal server error occurred while processing your request. Please try again."
        },
    )


# Mount routers
app.include_router(analyze_router)
app.include_router(reports_router)


@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint for deployment monitoring and readiness probes."""
    has_gemini_key = bool(settings.GEMINI_API_KEY and settings.GEMINI_API_KEY.strip())
    tesseract_found = bool(shutil.which("tesseract") or shutil.which(r"C:\Program Files\Tesseract-OCR\tesseract.exe"))

    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "gemini_configured": has_gemini_key,
        "tesseract_available": tesseract_found,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
