from datetime import datetime
from unittest.mock import MagicMock

from app.session import RouletteSession
from app.session_repository import SessionRepository


def test_create_session(monkeypatch):
    session = RouletteSession()

    expected = {
        "session_id": session.session_id,
        "status": "NEW",
        "initial_spin_count": 0,
    }

    mocked_method = MagicMock(
        return_value=expected
    )

    monkeypatch.setattr(
        "app.session_repository."
        "DatabaseService.execute_returning_one",
        mocked_method,
    )

    result = SessionRepository.create_session(
        session
    )

    assert result == expected

    mocked_method.assert_called_once()


def test_update_session(monkeypatch):
    session = RouletteSession()

    session.start([
        1, 2, 3, 4, 5,
        6, 7, 8, 9, 10,
    ])

    mocked_method = MagicMock()

    monkeypatch.setattr(
        "app.session_repository."
        "DatabaseService.execute",
        mocked_method,
    )

    SessionRepository.update_session(
        session
    )

    mocked_method.assert_called_once()


def test_get_session(monkeypatch):
    session_id = "test-session"

    expected = {
        "session_id": session_id,
        "status": "ACTIVE",
        "initial_spin_count": 10,
        "started_at": datetime.now(),
        "ended_at": None,
    }

    mocked_method = MagicMock(
        return_value=expected
    )

    monkeypatch.setattr(
        "app.session_repository."
        "DatabaseService.fetch_one",
        mocked_method,
    )

    result = SessionRepository.get_session(
        session_id
    )

    assert result == expected

    mocked_method.assert_called_once()


def test_get_all_sessions(monkeypatch):
    expected = [
        {
            "session_id": "session-1",
            "status": "ACTIVE",
        },
        {
            "session_id": "session-2",
            "status": "ENDED",
        },
    ]

    mocked_method = MagicMock(
        return_value=expected
    )

    monkeypatch.setattr(
        "app.session_repository."
        "DatabaseService.fetch_all",
        mocked_method,
    )

    result = SessionRepository.get_all_sessions()

    assert result == expected

    mocked_method.assert_called_once()