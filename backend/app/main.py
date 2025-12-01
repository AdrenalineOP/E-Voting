from fastapi import FastAPI
from datetime import datetime
from app.api.route import api_router
from app.core.config import settings
from app.db.database import create_db_and_tables

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)


# Create database tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    API information endpoint
    """
    return {
        "app": settings.APP_NAME,
        "message": f"{settings.APP_NAME} version {settings.APP_VERSION}",
        "version": settings.APP_VERSION,
        "type": "API Backend",
        "environment": settings.ENVIRONMENT,
        "status": "running",
        "timestamp": datetime.utcnow().isoformat()
    }


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check for monitoring backend status
    """
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "timestamp": datetime.utcnow().isoformat()
    }


# Include API router
app.include_router(api_router, prefix=settings.API_PREFIX)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
