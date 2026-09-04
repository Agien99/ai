from fastapi import FastAPI
from fastapi.middleware.cors import (
    CORSMiddleware,
)

from app.api.config import settings
from app.api.errors import (
    register_exception_handlers,
)
from app.api.routers.health import (
    router as health_router,
)
from app.api.routers.models import (
    router as models_router,
)
from app.api.routers.sessions import (
    router as sessions_router,
)


app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=(
        settings.cors_origins
    ),
    allow_credentials=False,
    allow_methods=[
        "GET",
        "POST",
        "OPTIONS",
    ],
    allow_headers=["*"],
)


register_exception_handlers(app)


app.include_router(
    health_router
)

app.include_router(
    sessions_router
)

app.include_router(
    models_router
)