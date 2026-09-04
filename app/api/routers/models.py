from fastapi import APIRouter

from app.api.reporting import (
    APIReportingService,
)
from app.api.schemas import (
    ModelsResponse,
)


router = APIRouter(
    prefix="/models",
    tags=["Models"],
)


@router.get(
    "",
    response_model=ModelsResponse,
)
def get_models():
    return (
        APIReportingService
        .get_models()
    )