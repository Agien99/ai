from unittest.mock import MagicMock

from app.model_metric_repository import (
    ModelMetricRepository,
)
from app.model_version_repository import (
    ModelVersionRepository,
)
from app.prediction_item_repository import (
    PredictionItemRepository,
)
from app.prediction_run_repository import (
    PredictionRunRepository,
)
from app.spin_repository import SpinRepository


def test_create_spin(monkeypatch):
    expected = {
        "spin_id": "spin-1",
        "session_id": "session-1",
        "spin_index": 1,
        "number": 17,
        "spin_type": "INITIAL",
    }

    mocked = MagicMock(
        return_value=expected
    )

    monkeypatch.setattr(
        "app.spin_repository."
        "DatabaseService.execute_returning_one",
        mocked,
    )

    result = SpinRepository.create_spin(
        session_id="session-1",
        spin_index=1,
        number=17,
        spin_type="INITIAL",
    )

    assert result == expected
    mocked.assert_called_once()


def test_get_session_spins(monkeypatch):
    expected = [
        {
            "spin_index": 1,
            "number": 17,
        },
        {
            "spin_index": 2,
            "number": 7,
        },
    ]

    mocked = MagicMock(
        return_value=expected
    )

    monkeypatch.setattr(
        "app.spin_repository."
        "DatabaseService.fetch_all",
        mocked,
    )

    result = SpinRepository.get_session_spins(
        "session-1"
    )

    assert result == expected


def test_create_prediction_run(monkeypatch):
    expected = {
        "prediction_run_id": "run-1",
        "session_id": "session-1",
        "strategy_key": "v1",
    }

    mocked = MagicMock(
        return_value=expected
    )

    monkeypatch.setattr(
        "app.prediction_run_repository."
        "DatabaseService.execute_returning_one",
        mocked,
    )

    result = (
        PredictionRunRepository
        .create_prediction_run(
            session_id="session-1",
            strategy_key="v1",
            prediction_for_spin_index=11,
            input_spin_count=10,
            recent_window=10,
        )
    )

    assert result == expected
    mocked.assert_called_once()


def test_evaluate_prediction_run(monkeypatch):
    expected = {
        "prediction_run_id": "run-1",
        "actual_spin_id": "spin-11",
    }

    mocked = MagicMock(
        return_value=expected
    )

    monkeypatch.setattr(
        "app.prediction_run_repository."
        "DatabaseService.execute_returning_one",
        mocked,
    )

    result = (
        PredictionRunRepository
        .evaluate_prediction_run(
            "run-1",
            "spin-11",
        )
    )

    assert result == expected


def test_create_prediction_item(monkeypatch):
    expected = {
        "prediction_item_id": "item-1",
        "category": "DOZENS",
    }

    mocked = MagicMock(
        return_value=expected
    )

    monkeypatch.setattr(
        "app.prediction_item_repository."
        "DatabaseService.execute_returning_one",
        mocked,
    )

    result = (
        PredictionItemRepository
        .create_prediction_item(
            prediction_run_id="run-1",
            category="DOZENS",
            payload=[
                {
                    "rank": 1,
                    "dozen": 2,
                    "score": 0.42,
                }
            ],
        )
    )

    assert result == expected
    mocked.assert_called_once()


def test_update_prediction_item_evaluation(
    monkeypatch,
):
    expected = {
        "prediction_item_id": "item-1",
        "is_hit": True,
    }

    mocked = MagicMock(
        return_value=expected
    )

    monkeypatch.setattr(
        "app.prediction_item_repository."
        "DatabaseService.execute_returning_one",
        mocked,
    )

    result = (
        PredictionItemRepository
        .update_evaluation(
            "item-1",
            True,
        )
    )

    assert result == expected


def test_create_model_version(monkeypatch):
    expected = {
        "model_version_id": "model-1",
        "model_name": "random_forest",
        "version_number": 1,
    }

    mocked = MagicMock(
        return_value=expected
    )

    monkeypatch.setattr(
        "app.model_version_repository."
        "DatabaseService.execute_returning_one",
        mocked,
    )

    result = (
        ModelVersionRepository
        .create_model_version(
            model_name="random_forest",
            version_number=1,
            feature_version="v1",
            training_row_count=100,
            training_session_count=5,
            training_parameters={
                "n_estimators": 100,
            },
            is_active=True,
        )
    )

    assert result == expected
    mocked.assert_called_once()


def test_get_active_model_version(monkeypatch):
    expected = {
        "model_version_id": "model-1",
        "model_name": "random_forest",
        "is_active": True,
    }

    mocked = MagicMock(
        return_value=expected
    )

    monkeypatch.setattr(
        "app.model_version_repository."
        "DatabaseService.fetch_one",
        mocked,
    )

    result = (
        ModelVersionRepository
        .get_active_model_version(
            "random_forest"
        )
    )

    assert result == expected


def test_create_model_metric(monkeypatch):
    expected = {
        "model_metric_id": "metric-1",
        "model_version_id": "model-1",
        "metric_name": "top_1_accuracy",
        "metric_value": 0.04,
    }

    mocked = MagicMock(
        return_value=expected
    )

    monkeypatch.setattr(
        "app.model_metric_repository."
        "DatabaseService.execute_returning_one",
        mocked,
    )

    result = (
        ModelMetricRepository
        .create_model_metric(
            model_version_id="model-1",
            metric_scope="NUMBER",
            metric_name="top_1_accuracy",
            metric_value=0.04,
            sample_count=100,
            evaluation_type="BENCHMARK",
        )
    )

    assert result == expected
    mocked.assert_called_once()


def test_get_model_metrics(monkeypatch):
    expected = [
        {
            "metric_name": "top_1_accuracy",
            "metric_value": 0.04,
        },
        {
            "metric_name": "top_3_accuracy",
            "metric_value": 0.10,
        },
    ]

    mocked = MagicMock(
        return_value=expected
    )

    monkeypatch.setattr(
        "app.model_metric_repository."
        "DatabaseService.fetch_all",
        mocked,
    )

    result = (
        ModelMetricRepository
        .get_model_metrics(
            "model-1"
        )
    )

    assert result == expected