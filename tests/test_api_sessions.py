from datetime import datetime, timezone
from uuid import uuid4
from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from app.api.main import app
from app.session import RouletteSession


client = TestClient(app)


def test_health_endpoint():
    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert data["service"] == (
        "Roulette AI API"
    )


def test_create_session(monkeypatch):
    session_id = uuid4()
    now = datetime.now(timezone.utc)

    expected = {
        "session_id": session_id,
        "status": "NEW",
        "initial_spin_count": 0,
        "started_at": now,
        "ended_at": None,
        "created_at": now,
        "updated_at": now,
    }

    mocked = MagicMock(
        return_value=expected
    )

    monkeypatch.setattr(
        "app.api.routers.sessions."
        "SessionRepository.create_session",
        mocked,
    )

    response = client.post(
        "/sessions"
    )

    assert response.status_code == 201

    data = response.json()

    assert data["session_id"] == str(
        session_id
    )

    assert data["status"] == "NEW"
    assert data["initial_spin_count"] == 0

    mocked.assert_called_once()


def test_get_session(monkeypatch):
    session_id = uuid4()
    now = datetime.now(timezone.utc)

    expected = {
        "session_id": session_id,
        "status": "ACTIVE",
        "initial_spin_count": 10,
        "started_at": now,
        "ended_at": None,
        "created_at": now,
        "updated_at": now,
    }

    mocked = MagicMock(
        return_value=expected
    )

    monkeypatch.setattr(
        "app.api.routers.sessions."
        "SessionRepository.get_session",
        mocked,
    )

    response = client.get(
        f"/sessions/{session_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["session_id"] == str(
        session_id
    )

    assert data["status"] == "ACTIVE"


def test_get_missing_session(monkeypatch):
    session_id = uuid4()

    monkeypatch.setattr(
        "app.api.routers.sessions."
        "SessionRepository.get_session",
        MagicMock(
            return_value=None
        ),
    )

    response = client.get(
        f"/sessions/{session_id}"
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Session not found."
    }


def test_add_initial_spins(monkeypatch):
    session_id = uuid4()

    session = RouletteSession()

    session.session_id = str(
        session_id
    )

    load_session = MagicMock(
        return_value=session
    )

    update_session = MagicMock()
    create_spin = MagicMock()

    now = datetime.now(timezone.utc)

    stored_session = {
        "session_id": session_id,
        "status": "ACTIVE",
        "initial_spin_count": 10,
        "started_at": now,
        "ended_at": None,
        "created_at": now,
        "updated_at": now,
    }

    get_session = MagicMock(
        return_value=stored_session
    )

    monkeypatch.setattr(
        "app.api.routers.sessions."
        "SessionStorageService.load_session",
        load_session,
    )

    monkeypatch.setattr(
        "app.api.routers.sessions."
        "SessionRepository.update_session",
        update_session,
    )

    monkeypatch.setattr(
        "app.api.routers.sessions."
        "SpinRepository.create_spin",
        create_spin,
    )

    monkeypatch.setattr(
        "app.api.routers.sessions."
        "SessionRepository.get_session",
        get_session,
    )

    spins = [
        17,
        7,
        32,
        14,
        20,
        1,
        9,
        28,
        5,
        31,
    ]

    response = client.post(
        (
            f"/sessions/{session_id}"
            "/initial-spins"
        ),
        json={
            "spins": spins,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ACTIVE"
    assert data["initial_spin_count"] == 10

    update_session.assert_called_once()

    assert create_spin.call_count == 10


def test_initial_spins_reject_less_than_10():
    session_id = uuid4()

    response = client.post(
        (
            f"/sessions/{session_id}"
            "/initial-spins"
        ),
        json={
            "spins": [
                1,
                2,
                3,
            ],
        },
    )

    assert response.status_code == 422


def test_initial_spins_reject_invalid_number():
    session_id = uuid4()

    response = client.post(
        (
            f"/sessions/{session_id}"
            "/initial-spins"
        ),
        json={
            "spins": [
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                99,
            ],
        },
    )

    assert response.status_code == 422