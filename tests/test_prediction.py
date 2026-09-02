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