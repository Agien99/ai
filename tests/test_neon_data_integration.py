from datetime import datetime
from unittest.mock import MagicMock

from app.evaluation import (
    PredictionEvaluationRecord,
)
from app.evaluation_storage_service import (
    EvaluationStorageService,
)
from app.ml.neon_training import (
    NeonRetrainingService,
    NeonTrainingDataService,
)
from app.session_storage_service import (
    SessionStorageService,
)


def test_reconstruct_session(monkeypatch):
    session_row = {
        "session_id": "session-1",
        "status": "ACTIVE",
        "initial_spin_count": 10,
        "started_at": datetime.now(),
        "ended_at": None,
    }

    spin_rows = [
        {
            "spin_index": index,
            "number": number,
        }
        for index, number in enumerate(
            range(1, 13),
            start=1,
        )
    ]

    monkeypatch.setattr(
        "app.session_storage_service."
        "SessionRepository.get_session",
        MagicMock(
            return_value=session_row
        ),
    )

    monkeypatch.setattr(
        "app.session_storage_service."
        "SpinRepository.get_session_spins",
        MagicMock(
            return_value=spin_rows
        ),
    )

    session = (
        SessionStorageService.load_session(
            "session-1"
        )
    )

    assert session is not None
    assert session.session_id == "session-1"
    assert session.status == "ACTIVE"

    assert session.initial_spins == list(
        range(1, 11)
    )

    assert session.spins == list(
        range(1, 13)
    )


def test_load_missing_session(monkeypatch):
    monkeypatch.setattr(
        "app.session_storage_service."
        "SessionRepository.get_session",
        MagicMock(
            return_value=None
        ),
    )

    result = (
        SessionStorageService.load_session(
            "missing"
        )
    )

    assert result is None


def test_save_evaluation(monkeypatch):
    update_run = MagicMock()

    get_items = MagicMock(
        return_value=[
            {
                "prediction_item_id": "d1",
                "category": "DOZENS",
            },
            {
                "prediction_item_id": "c1",
                "category": "COLUMNS",
            },
            {
                "prediction_item_id": "s1",
                "category": "STREETS",
            },
            {
                "prediction_item_id": "sp1",
                "category": "SPLITS",
            },
            {
                "prediction_item_id": "co1",
                "category": "CORNERS",
            },
            {
                "prediction_item_id": "np1",
                "category":
                    "NUMBER_PROBABILITIES",
            },
        ]
    )

    update_item = MagicMock()

    monkeypatch.setattr(
        "app.evaluation_storage_service."
        "PredictionRunRepository."
        "evaluate_prediction_run",
        update_run,
    )

    monkeypatch.setattr(
        "app.evaluation_storage_service."
        "PredictionItemRepository."
        "get_prediction_items",
        get_items,
    )

    monkeypatch.setattr(
        "app.evaluation_storage_service."
        "PredictionItemRepository."
        "update_evaluation",
        update_item,
    )

    evaluation = (
        PredictionEvaluationRecord(
            actual_number=17,
            evaluated_at=datetime.now(),
            dozen_hit=True,
            column_hit=False,
            street_hit=True,
            split_hit=True,
            corner_hit=False,
        )
    )

    EvaluationStorageService.save_evaluation(
        prediction_run_id="run-1",
        actual_spin_id="spin-11",
        evaluation=evaluation,
    )

    update_run.assert_called_once_with(
        "run-1",
        "spin-11",
    )

    assert update_item.call_count == 5

    update_item.assert_any_call(
        "d1",
        True,
    )

    update_item.assert_any_call(
        "c1",
        False,
    )

    update_item.assert_any_call(
        "s1",
        True,
    )

    update_item.assert_any_call(
        "sp1",
        True,
    )

    update_item.assert_any_call(
        "co1",
        False,
    )


def test_load_training_sequences(
    monkeypatch,
):
    sessions = [
        {
            "session_id": "session-1",
        },
        {
            "session_id": "session-2",
        },
    ]

    monkeypatch.setattr(
        "app.ml.neon_training."
        "SessionRepository.get_all_sessions",
        MagicMock(
            return_value=sessions
        ),
    )

    def fake_spins(session_id):
        if session_id == "session-1":
            numbers = list(
                range(1, 13)
            )
        else:
            numbers = list(
                range(13, 25)
            )

        return [
            {
                "spin_index": index,
                "number": number,
            }
            for index, number in enumerate(
                numbers,
                start=1,
            )
        ]

    monkeypatch.setattr(
        "app.ml.neon_training."
        "SpinRepository.get_session_spins",
        fake_spins,
    )

    service = NeonTrainingDataService(
        minimum_history=10,
    )

    sequences = (
        service.load_training_sequences()
    )

    assert len(sequences) == 2
    assert sequences[0] == list(
        range(1, 13)
    )
    assert sequences[1] == list(
        range(13, 25)
    )


def test_training_dataset_keeps_sessions_separate(
    monkeypatch,
):
    service = NeonTrainingDataService(
        minimum_history=10,
    )

    monkeypatch.setattr(
        service,
        "load_training_sequences",
        MagicMock(
            return_value=[
                list(range(1, 13)),
                list(range(13, 25)),
            ]
        ),
    )

    dataset = (
        service.build_training_dataset()
    )

    # Each 12-spin session generates:
    #
    # history 10 → target 11
    # history 11 → target 12
    #
    # 2 rows per session × 2 sessions = 4.
    assert len(dataset.X) == 4
    assert len(dataset.y) == 4


def test_retrain_model_from_neon(
    monkeypatch,
):
    service = NeonRetrainingService(
        minimum_history=10,
    )

    dataset = MagicMock()

    dataset.X = [
        [0.0, 1.0],
        [1.0, 0.0],
    ]

    dataset.y = [
        17,
        20,
    ]

    monkeypatch.setattr(
        service.training_data,
        "build_training_dataset",
        MagicMock(
            return_value=dataset
        ),
    )

    model = MagicMock()

    result = service.retrain_model(
        model
    )

    model.fit.assert_called_once_with(
        dataset.X,
        dataset.y,
    )

    assert result is model


def test_retrain_requires_data(
    monkeypatch,
):
    service = NeonRetrainingService()

    dataset = MagicMock()
    dataset.X = []
    dataset.y = []

    monkeypatch.setattr(
        service.training_data,
        "build_training_dataset",
        MagicMock(
            return_value=dataset
        ),
    )

    model = MagicMock()

    try:
        service.train_model(model)
        assert False
    except ValueError as error:
        assert (
            "Not enough historical Neon data"
            in str(error)
        )