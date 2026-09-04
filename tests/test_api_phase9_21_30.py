from datetime import (
    datetime,
    timezone,
)
from unittest.mock import MagicMock
from uuid import uuid4

from fastapi.testclient import TestClient

from app.api.main import app
from app.session import RouletteSession


client = TestClient(app)


def active_session(
    session_id,
):
    session = RouletteSession()

    session.session_id = str(
        session_id
    )

    session.start([
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
    ])

    return session


def test_new_spin_triggers_evaluation(
    monkeypatch,
):
    session_id = uuid4()
    spin_id = uuid4()

    session = active_session(
        session_id
    )

    monkeypatch.setattr(
        "app.api.routers.sessions."
        "SessionStorageService.load_session",
        MagicMock(
            return_value=session
        ),
    )

    monkeypatch.setattr(
        "app.api.routers.sessions."
        "SpinRepository.create_spin",
        MagicMock(
            return_value={
                "spin_id": spin_id,
                "session_id":
                    session_id,
                "spin_index": 11,
                "number": 17,
                "spin_type":
                    "OBSERVED",
                "spun_at": None,
                "created_at":
                    datetime.now(
                        timezone.utc
                    ),
            }
        ),
    )

    monkeypatch.setattr(
        "app.api.routers.sessions."
        "SessionRepository.update_session",
        MagicMock(),
    )

    evaluate = MagicMock(
        return_value=[]
    )

    monkeypatch.setattr(
        "app.api.routers.sessions."
        "APIEvaluationService."
        "evaluate_pending_for_spin",
        evaluate,
    )

    response = client.post(
        f"/sessions/{session_id}/spins",
        json={
            "number": 17,
        },
    )

    assert response.status_code == 201

    evaluate.assert_called_once_with(
        session_id=str(session_id),
        actual_spin_id=str(spin_id),
        spin_index=11,
        actual_number=17,
    )


def test_evaluation_endpoint(
    monkeypatch,
):
    session_id = uuid4()

    session = active_session(
        session_id
    )

    monkeypatch.setattr(
        "app.api.routers.sessions."
        "SessionStorageService.load_session",
        MagicMock(
            return_value=session
        ),
    )

    monkeypatch.setattr(
        "app.api.routers.sessions."
        "APIReportingService."
        "get_session_evaluations",
        MagicMock(
            return_value={
                "session_id":
                    str(session_id),
                "evaluation_count":
                    0,
                "evaluations":
                    [],
            }
        ),
    )

    response = client.get(
        (
            f"/sessions/{session_id}"
            "/evaluation"
        )
    )

    assert response.status_code == 200
    assert response.json()[
        "evaluation_count"
    ] == 0


def test_comparison_endpoint(
    monkeypatch,
):
    session_id = uuid4()

    session = active_session(
        session_id
    )

    monkeypatch.setattr(
        "app.api.routers.sessions."
        "SessionStorageService.load_session",
        MagicMock(
            return_value=session
        ),
    )

    monkeypatch.setattr(
        "app.api.routers.sessions."
        "APIReportingService."
        "get_strategy_comparison",
        MagicMock(
            return_value={
                "session_id":
                    str(session_id),
                "strategy_count":
                    0,
                "strategies":
                    {},
            }
        ),
    )

    response = client.get(
        (
            f"/sessions/{session_id}"
            "/comparison"
        )
    )

    assert response.status_code == 200


def test_end_session(monkeypatch):
    session_id = uuid4()

    session = active_session(
        session_id
    )

    now = datetime.now(
        timezone.utc
    )

    monkeypatch.setattr(
        "app.api.routers.sessions."
        "SessionStorageService.load_session",
        MagicMock(
            return_value=session
        ),
    )

    monkeypatch.setattr(
        "app.api.routers.sessions."
        "SessionRepository.update_session",
        MagicMock(),
    )

    monkeypatch.setattr(
        "app.api.routers.sessions."
        "SessionRepository.get_session",
        MagicMock(
            return_value={
                "session_id":
                    session_id,
                "status":
                    "ENDED",
                "initial_spin_count":
                    10,
                "started_at":
                    now,
                "ended_at":
                    now,
                "created_at":
                    now,
                "updated_at":
                    now,
            }
        ),
    )

    response = client.post(
        f"/sessions/{session_id}/end"
    )

    assert response.status_code == 200
    assert response.json()[
        "status"
    ] == "ENDED"


def test_historical_sessions(
    monkeypatch,
):
    monkeypatch.setattr(
        "app.api.routers.sessions."
        "SessionRepository.get_all_sessions",
        MagicMock(
            return_value=[]
        ),
    )

    response = client.get(
        "/sessions"
    )

    assert response.status_code == 200
    assert response.json() == []


def test_models_endpoint(
    monkeypatch,
):
    monkeypatch.setattr(
        "app.api.routers.models."
        "APIReportingService.get_models",
        MagicMock(
            return_value={
                "model_version_count":
                    0,
                "models":
                    [],
            }
        ),
    )

    response = client.get(
        "/models"
    )

    assert response.status_code == 200
    assert response.json()[
        "model_version_count"
    ] == 0


def test_extra_request_field_rejected():
    session_id = uuid4()

    response = client.post(
        f"/sessions/{session_id}/spins",
        json={
            "number": 17,
            "unexpected": True,
        },
    )

    assert response.status_code == 422


def test_cors_localhost():
    response = client.options(
        "/health",
        headers={
            "Origin":
                "http://localhost:5173",
            "Access-Control-Request-Method":
                "GET",
        },
    )

    assert response.status_code == 200

    assert (
        response.headers[
            "access-control-allow-origin"
        ]
        == "http://localhost:5173"
    )