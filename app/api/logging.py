import logging
import sys
from time import perf_counter

from fastapi import Request


LOGGER_NAME = "roulette_ai.api"


def configure_logging(
    log_level: str = "INFO",
) -> logging.Logger:
    logger = logging.getLogger(
        LOGGER_NAME
    )

    level = getattr(
        logging,
        log_level.upper(),
        logging.INFO,
    )

    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler(
            sys.stdout
        )

        formatter = logging.Formatter(
            (
                "%(asctime)s "
                "%(levelname)s "
                "%(name)s "
                "%(message)s"
            )
        )

        handler.setFormatter(
            formatter
        )

        logger.addHandler(
            handler
        )

    logger.propagate = True

    return logger


async def request_logging_middleware(
    request: Request,
    call_next,
):
    logger = logging.getLogger(
        LOGGER_NAME
    )

    started = perf_counter()

    try:
        response = await call_next(
            request
        )

    except Exception:
        duration_ms = (
            perf_counter() - started
        ) * 1000

        logger.exception(
            (
                "request_failed "
                "method=%s path=%s "
                "duration_ms=%.2f"
            ),
            request.method,
            request.url.path,
            duration_ms,
        )

        raise

    duration_ms = (
        perf_counter() - started
    ) * 1000

    logger.info(
        (
            "request_complete "
            "method=%s path=%s "
            "status=%s "
            "duration_ms=%.2f"
        ),
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )

    return response