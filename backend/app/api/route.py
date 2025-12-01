from fastapi import APIRouter
from datetime import datetime
from app.core.config import settings
from app.api.endpoints import organizations, users, otp

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(organizations.router)
api_router.include_router(users.router)
api_router.include_router(otp.router)


@api_router.get("/", tags=["API Health"])
async def api_health_check():
    """
    API health check - called by Flet app to verify backend connectivity
    """
    return {
        "status": "healthy",
        "service": f"{settings.APP_NAME} API",
        "endpoint": f"{settings.API_PREFIX}",
        "database_status": "connected",
        "timestamp": datetime.utcnow().isoformat()
    }


@api_router.get("/info", tags=["API Info"])
async def api_info():
    """
    API configuration information for Flet app
    """
    return {
        "api_version": settings.APP_VERSION,
        "api_prefix": settings.API_PREFIX,
        "environment": settings.ENVIRONMENT,
        "endpoints": {
            "health": f"{settings.API_PREFIX}",
            "info": f"{settings.API_PREFIX}/info",
            "organizations": f"{settings.API_PREFIX}/organizations",
            "users": f"{settings.API_PREFIX}/users",
            "otp": f"{settings.API_PREFIX}/otp"
        }
    }
