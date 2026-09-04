from uuid import UUID

from fastapi import APIRouter, status

from app.api.errors import APIError
from app.api.schemas import (
    InitialSpinsRequest,
    SessionResponse,
)
from app.session import RouletteSession
from app.session_repository import (
    SessionRepository,
)
from app.session_storage_service import (
    SessionStorageService,
)
from app.spin_repository import (
    SpinRepository,
)


router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"],
)


@router.post(
    "",
    response_model=SessionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_session():
    session = RouletteSession()

    return SessionRepository.create_session(
        session
    )


@router.get(
    "/{session_id}",
    response_model=SessionResponse,
)
def get_session(
    session_id: UUID,
):
    session = SessionRepository.get_session(
        str(session_id)
    )

    if session is None:
        raise APIError(
            status_code=404,
            message="Session not found.",
        )

    return session


@router.post(
    "/{session_id}/initial-spins",
    response_model=SessionResponse,
)
def add_initial_spins(
    session_id: UUID,
    request: InitialSpinsRequest,
):
    session = (
        SessionStorageService.load_session(
            str(session_id)
        )
    )

    if session is None:
        raise APIError(
            status_code=404,
            message="Session not found.",
        )

    if session.status != "NEW":
        raise APIError(
            status_code=409,
            message=(
                "Initial spins have already "
                "been submitted for this session."
            ),
        )

    try:
        session.start(
            request.spins
        )

    except ValueError as error:
        raise APIError(
            status_code=400,
            message=str(error),
        ) from error

    SessionRepository.update_session(
        session
    )

    for spin_index, number in enumerate(
        request.spins,
        start=1,
    ):
        SpinRepository.create_spin(
            session_id=session.session_id,
            spin_index=spin_index,
            number=number,
            spin_type="INITIAL",
        )

    stored_session = (
        SessionRepository.get_session(
            session.session_id
        )
    )

    if stored_session is None:
        raise APIError(
            status_code=500,
            message=(
                "Session could not be "
                "reloaded after update."
            ),
        )

    return stored_session