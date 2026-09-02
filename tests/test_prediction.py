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

def test_score_dozens():
    spins = [
        1, 2, 5, 7,
        13, 18, 20,
        25, 31, 36,
        1, 2, 3, 4, 5,
    ]

    engine = PredictionEngine(spins)

    results = engine.score_dozens(
        recent_window=5
    )

    assert len(results) == 3

    assert results[0]["dozen"] == 1

    assert results[0]["total_hits"] == 9
    assert results[0]["recent_hits"] == 5

    assert results[1]["dozen"] in [2, 3]
    assert results[2]["dozen"] in [2, 3]

    assert results[0]["prediction_score"] > (
        results[1]["prediction_score"]
    )

def test_dozens_are_ranked_by_score():
    spins = [
        1, 2, 3, 4, 5,
        13, 14, 15,
        25, 26,
    ]

    engine = PredictionEngine(spins)

    results = engine.score_dozens(
        recent_window=5
    )

    assert (
        results[0]["prediction_score"]
        >= results[1]["prediction_score"]
    )

    assert (
        results[1]["prediction_score"]
        >= results[2]["prediction_score"]
    )

def test_score_dozens_empty_history():
    engine = PredictionEngine([])

    results = engine.score_dozens()

    assert len(results) == 3

    for result in results:
        assert result["total_hits"] == 0
        assert result["recent_hits"] == 0
        assert result["frequency_score"] == 0.0
        assert result["recency_score"] == 0.0
        assert result["activity_score"] == 0.0
        assert result["prediction_score"] == 0.0

def test_score_columns():
    spins = [
        1, 4, 7, 10,
        2, 5, 8,
        3, 6, 9,
        1, 4, 7, 10, 13,
    ]

    engine = PredictionEngine(spins)

    results = engine.score_columns(
        recent_window=5
    )

    assert len(results) == 3

    assert results[0]["column"] == 1
    assert results[0]["total_hits"] == 9
    assert results[0]["recent_hits"] == 5

    assert results[0]["prediction_score"] > (
        results[1]["prediction_score"]
    )

def test_columns_are_ranked_by_score():
    spins = [
        1, 4, 7, 10,
        2, 5, 8,
        3, 6,
    ]

    engine = PredictionEngine(spins)

    results = engine.score_columns(
        recent_window=5
    )

    assert (
        results[0]["prediction_score"]
        >= results[1]["prediction_score"]
    )

    assert (
        results[1]["prediction_score"]
        >= results[2]["prediction_score"]
    )

def test_score_columns_empty_history():
    engine = PredictionEngine([])

    results = engine.score_columns()

    assert len(results) == 3

    for result in results:
        assert result["total_hits"] == 0
        assert result["recent_hits"] == 0
        assert result["frequency_score"] == 0.0
        assert result["recency_score"] == 0.0
        assert result["activity_score"] == 0.0
        assert result["prediction_score"] == 0.0

def test_score_streets():
    spins = [
        1, 2, 3,
        4, 5,
        10,
        1, 2, 3, 1, 2,
    ]

    engine = PredictionEngine(spins)

    results = engine.score_streets(
        recent_window=5
    )

    assert len(results) == 12

    assert results[0]["street"] == (1, 2, 3)
    assert results[0]["total_hits"] == 8
    assert results[0]["recent_hits"] == 5

    assert results[0]["prediction_score"] > (
        results[1]["prediction_score"]
    )

def test_streets_are_ranked_by_score():
    spins = [
        1, 2, 3, 1,
        4, 5, 6,
        7, 8,
    ]

    engine = PredictionEngine(spins)

    results = engine.score_streets(
        recent_window=5
    )

    for index in range(len(results) - 1):
        assert (
            results[index]["prediction_score"]
            >= results[index + 1][
                "prediction_score"
            ]
        )

def test_score_streets_empty_history():
    engine = PredictionEngine([])

    results = engine.score_streets()

    assert len(results) == 12

    for result in results:
        assert result["total_hits"] == 0
        assert result["recent_hits"] == 0
        assert result["frequency_score"] == 0.0
        assert result["recency_score"] == 0.0
        assert result["activity_score"] == 0.0
        assert result["prediction_score"] == 0.0

def test_score_splits():
    spins = [
        1,
        2,
        5,
        5,
        8,
        2,
        5,
        2,
        5,
        2,
    ]

    engine = PredictionEngine(spins)

    results = engine.score_splits(
        recent_window=5
    )

    assert len(results) == 57

    assert results[0]["split"] == (2, 5)

    assert results[0]["total_hits"] == 8
    assert results[0]["recent_hits"] == 5

def test_splits_are_ranked_by_score():
    spins = [
        1, 2, 5,
        8, 11, 14,
        17, 20,
    ]

    engine = PredictionEngine(spins)

    results = engine.score_splits(
        recent_window=5
    )

    for index in range(len(results) - 1):
        assert (
            results[index]["prediction_score"]
            >= results[index + 1][
                "prediction_score"
            ]
        )

def test_score_splits_empty_history():
    engine = PredictionEngine([])

    results = engine.score_splits()

    assert len(results) == 57

    for result in results:
        assert result["total_hits"] == 0
        assert result["recent_hits"] == 0
        assert result["frequency_score"] == 0.0
        assert result["recency_score"] == 0.0
        assert result["activity_score"] == 0.0
        assert result["prediction_score"] == 0.0

def test_score_corners():
    spins = [
        1,
        2,
        4,
        5,
        8,
        1,
        2,
        4,
        5,
        5,
    ]

    engine = PredictionEngine(spins)

    results = engine.score_corners(
        recent_window=5
    )

    assert len(results) == 22

    assert results[0]["corner"] == (
        1, 2, 4, 5
    )

    assert results[0]["total_hits"] == 9
    assert results[0]["recent_hits"] == 5

def test_corners_are_ranked_by_score():
    spins = [
        1, 2, 4, 5,
        8, 9, 11,
        12, 14,
    ]

    engine = PredictionEngine(spins)

    results = engine.score_corners(
        recent_window=5
    )

    for index in range(len(results) - 1):
        assert (
            results[index]["prediction_score"]
            >= results[index + 1][
                "prediction_score"
            ]
        )
        
def test_score_corners_empty_history():
    engine = PredictionEngine([])

    results = engine.score_corners()

    assert len(results) == 22

    for result in results:
        assert result["total_hits"] == 0
        assert result["recent_hits"] == 0
        assert result["frequency_score"] == 0.0
        assert result["recency_score"] == 0.0
        assert result["activity_score"] == 0.0
        assert result["prediction_score"] == 0.0

def test_rank_predictions():
    engine = PredictionEngine([1, 2, 3])

    predictions = [
        {
            "street": (4, 5, 6),
            "prediction_score": 0.5,
        },
        {
            "street": (1, 2, 3),
            "prediction_score": 0.9,
        },
        {
            "street": (7, 8, 9),
            "prediction_score": 0.7,
        },
    ]

    ranked = engine.rank_predictions(
        predictions,
        key_name="street",
    )

    assert ranked[0]["street"] == (1, 2, 3)
    assert ranked[1]["street"] == (7, 8, 9)
    assert ranked[2]["street"] == (4, 5, 6)

def test_rank_predictions_with_limit():
    engine = PredictionEngine([1, 2, 3])

    predictions = [
        {
            "dozen": 1,
            "prediction_score": 0.8,
        },
        {
            "dozen": 2,
            "prediction_score": 0.9,
        },
        {
            "dozen": 3,
            "prediction_score": 0.7,
        },
    ]

    ranked = engine.rank_predictions(
        predictions,
        key_name="dozen",
        limit=2,
    )

    assert len(ranked) == 2
    assert ranked[0]["dozen"] == 2
    assert ranked[1]["dozen"] == 1

def test_rank_predictions_tie_breaker():
    engine = PredictionEngine([1, 2, 3])

    predictions = [
        {
            "column": 3,
            "prediction_score": 0.5,
        },
        {
            "column": 1,
            "prediction_score": 0.5,
        },
        {
            "column": 2,
            "prediction_score": 0.5,
        },
    ]

    ranked = engine.rank_predictions(
        predictions,
        key_name="column",
    )

    assert ranked[0]["column"] == 1
    assert ranked[1]["column"] == 2
    assert ranked[2]["column"] == 3