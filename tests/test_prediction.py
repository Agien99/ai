from app.prediction import PredictionEngine


def test_prediction_engine_creation():
    spins = [
        12, 7, 31, 4, 18,
        22, 7, 14, 0, 27,
    ]

    engine = PredictionEngine(spins)

    assert engine.statistics.spins == spins
    assert len(engine.statistics.spins) == 10

def test_prediction_engine_statistics_summary():
    spins = [
        12, 7, 31, 4, 18,
        22, 7, 14, 0, 27,
        7, 12,
    ]

    engine = PredictionEngine(spins)

    summary = engine.get_statistics_summary()

    assert summary["spin_count"] == 12
    assert summary["number_frequency"][7] == 3
    assert summary["number_frequency"][12] == 2

    assert "dozen_frequency" in summary
    assert "column_frequency" in summary
    assert "street_activity" in summary
    assert "split_activity" in summary
    assert "corner_activity" in summary

def test_frequency_score():
    engine = PredictionEngine([1, 2, 3, 4])

    score = engine.calculate_frequency_score(
        total_hits=2,
        total_spins=4,
    )

    assert score == 0.5

def test_recency_score():
    engine = PredictionEngine([1, 2, 3, 4, 5])

    score = engine.calculate_recency_score(
        recent_hits=2,
        recent_window_size=5,
    )

    assert score == 0.4

def test_activity_score():
    engine = PredictionEngine([1, 2, 3, 4, 5])

    score = engine.calculate_activity_score(
        activity_count=3,
        total_spins=5,
    )

    assert score == 0.6

def test_prediction_score():
    engine = PredictionEngine([1, 2, 3])

    score = engine.calculate_prediction_score(
        frequency_score=0.4,
        recency_score=0.6,
        activity_score=0.5,
    )

    assert score == 1.5

def test_scoring_with_zero_denominator():
    engine = PredictionEngine([])

    assert engine.calculate_frequency_score(0, 0) == 0.0
    assert engine.calculate_recency_score(0, 0) == 0.0
    assert engine.calculate_activity_score(0, 0) == 0.0