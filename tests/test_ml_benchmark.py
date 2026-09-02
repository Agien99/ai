from app.ml.benchmark import (
    RouletteMLBenchmark,
)


def build_benchmark_history():

    pattern = [
        1, 7, 14, 21, 30,
        17, 8, 25, 32, 5,
        12, 19, 28, 36, 3,
    ]

    return pattern * 4


def test_ml_final_benchmark():

    benchmark = RouletteMLBenchmark(
        minimum_history=10,
    )

    report = benchmark.run(
        build_benchmark_history(),
        train_ratio=0.8,
    )

    assert report[
        "training_rows"
    ] > 0

    assert report[
        "testing_rows"
    ] > 0

    assert set(
        report["models"].keys()
    ) == {
        "logistic_regression",
        "random_forest",
        "gradient_boosting",
        "xgboost",
    }

    assert report[
        "best_model"
    ] in report["models"]

    for model_result in (
        report["models"].values()
    ):

        rates = model_result[
            "category_hit_rates"
        ]

        assert "dozens" in rates
        assert "columns" in rates
        assert "streets" in rates
        assert "splits" in rates
        assert "corners" in rates