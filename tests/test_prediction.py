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

def test_generate_predictions():
    spins = [
        1, 2, 5, 7, 12,
        13, 18, 22, 25, 31,
        4, 5, 7, 8, 10,
    ]

    engine = PredictionEngine(spins)

    predictions = engine.generate_predictions(
        recent_window=10
    )

    assert len(predictions["dozens"]) == 2
    assert len(predictions["columns"]) == 2
    assert len(predictions["corners"]) == 5
    assert len(predictions["splits"]) == 12
    assert len(predictions["streets"]) == 6

def test_generate_predictions_structure():
    spins = [
        1, 4, 7, 10,
        2, 5, 8,
        3, 6, 9,
        12, 15, 18,
    ]

    engine = PredictionEngine(spins)

    predictions = engine.generate_predictions()

    assert set(predictions.keys()) == {
        "dozens",
        "columns",
        "corners",
        "splits",
        "streets",
    }

    assert "dozen" in predictions["dozens"][0]
    assert "column" in predictions["columns"][0]
    assert "corner" in predictions["corners"][0]
    assert "split" in predictions["splits"][0]
    assert "street" in predictions["streets"][0]

    assert "prediction_score" in predictions["dozens"][0]
    assert "prediction_score" in predictions["columns"][0]
    assert "prediction_score" in predictions["corners"][0]
    assert "prediction_score" in predictions["splits"][0]
    assert "prediction_score" in predictions["streets"][0]

def test_generated_predictions_keep_highest_scores():
    spins = [
        1, 2, 3, 1, 2,
        4, 5,
        7, 8,
        1, 2, 3,
    ]

    engine = PredictionEngine(spins)

    predictions = engine.generate_predictions(
        recent_window=5
    )

    streets = predictions["streets"]

    for index in range(len(streets) - 1):
        assert (
            streets[index]["prediction_score"]
            >= streets[index + 1]["prediction_score"]
        )

def test_prediction_output_structure():
    spins = [
        1, 2, 5, 7, 12,
        13, 18, 22, 25, 31,
        4, 5, 7, 8, 10,
    ]

    engine = PredictionEngine(spins)

    output = engine.build_prediction_output(
        recent_window=10
    )

    assert output["version"] == "v1"
    assert output["recent_window"] == 10
    assert output["spin_count"] == 15

    assert "predictions" in output

    predictions = output["predictions"]

    assert len(predictions["dozens"]) == 2
    assert len(predictions["columns"]) == 2
    assert len(predictions["corners"]) == 5
    assert len(predictions["splits"]) == 12
    assert len(predictions["streets"]) == 6

def test_prediction_output_recent_window():
    spins = [
        1, 2, 3, 4, 5,
        6, 7, 8, 9, 10,
    ]

    engine = PredictionEngine(spins)

    output = engine.build_prediction_output(
        recent_window=5
    )

    assert output["recent_window"] == 5
    assert output["spin_count"] == 10

def test_invalid_recent_window_zero():
    engine = PredictionEngine([
        1, 2, 3,
    ])

    try:
        engine.generate_predictions(
            recent_window=0
        )
        assert False
    except ValueError as error:
        assert str(error) == (
            "Recent window must be greater than zero."
        )

def test_invalid_recent_window_negative():
    engine = PredictionEngine([
        1, 2, 3,
    ])

    try:
        engine.generate_predictions(
            recent_window=-5
        )
        assert False
    except ValueError as error:
        assert str(error) == (
            "Recent window must be greater than zero."
        )

def test_invalid_recent_window_non_integer():
    engine = PredictionEngine([
        1, 2, 3,
    ])

    try:
        engine.generate_predictions(
            recent_window="10"
        )
        assert False
    except ValueError as error:
        assert str(error) == (
            "Recent window must be an integer."
        )

def test_recent_window_larger_than_history():
    spins = [
        1, 2, 3, 4, 5,
    ]

    engine = PredictionEngine(spins)

    predictions = engine.generate_predictions(
        recent_window=20
    )

    assert len(predictions["dozens"]) == 2
    assert len(predictions["columns"]) == 2
    assert len(predictions["corners"]) == 5
    assert len(predictions["splits"]) == 12
    assert len(predictions["streets"]) == 6

def test_prediction_engine_handles_zero():
    spins = [
        0, 1, 0, 7, 12,
        0, 18, 25, 31, 36,
    ]

    engine = PredictionEngine(spins)

    output = engine.build_prediction_output()

    assert output["spin_count"] == 10

    assert len(
        output["predictions"]["dozens"]
    ) == 2

    assert len(
        output["predictions"]["columns"]
    ) == 2

    assert len(
        output["predictions"]["streets"]
    ) == 6

def test_full_prediction_engine():
    spins = [
        12, 7, 31, 4, 18,
        22, 7, 14, 0, 27,
        7, 12, 5, 8, 19,
    ]

    engine = PredictionEngine(spins)

    output = engine.build_prediction_output(
        recent_window=10
    )

    assert output["version"] == "v1"
    assert output["spin_count"] == 15
    assert output["recent_window"] == 10

    predictions = output["predictions"]

    assert len(predictions["dozens"]) == 2
    assert len(predictions["columns"]) == 2
    assert len(predictions["corners"]) == 5
    assert len(predictions["splits"]) == 12
    assert len(predictions["streets"]) == 6

def test_all_predictions_have_scores():
    spins = [
        1, 2, 3, 4, 5,
        6, 7, 8, 9, 10,
        11, 12, 13, 14, 15,
    ]

    engine = PredictionEngine(spins)

    predictions = engine.generate_predictions()

    for category in predictions.values():
        for prediction in category:
            assert "prediction_score" in prediction

            assert isinstance(
                prediction["prediction_score"],
                float,
            )

def test_all_prediction_categories_are_ranked():
    spins = [
        1, 2, 3, 1, 2,
        4, 5, 6, 7, 8,
        1, 2, 3, 10, 11,
    ]

    engine = PredictionEngine(spins)

    predictions = engine.generate_predictions(
        recent_window=10
    )

    for category in predictions.values():
        for index in range(len(category) - 1):
            assert (
                category[index]["prediction_score"]
                >=
                category[index + 1]["prediction_score"]
            )

def test_generated_predictions_have_no_duplicates():
    spins = [
        1, 4, 7, 10,
        2, 5, 8,
        3, 6, 9,
        12, 15, 18,
        21, 24,
    ]

    engine = PredictionEngine(spins)

    predictions = engine.generate_predictions()

    dozens = [
        item["dozen"]
        for item in predictions["dozens"]
    ]

    columns = [
        item["column"]
        for item in predictions["columns"]
    ]

    corners = [
        item["corner"]
        for item in predictions["corners"]
    ]

    splits = [
        item["split"]
        for item in predictions["splits"]
    ]

    streets = [
        item["street"]
        for item in predictions["streets"]
    ]

    assert len(dozens) == len(set(dozens))
    assert len(columns) == len(set(columns))
    assert len(corners) == len(set(corners))
    assert len(splits) == len(set(splits))
    assert len(streets) == len(set(streets))

def test_predictions_are_deterministic():
    spins = [
        12, 7, 31, 4, 18,
        22, 7, 14, 0, 27,
        7, 12, 5, 8, 19,
    ]

    engine_one = PredictionEngine(spins)
    engine_two = PredictionEngine(spins)

    predictions_one = (
        engine_one.generate_predictions(
            recent_window=10
        )
    )

    predictions_two = (
        engine_two.generate_predictions(
            recent_window=10
        )
    )

    assert predictions_one == predictions_two

def test_full_prediction_engine_empty_history():
    engine = PredictionEngine([])

    output = engine.build_prediction_output()

    assert output["spin_count"] == 0

    predictions = output["predictions"]

    assert len(predictions["dozens"]) == 2
    assert len(predictions["columns"]) == 2
    assert len(predictions["corners"]) == 5
    assert len(predictions["splits"]) == 12
    assert len(predictions["streets"]) == 6

    for category in predictions.values():
        for prediction in category:
            assert prediction["prediction_score"] == 0.0

def test_prediction_engine_single_spin():
    engine = PredictionEngine([7])

    output = engine.build_prediction_output(
        recent_window=10
    )

    assert output["spin_count"] == 1

    assert len(
        output["predictions"]["dozens"]
    ) == 2

    assert len(
        output["predictions"]["columns"]
    ) == 2

    assert len(
        output["predictions"]["corners"]
    ) == 5

    assert len(
        output["predictions"]["splits"]
    ) == 12

    assert len(
        output["predictions"]["streets"]
    ) == 6