from app.evaluation import PredictionEvaluationEngine


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