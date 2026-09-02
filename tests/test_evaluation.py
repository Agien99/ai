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

def test_evaluate_dozens_hit():
    engine = PredictionEvaluationEngine()

    predicted_dozens = [
        {
            "dozen": 1,
            "prediction_score": 1.0,
        },
        {
            "dozen": 3,
            "prediction_score": 0.8,
        },
    ]

    result = engine.evaluate_dozens(
        predicted_dozens,
        actual_number=7,
    )

    assert result is True

def test_evaluate_dozens_miss():
    engine = PredictionEvaluationEngine()

    predicted_dozens = [
        {
            "dozen": 1,
            "prediction_score": 1.0,
        },
        {
            "dozen": 3,
            "prediction_score": 0.8,
        },
    ]

    result = engine.evaluate_dozens(
        predicted_dozens,
        actual_number=18,
    )

    assert result is False

def test_evaluate_dozens_third_dozen_hit():
    engine = PredictionEvaluationEngine()

    predicted_dozens = [
        {
            "dozen": 2,
            "prediction_score": 1.0,
        },
        {
            "dozen": 3,
            "prediction_score": 0.9,
        },
    ]

    result = engine.evaluate_dozens(
        predicted_dozens,
        actual_number=31,
    )

    assert result is True

def test_evaluate_dozens_zero_is_miss():
    engine = PredictionEvaluationEngine()

    predicted_dozens = [
        {
            "dozen": 1,
            "prediction_score": 1.0,
        },
        {
            "dozen": 2,
            "prediction_score": 0.8,
        },
    ]

    result = engine.evaluate_dozens(
        predicted_dozens,
        actual_number=0,
    )

    assert result is False

def evaluate_dozens_for_record(
    self,
    record: PredictionEvaluationRecord,
    predicted_dozens: list[dict],
) -> PredictionEvaluationRecord:
    """
    Update an evaluation record with
    the dozen HIT / MISS result.
    """
    record.dozen_hit = self.evaluate_dozens(
        predicted_dozens,
        record.actual_number,
    )

    return record

def test_evaluate_dozens_updates_record():
    engine = PredictionEvaluationEngine()

    record = engine.create_evaluation_record(
        actual_number=9
    )

    predicted_dozens = [
        {
            "dozen": 1,
            "prediction_score": 1.0,
        },
        {
            "dozen": 2,
            "prediction_score": 0.8,
        },
    ]

    updated_record = (
        engine.evaluate_dozens_for_record(
            record,
            predicted_dozens,
        )
    )

    assert updated_record.dozen_hit is True

def test_evaluate_columns_hit():
    engine = PredictionEvaluationEngine()

    predicted_columns = [
        {
            "column": 1,
            "prediction_score": 1.0,
        },
        {
            "column": 3,
            "prediction_score": 0.8,
        },
    ]

    result = engine.evaluate_columns(
        predicted_columns,
        actual_number=7,
    )

    assert result is True

def test_evaluate_columns_miss():
    engine = PredictionEvaluationEngine()

    predicted_columns = [
        {
            "column": 1,
            "prediction_score": 1.0,
        },
        {
            "column": 3,
            "prediction_score": 0.8,
        },
    ]

    result = engine.evaluate_columns(
        predicted_columns,
        actual_number=8,
    )

    assert result is False

def test_evaluate_columns_third_column_hit():
    engine = PredictionEvaluationEngine()

    predicted_columns = [
        {
            "column": 2,
            "prediction_score": 1.0,
        },
        {
            "column": 3,
            "prediction_score": 0.9,
        },
    ]

    result = engine.evaluate_columns(
        predicted_columns,
        actual_number=36,
    )

    assert result is True

def test_evaluate_columns_zero_is_miss():
    engine = PredictionEvaluationEngine()

    predicted_columns = [
        {
            "column": 1,
            "prediction_score": 1.0,
        },
        {
            "column": 2,
            "prediction_score": 0.8,
        },
    ]

    result = engine.evaluate_columns(
        predicted_columns,
        actual_number=0,
    )

    assert result is False

def test_evaluate_columns_updates_record():
    engine = PredictionEvaluationEngine()

    record = engine.create_evaluation_record(
        actual_number=11
    )

    predicted_columns = [
        {
            "column": 1,
            "prediction_score": 1.0,
        },
        {
            "column": 2,
            "prediction_score": 0.8,
        },
    ]

    updated_record = (
        engine.evaluate_columns_for_record(
            record,
            predicted_columns,
        )
    )

    assert updated_record.column_hit is True