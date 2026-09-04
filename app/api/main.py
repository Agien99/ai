from fastapi import FastAPI

from app.api.config import settings
from app.api.errors import (
    register_exception_handlers,
)
from app.api.routers.health import (
    router as health_router,
)
from app.api.routers.sessions import (
    router as sessions_router,
)


app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
)


register_exception_handlers(app)


app.include_router(
    health_router
)

app.include_router(
    sessions_router
)