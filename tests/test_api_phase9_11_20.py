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


def test_add_spin(monkeypatch):
    session_id = uuid4()
    spin_id = uuid4()
    now = datetime.now(
        timezone.utc
    )

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

    create_spin = MagicMock(
        return_value={
            "spin_id": spin_id,
            "session_id": session_id,
            "spin_index": 11,
            "number": 17,
            "spin_type": "OBSERVED",
            "spun_at": None,
            "created_at": now,
        }
    )

    monkeypatch.setattr(
        "app.api.routers.sessions."
        "SpinRepository.create_spin",
        create_spin,
    )

    monkeypatch.setattr(
        "app.api.routers.sessions."
        "SessionRepository.update_session",
        MagicMock(),
    )

    response = client.post(
        f"/sessions/{session_id}/spins",
        json={
            "number": 17,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["number"] == 17
    assert data["spin_index"] == 11

    create_spin.assert_called_once()


def test_add_spin_rejects_invalid_number():
    session_id = uuid4()

    response = client.post(
        f"/sessions/{session_id}/spins",
        json={
            "number": 99,
        },
    )

    assert response.status_code == 422


def test_get_session_spins(monkeypatch):
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
        "SpinRepository.get_session_spins",
        MagicMock(
            return_value=[
                {
                    "spin_id": spin_id,
                    "session_id":
                        session_id,
                    "spin_index": 1,
                    "number": 17,
                    "spin_type":
                        "INITIAL",
                    "spun_at": None,
                    "created_at": None,
                }
            ]
        ),
    )

    response = client.get(
        f"/sessions/{session_id}/spins"
    )

    assert response.status_code == 200

    assert response.json()[0][
        "number"
    ] == 17


def test_get_statistics(monkeypatch):
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

    response = client.get(
        f"/sessions/{session_id}/stats"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["spin_count"] == 10

    assert (
        data["statistics"][
            "spin_count"
        ]
        == 10
    )


def test_generate_v1_prediction(
    monkeypatch,
):
    session_id = uuid4()
    run_id = uuid4()

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

    prediction_result = {
        "prediction_run_id":
            run_id,
        "session_id":
            session_id,
        "strategy":
            "v1",
        "prediction_for_spin_index":
            11,
        "input_spin_count":
            10,
        "recent_window":
            10,
        "model_version_id":
            None,
        "predictions": {
            "dozens": [],
            "columns": [],
            "streets": [],
            "splits": [],
            "corners": [],
        },
        "number_probabilities":
            None,
    }

    generate = MagicMock(
        return_value=prediction_result
    )

    monkeypatch.setattr(
        "app.api.routers.sessions."
        "APIPredictionService.generate",
        generate,
    )

    response = client.post(
        (
            f"/sessions/{session_id}"
            "/predictions"
        ),
        json={
            "strategy": "v1",
            "recent_window": 10,
        },
    )

    assert response.status_code == 201

    assert response.json()[
        "strategy"
    ] == "v1"


def test_invalid_prediction_strategy():
    session_id = uuid4()

    response = client.post(
        (
            f"/sessions/{session_id}"
            "/predictions"
        ),
        json={
            "strategy":
                "something_invalid",
        },
    )

    assert response.status_code == 422


def test_get_latest_prediction(
    monkeypatch,
):
    session_id = uuid4()
    run_id = uuid4()

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
        "APIPredictionService.get_latest",
        MagicMock(
            return_value={
                "prediction_run": {
                    "prediction_run_id":
                        run_id,
                    "session_id":
                        session_id,
                    "strategy_key":
                        "v1",
                },
                "prediction_items": [],
            }
        ),
    )

    response = client.get(
        (
            f"/sessions/{session_id}"
            "/predictions/latest"
        )
    )

    assert response.status_code == 200

    assert (
        response.json()[
            "prediction_run"
        ]["strategy_key"]
        == "v1"
    )