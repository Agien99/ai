from app.ml.metrics import (
    RouletteMLMetrics,
)


def test_ml_metrics_empty():

    metrics = RouletteMLMetrics()

    summary = metrics.get_summary()

    assert (
        summary["prediction_count"]
        == 0
    )

    assert (
        summary["top_1_accuracy"]
        == 0.0
    )


def test_ml_metrics_top_accuracy():

    probabilities = {
        number: 0.0
        for number in range(37)
    }

    probabilities[17] = 0.7
    probabilities[7] = 0.2
    probabilities[20] = 0.1

    metrics = RouletteMLMetrics()

    metrics.add_prediction(
        probabilities,
        actual_number=17,
    )

    summary = metrics.get_summary()

    assert (
        summary["top_1_accuracy"]
        == 1.0
    )

    assert (
        summary["top_3_accuracy"]
        == 1.0
    )

    assert (
        summary["top_5_accuracy"]
        == 1.0
    )