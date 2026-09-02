from datetime import datetime

from app.evaluation import (
    PredictionEvaluationEngine,
    PredictionEvaluationRecord,
)

def test_evaluation_engine_creation():
    engine = PredictionEvaluationEngine()

    assert isinstance(
        engine,
        PredictionEvaluationEngine,
    )


def test_validate_actual_number():
    engine = PredictionEvaluationEngine()

    assert engine.validate_actual_number(0) is True
    assert engine.validate_actual_number(17) is True
    assert engine.validate_actual_number(36) is True


def test_validate_invalid_actual_number():
    engine = PredictionEvaluationEngine()

    try:
        engine.validate_actual_number(37)
        assert False

    except ValueError as error:
        assert str(error) == (
            "Invalid roulette number: 37"
        )

def test_validate_negative_actual_number():
    engine = PredictionEvaluationEngine()

    try:
        engine.validate_actual_number(-1)
        assert False

    except ValueError as error:
        assert str(error) == (
            "Invalid roulette number: -1"
        )

def test_create_evaluation_record():
    engine = PredictionEvaluationEngine()

    record = engine.create_evaluation_record(
        actual_number=17
    )

    assert isinstance(
        record,
        PredictionEvaluationRecord,
    )

    assert record.actual_number == 17

    assert isinstance(
        record.evaluated_at,
        datetime,
    )

def test_evaluation_record_initial_hit_values():
    engine = PredictionEvaluationEngine()

    record = engine.create_evaluation_record(
        actual_number=7
    )

    assert record.dozen_hit is False
    assert record.column_hit is False
    assert record.street_hit is False
    assert record.split_hit is False
    assert record.corner_hit is False

def test_create_evaluation_record_invalid_number():
    engine = PredictionEvaluationEngine()

    try:
        engine.create_evaluation_record(
            actual_number=37
        )
        assert False

    except ValueError as error:
        assert str(error) == (
            "Invalid roulette number: 37"
        )