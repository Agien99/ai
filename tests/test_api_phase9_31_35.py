import logging
from datetime import (
    datetime,
    timezone,
)
from unittest.mock import MagicMock
from uuid import uuid4

from fastapi.testclient import (
    TestClient,
)

from app.api.config import (
    APISettings,
)
from app.api.logging import (
    LOGGER_NAME,
)
from app.api.main import app
from app.session import RouletteSession


client = TestClient(app)


INITIAL_SPINS = [
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


def session_record(
    session,
):
    now = datetime.now(
        timezone.utc
    )

    return {
        "session_id":
            session.session_id,
        "status":
            session.status,
        "initial_spin_count":
            len(
                session.initial_spins
            ),
        "started_at":
            session.started_at
            or now,
        "ended_at":
            session.ended_at,
        "created_at":
            now,
        "updated_at":
            now,
    }


def test_api_request_logging(
    caplog,
):
    with caplog.at_level(
        logging.INFO,
        logger=LOGGER_NAME,
    ):
        response = client.get(
            "/health"
        )

    assert response.status_code == 200

    assert any(
        (
            "request_complete"
            in record.message
            and "GET"
            in record.message
            and "/health"
            in record.message
            and "status=200"
            in record.message
        )
        for record in caplog.records
    )


def test_production_configuration(
    monkeypatch,
):
    monkeypatch.setenv(
        "API_ENV",
        "production",
    )

    monkeypatch.setenv(
        "LOG_LEVEL",
        "WARNING",
    )

    monkeypatch.setenv(
        "API_DOCS_ENABLED",
        "false",
    )

    monkeypatch.setenv(
        "CORS_ORIGINS",
        "https://agien99.github.io",
    )

    production = APISettings()

    assert (
        production.api_environment
        == "production"
    )

    assert (
        production.log_level
        == "WARNING"
    )

    assert (
        production.docs_enabled
        is False
    )

    assert production.cors_origins == [
        "https://agien99.github.io"
    ]


def test_complete_session_api_flow(
    monkeypatch,
):
    session_id = uuid4()
    prediction_run_id = uuid4()
    observed_spin_id = uuid4()

    session = RouletteSession()

    session.session_id = str(
        session_id
    )

    def create_session(
        created_session,
    ):
        created_session.session_id = str(
            session_id
        )

        return session_record(
            created_session
        )

    def load_session(
        requested_session_id,
    ):
        assert requested_session_id == str(
            session_id
        )

        return session

    def get_session(
        requested_session_id,
    ):
        assert requested_session_id == str(
            session_id
        )

        return session_record(
            session
        )

    spin_counter = {
        "value": 0,
    }

    def create_spin(
        session_id,
        spin_index,
        number,
        spin_type,
        spun_at=None,
    ):
        spin_counter[
            "value"
        ] += 1

        return {
            "spin_id":
                (
                    observed_spin_id
                    if spin_type
                    == "OBSERVED"
                    else uuid4()
                ),
            "session_id":
                session_id,
            "spin_index":
                spin_index,
            "number":
                number,
            "spin_type":
                spin_type,
            "spun_at":
                spun_at,
            "created_at":
                datetime.now(
                    timezone.utc
                ),
        }

    monkeypatch.setattr(
        "app.api.routers.sessions."
        "SessionRepository.create_session",
        create_session,
    )

    monkeypatch.setattr(
        "app.api.routers.sessions."
        "SessionStorageService.load_session",
        load_session,
    )

    monkeypatch.setattr(
        "app.api.routers.sessions."
        "SessionRepository.update_session",
        MagicMock(),
    )

    monkeypatch.setattr(
        "app.api.routers.sessions."
        "SessionRepository.get_session",
        get_session,
    )

    monkeypatch.setattr(
        "app.api.routers.sessions."
        "SpinRepository.create_spin",
        create_spin,
    )

    prediction = {
        "prediction_run_id":
            prediction_run_id,
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

    generate_prediction = MagicMock(
        return_value=prediction
    )

    evaluate_prediction = MagicMock(
        return_value=[]
    )

    monkeypatch.setattr(
        "app.api.routers.sessions."
        "APIPredictionService.generate",
        generate_prediction,
    )

    monkeypatch.setattr(
        "app.api.routers.sessions."
        "APIEvaluationService."
        "evaluate_pending_for_spin",
        evaluate_prediction,
    )

    # 1. Create session
    response = client.post(
        "/sessions"
    )

    assert response.status_code == 201
    assert response.json()[
        "status"
    ] == "NEW"

    # 2. Add initial spins
    response = client.post(
        (
            f"/sessions/{session_id}"
            "/initial-spins"
        ),
        json={
            "spins": INITIAL_SPINS,
        },
    )

    assert response.status_code == 200

    assert response.json()[
        "status"
    ] == "ACTIVE"

    assert response.json()[
        "initial_spin_count"
    ] == 10

    # 3. Generate prediction
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
        "prediction_for_spin_index"
    ] == 11

    # 4. Add actual observed spin
    response = client.post(
        (
            f"/sessions/{session_id}"
            "/spins"
        ),
        json={
            "number": 23,
        },
    )

    assert response.status_code == 201

    assert response.json()[
        "number"
    ] == 23

    assert response.json()[
        "spin_index"
    ] == 11

    # Previous prediction must be evaluated
    evaluate_prediction\
        .assert_called_once_with(
            session_id=str(
                session_id
            ),
            actual_spin_id=str(
                observed_spin_id
            ),
            spin_index=11,
            actual_number=23,
        )

    # 5. Statistics now include spin 11
    response = client.get(
        f"/sessions/{session_id}/stats"
    )

    assert response.status_code == 200

    assert response.json()[
        "spin_count"
    ] == 11

    # 6. End session
    response = client.post(
        (
            f"/sessions/{session_id}"
            "/end"
        )
    )

    assert response.status_code == 200

    assert response.json()[
        "status"
    ] == "ENDED"

    assert session.status == "ENDED"

    # 10 initial + 1 observed
    assert spin_counter[
        "value"
    ] == 11


def test_phase9_final_smoke_test():
    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data[
        "status"
    ] == "ok"

    assert data[
        "service"
    ] == "Roulette AI API"

    assert "version" in data