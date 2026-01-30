"""
SIRA Platform - WSGI-Compatible Entry Point
For PythonAnywhere deployment (no async middleware)
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import logging
import os

from app.core.config import settings
from app.core.database import init_db
from app.api import api_router

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Frontend dist path (for PythonAnywhere)
FRONTEND_DIST = os.environ.get('FRONTEND_DIST', '/home/sackson/sira/frontend/dist')

# Create FastAPI application (without lifespan for WSGI compatibility)
app = FastAPI(
    title=settings.APP_NAME,
    description="SIRA Platform API - Shipping Intelligence & Risk Analytics",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Initialize database on import
try:
    init_db()
    logger.info("Database initialized")
except Exception as e:
    logger.error(f"Database initialization failed: {e}")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring"""
    from datetime import datetime, timezone
    from app.core.database import check_db_connection

    db_status = "healthy" if check_db_connection() else "unhealthy"

    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "version": settings.APP_VERSION,
        "database": db_status,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


# Include API router
app.include_router(api_router, prefix="/api")

# Mount static files for frontend assets (if dist exists)
if os.path.exists(os.path.join(FRONTEND_DIST, 'assets')):
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIST, 'assets')), name="assets")

# Serve frontend for all non-API routes (SPA catch-all)
@app.get("/{full_path:path}", tags=["Frontend"])
async def serve_frontend(request: Request, full_path: str):
    """Serve frontend SPA for all non-API routes"""
    # Don't serve frontend for API paths
    if full_path.startswith("api/") or full_path in ["docs", "redoc", "openapi.json", "health"]:
        return JSONResponse(status_code=404, content={"detail": "Not found"})

    index_path = os.path.join(FRONTEND_DIST, 'index.html')
    if os.path.exists(index_path):
        return FileResponse(index_path, media_type="text/html")

    # Fallback to API info if frontend not deployed
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": "Shipping Intelligence & Risk Analytics Platform",
        "docs": "/docs",
        "health": "/health",
        "note": "Frontend not deployed. Upload frontend/dist to serve the UI."
    }
