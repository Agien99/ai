import pytest

from app.ml.engine import RouletteMLEngine
from app.ml.features import (
    RouletteMLFeatureBuilder,
)
from app.ml.models import (
    RouletteGradientBoosting,
    RouletteLogisticRegression,
    RouletteRandomForest,
    RouletteXGBoost,
)


def build_training_data():
    builder = RouletteMLFeatureBuilder()

    histories = [
        [1, 2, 3, 4, 5],
        [2, 3, 4, 5, 6],
        [3, 4, 5, 6, 7],
        [4, 5, 6, 7, 8],
        [5, 6, 7, 8, 9],
        [6, 7, 8, 9, 10],
    ]

    X = [
        builder.build_features(history)
        for history in histories
    ]

    y = [
        10,
        20,
        10,
        20,
        10,
        20,
    ]

    return X, y


@pytest.mark.parametrize(
    "model_class",
    [
        RouletteLogisticRegression,
        RouletteRandomForest,
        RouletteGradientBoosting,
    ],
)
def test_model_training(model_class):
    X, y = build_training_data()

    model = model_class()

    model.fit(X, y)

    assert model.is_fitted is True


@pytest.mark.parametrize(
    "model_class",
    [
        RouletteLogisticRegression,
        RouletteRandomForest,
        RouletteGradientBoosting,
    ],
)
def test_number_probabilities(model_class):
    X, y = build_training_data()

    model = model_class()

    model.fit(X, y)

    probabilities = (
        model.predict_number_probabilities(
            X[0]
        )
    )

    assert len(probabilities) == 37

    assert set(probabilities.keys()) == set(
        range(37)
    )

    assert (
        abs(
            sum(probabilities.values())
            - 1.0
        )
        < 0.000001
    )


def test_unfitted_model_rejected():
    model = RouletteRandomForest()

    builder = RouletteMLFeatureBuilder()

    features = builder.build_features(
        [1, 2, 3]
    )

    with pytest.raises(ValueError):
        model.predict_number_probabilities(
            features
        )


def test_single_class_training_rejected():
    builder = RouletteMLFeatureBuilder()

    X = [
        builder.build_features(
            [1, 2, 3]
        ),
        builder.build_features(
            [4, 5, 6]
        ),
    ]

    y = [
        10,
        10,
    ]

    model = RouletteRandomForest()

    with pytest.raises(ValueError):
        model.fit(X, y)


def test_standardized_ml_output():
    X, y = build_training_data()

    model = RouletteRandomForest(
        random_state=42
    )

    model.fit(X, y)

    engine = RouletteMLEngine(
        model=model
    )

    output = engine.predict(
        [
            1, 5, 9, 12, 17,
            20, 24, 28, 31, 36,
        ]
    )

    assert (
        output["model"]
        == "random_forest"
    )

    assert output["spin_count"] == 10

    assert len(
        output["number_probabilities"]
    ) == 37

    probabilities = [
        item["probability"]
        for item
        in output[
            "number_probabilities"
        ]
    ]

    assert probabilities == sorted(
        probabilities,
        reverse=True,
    )

def test_xgboost_model_creation():
    model = RouletteXGBoost(
        random_state=42
    )

    assert model.model_name == "xgboost"
    assert model.is_fitted is False

def test_xgboost_training():

    X, y = build_training_data()

    model = RouletteXGBoost(
        random_state=42
    )

    model.fit(
        X,
        y,
    )

    probabilities = (
        model.predict_number_probabilities(
            X[0]
        )
    )

    assert model.is_fitted is True
    assert len(probabilities) == 37

    assert abs(
        sum(probabilities.values())
        - 1.0
    ) < 0.000001