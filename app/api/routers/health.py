from fastapi import APIRouter

from app.api.config import settings
from app.api.schemas import HealthResponse


router = APIRouter(
    tags=["Health"],
)


@router.get(
    "/health",
    response_model=HealthResponse,
)
def health_check():
    return {
        "status": "ok",
        "service": settings.api_title,
        "version": settings.api_version,
    }