import pytest

from app.ml.features import (
    RouletteMLFeatureBuilder,
)


def test_ml_feature_builder_creation():
    builder = RouletteMLFeatureBuilder()

    assert builder.recent_window == 10


def test_ml_feature_length():
    builder = RouletteMLFeatureBuilder()

    spins = [
        1, 5, 9, 12, 17,
        20, 24, 28, 31, 36,
    ]

    features = builder.build_features(
        spins
    )

    assert len(features) == 118


def test_ml_features_are_numeric():
    builder = RouletteMLFeatureBuilder()

    features = builder.build_features(
        [1, 2, 3, 4, 5]
    )

    assert all(
        isinstance(value, float)
        for value in features
    )


def test_invalid_recent_window():
    with pytest.raises(ValueError):
        RouletteMLFeatureBuilder(
            recent_window=0
        )


def test_invalid_spin_rejected():
    builder = RouletteMLFeatureBuilder()

    with pytest.raises(ValueError):
        builder.build_features(
            [1, 2, 37]
        )