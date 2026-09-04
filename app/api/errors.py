from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.database_errors import (
    DatabaseConnectionError,
    DatabaseDuplicateError,
    DatabaseReferenceError,
    DatabaseValidationError,
)


class APIError(Exception):
    def __init__(
        self,
        status_code: int,
        message: str,
    ):
        self.status_code = status_code
        self.message = message

        super().__init__(message)


async def api_error_handler(
    request: Request,
    error: APIError,
):
    return JSONResponse(
        status_code=error.status_code,
        content={
            "detail": error.message,
        },
    )


async def database_duplicate_handler(
    request: Request,
    error: DatabaseDuplicateError,
):
    return JSONResponse(
        status_code=409,
        content={
            "detail": str(error),
        },
    )


async def database_reference_handler(
    request: Request,
    error: DatabaseReferenceError,
):
    return JSONResponse(
        status_code=400,
        content={
            "detail": str(error),
        },
    )


async def database_validation_handler(
    request: Request,
    error: DatabaseValidationError,
):
    return JSONResponse(
        status_code=400,
        content={
            "detail": str(error),
        },
    )


async def database_connection_handler(
    request: Request,
    error: DatabaseConnectionError,
):
    return JSONResponse(
        status_code=503,
        content={
            "detail": (
                "Database service is currently "
                "unavailable."
            ),
        },
    )


def register_exception_handlers(
    app: FastAPI,
) -> None:
    app.add_exception_handler(
        APIError,
        api_error_handler,
    )

    app.add_exception_handler(
        DatabaseDuplicateError,
        database_duplicate_handler,
    )

    app.add_exception_handler(
        DatabaseReferenceError,
        database_reference_handler,
    )

    app.add_exception_handler(
        DatabaseValidationError,
        database_validation_handler,
    )

    app.add_exception_handler(
        DatabaseConnectionError,
        database_connection_handler,
    )