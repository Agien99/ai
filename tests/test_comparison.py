from app.comparison import (
    BaselineComparisonEngine,
)
from app.baseline import RouletteBaselineEngine


def build_hit_predictions():
    return {
        "dozens": [
            {
                "dozen": 1,
                "prediction_score": 1.0,
            },
        ],
        "columns": [
            {
                "column": 1,
                "prediction_score": 1.0,
            },
        ],
        "streets": [
            {
                "street": (1, 2, 3),
                "prediction_score": 1.0,
            },
        ],
        "splits": [
            {
                "split": (1, 2),
                "prediction_score": 1.0,
            },
        ],
        "corners": [
            {
                "corner": (1, 2, 4, 5),
                "prediction_score": 1.0,
            },
        ],
    }


def build_miss_predictions():
    return {
        "dozens": [
            {
                "dozen": 2,
                "prediction_score": 1.0,
            },
        ],
        "columns": [
            {
                "column": 2,
                "prediction_score": 1.0,
            },
        ],
        "streets": [
            {
                "street": (4, 5, 6),
                "prediction_score": 1.0,
            },
        ],
        "splits": [
            {
                "split": (4, 5),
                "prediction_score": 1.0,
            },
        ],
        "corners": [
            {
                "corner": (4, 5, 7, 8),
                "prediction_score": 1.0,
            },
        ],
    }


def test_comparison_engine_creation():
    engine = BaselineComparisonEngine()

    assert isinstance(
        engine,
        BaselineComparisonEngine,
    )

    assert engine.evaluators == {}


def test_build_strategy_output():
    engine = BaselineComparisonEngine()

    predictions = build_hit_predictions()

    output = engine.build_strategy_output(
        "prediction_v1",
        predictions,
    )

    assert (
        output["strategy"]
        == "prediction_v1"
    )

    assert (
        output["predictions"]
        == predictions
    )


def test_evaluate_same_spin():
    engine = BaselineComparisonEngine()

    v1 = engine.build_strategy_output(
        "prediction_v1",
        build_hit_predictions(),
    )

    random_baseline = (
        engine.build_strategy_output(
            "random",
            build_miss_predictions(),
        )
    )

    results = engine.evaluate_same_spin(
        [
            v1,
            random_baseline,
        ],
        actual_number=1,
    )

    assert "prediction_v1" in results
    assert "random" in results

    assert (
        results[
            "prediction_v1"
        ].dozen_hit
        is True
    )

    assert (
        results[
            "prediction_v1"
        ].column_hit
        is True
    )

    assert (
        results[
            "prediction_v1"
        ].street_hit
        is True
    )

    assert (
        results[
            "prediction_v1"
        ].split_hit
        is True
    )

    assert (
        results[
            "prediction_v1"
        ].corner_hit
        is True
    )

    assert (
        results["random"].dozen_hit
        is False
    )

    assert (
        results["random"].column_hit
        is False
    )

    assert (
        results["random"].street_hit
        is False
    )

    assert (
        results["random"].split_hit
        is False
    )

    assert (
        results["random"].corner_hit
        is False
    )

def test_hit_miss_counts_by_strategy():
    engine = BaselineComparisonEngine()

    v1 = engine.build_strategy_output(
        "prediction_v1",
        build_hit_predictions(),
    )

    random_baseline = (
        engine.build_strategy_output(
            "random",
            build_miss_predictions(),
        )
    )

    engine.evaluate_same_spin(
        [
            v1,
            random_baseline,
        ],
        actual_number=1,
    )

    counts = (
        engine.get_hit_miss_counts_by_strategy()
    )

    assert (
        counts[
            "prediction_v1"
        ]["dozens"]["hits"]
        == 1
    )

    assert (
        counts[
            "prediction_v1"
        ]["dozens"]["misses"]
        == 0
    )

    assert (
        counts[
            "random"
        ]["dozens"]["hits"]
        == 0
    )

    assert (
        counts[
            "random"
        ]["dozens"]["misses"]
        == 1
    )

def test_hit_rates_by_strategy():
    engine = BaselineComparisonEngine()

    v1_hit = engine.build_strategy_output(
        "prediction_v1",
        build_hit_predictions(),
    )

    random_miss = (
        engine.build_strategy_output(
            "random",
            build_miss_predictions(),
        )
    )

    engine.evaluate_same_spin(
        [
            v1_hit,
            random_miss,
        ],
        actual_number=1,
    )

    engine.evaluate_same_spin(
        [
            v1_hit,
            random_miss,
        ],
        actual_number=36,
    )

    rates = (
        engine.get_hit_rates_by_strategy()
    )

    assert (
        rates[
            "prediction_v1"
        ]["dozens"]["total"]
        == 2
    )

    assert (
        rates[
            "prediction_v1"
        ]["dozens"]["hits"]
        == 1
    )

    assert (
        rates[
            "prediction_v1"
        ]["dozens"]["misses"]
        == 1
    )

    assert (
        rates[
            "prediction_v1"
        ]["dozens"]["hit_rate"]
        == 0.5
    )

    assert (
        rates[
            "random"
        ]["dozens"]["hit_rate"]
        == 0.0
    )

def test_comparison_summary():
    engine = BaselineComparisonEngine()

    v1 = engine.build_strategy_output(
        "prediction_v1",
        build_hit_predictions(),
    )

    random_baseline = (
        engine.build_strategy_output(
            "random",
            build_miss_predictions(),
        )
    )

    engine.evaluate_same_spin(
        [
            v1,
            random_baseline,
        ],
        actual_number=1,
    )

    engine.evaluate_same_spin(
        [
            v1,
            random_baseline,
        ],
        actual_number=36,
    )

    summary = (
        engine.get_comparison_summary()
    )

    assert summary["strategy_count"] == 2

    assert (
        summary[
            "comparison"
        ]["dozens"]["prediction_v1"]
        == 0.5
    )

    assert (
        summary[
            "comparison"
        ]["dozens"]["random"]
        == 0.0
    )

def test_improvement_over_baseline():
    engine = BaselineComparisonEngine()

    v1 = engine.build_strategy_output(
        "prediction_v1",
        build_hit_predictions(),
    )

    random_baseline = (
        engine.build_strategy_output(
            "random",
            build_miss_predictions(),
        )
    )

    engine.evaluate_same_spin(
        [
            v1,
            random_baseline,
        ],
        actual_number=1,
    )

    engine.evaluate_same_spin(
        [
            v1,
            random_baseline,
        ],
        actual_number=36,
    )

    improvement = (
        engine.get_improvement_over_baselines()
    )

    dozen_result = (
        improvement[
            "random"
        ]["dozens"]
    )

    assert (
        dozen_result[
            "reference_hit_rate"
        ]
        == 0.5
    )

    assert (
        dozen_result[
            "baseline_hit_rate"
        ]
        == 0.0
    )

    assert (
        dozen_result["difference"]
        == 0.5
    )

    assert (
        dozen_result[
            "percentage_points"
        ]
        == 50.0
    )

def test_comparison_ready():
    engine = BaselineComparisonEngine()

    v1 = engine.build_strategy_output(
        "prediction_v1",
        build_hit_predictions(),
    )

    random_baseline = (
        engine.build_strategy_output(
            "random",
            build_miss_predictions(),
        )
    )

    engine.evaluate_same_spin(
        [
            v1,
            random_baseline,
        ],
        actual_number=1,
    )

    assert (
        engine.validate_comparison_ready()
        is True
    )

def test_comparison_missing_reference_strategy():
    engine = BaselineComparisonEngine()

    try:
        engine.validate_comparison_ready()

        assert False

    except ValueError as error:
        assert (
            "Reference strategy not found"
            in str(error)
        )

def test_comparison_requires_two_strategies():
    engine = BaselineComparisonEngine()

    v1 = engine.build_strategy_output(
        "prediction_v1",
        build_hit_predictions(),
    )

    engine.evaluate_strategy(
        v1,
        actual_number=1,
    )

    try:
        engine.validate_comparison_ready()

        assert False

    except ValueError as error:
        assert (
            "At least two strategies"
            in str(error)
        )

def test_comparison_requires_equal_evaluations():
    engine = BaselineComparisonEngine()

    v1 = engine.build_strategy_output(
        "prediction_v1",
        build_hit_predictions(),
    )

    random_baseline = (
        engine.build_strategy_output(
            "random",
            build_miss_predictions(),
        )
    )

    engine.evaluate_same_spin(
        [
            v1,
            random_baseline,
        ],
        actual_number=1,
    )

    engine.evaluate_strategy(
        v1,
        actual_number=2,
    )

    try:
        engine.validate_comparison_ready()

        assert False

    except ValueError as error:
        assert (
            "same number of spins"
            in str(error)
        )

def test_all_strategies_same_spin_integration():
    spins = [
        7, 14, 21, 7, 8,
        17, 32, 7, 14, 5,
        26, 17, 8, 7, 30,
    ]

    baseline_engine = (
        RouletteBaselineEngine(spins)
    )

    comparison_engine = (
        BaselineComparisonEngine()
    )

    v1_output = (
        comparison_engine.build_strategy_output(
            "prediction_v1",
            build_hit_predictions(),
        )
    )

    baseline_outputs = (
        baseline_engine.generate_all_baselines(
            random_seed=42
        )
    )

    all_strategies = [
        v1_output,
        *baseline_outputs,
    ]

    results = (
        comparison_engine.evaluate_same_spin(
            all_strategies,
            actual_number=1,
        )
    )

    assert len(results) == 5

    assert "prediction_v1" in results
    assert "random" in results
    assert "frequency" in results
    assert "hot" in results
    assert "cold" in results

    assert (
        comparison_engine
        .validate_comparison_ready()
        is True
    )

    counts = (
        comparison_engine
        .get_hit_miss_counts_by_strategy()
    )

    for strategy in [
        "prediction_v1",
        "random",
        "frequency",
        "hot",
        "cold",
    ]:

        assert (
            counts[
                strategy
            ]["dozens"]["hits"]
            +
            counts[
                strategy
            ]["dozens"]["misses"]
            == 1
        )