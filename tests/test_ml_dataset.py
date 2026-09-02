import pytest

from app.ml.dataset import (
    RouletteMLDatasetBuilder,
)


def test_dataset_builder_creation():
    builder = RouletteMLDatasetBuilder()

    assert builder.minimum_history == 10


def test_dataset_generation():
    spins = [
        1, 2, 3, 4, 5,
        6, 7, 8, 9, 10,
        11, 12, 13, 14, 15,
    ]

    builder = RouletteMLDatasetBuilder(
        minimum_history=10
    )

    dataset = builder.build_dataset(
        spins
    )

    assert len(dataset.X) == 5
    assert len(dataset.y) == 5

    assert dataset.y == [
        11,
        12,
        13,
        14,
        15,
    ]


def test_dataset_prevents_future_leakage():
    spins = [
        1, 2, 3, 4, 5,
        6, 7, 8, 9, 10,
        36,
    ]

    builder = RouletteMLDatasetBuilder(
        minimum_history=10
    )

    dataset = builder.build_dataset(
        spins
    )

    first_features = dataset.X[0]

    number_frequency = (
        first_features[:37]
    )

    assert number_frequency[36] == 0.0

    assert dataset.y[0] == 36


def test_short_history_returns_empty_dataset():
    builder = RouletteMLDatasetBuilder(
        minimum_history=10
    )

    dataset = builder.build_dataset(
        [1, 2, 3]
    )

    assert dataset.X == []
    assert dataset.y == []


def test_chronological_split():
    spins = list(range(20))

    builder = RouletteMLDatasetBuilder(
        minimum_history=10
    )

    dataset = builder.build_dataset(
        spins
    )

    split = builder.chronological_split(
        dataset,
        train_ratio=0.8,
    )

    assert split.y_train == [
        10, 11, 12, 13,
        14, 15, 16, 17,
    ]

    assert split.y_test == [
        18, 19,
    ]


def test_invalid_train_ratio():
    builder = RouletteMLDatasetBuilder()

    dataset = builder.build_dataset(
        list(range(20))
    )

    with pytest.raises(ValueError):
        builder.chronological_split(
            dataset,
            train_ratio=1.0,
        )