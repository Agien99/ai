from dataclasses import dataclass

from app.ml.features import (
    RouletteMLFeatureBuilder,
)
from app.roulette import validate_spin_history


@dataclass
class RouletteMLDataset:
    X: list[list[float]]
    y: list[int]


@dataclass
class RouletteMLSplit:
    X_train: list[list[float]]
    X_test: list[list[float]]

    y_train: list[int]
    y_test: list[int]


class RouletteMLDatasetBuilder:
    """
    Build sequential ML training data.

    Target:
        Predict the next roulette number 0-36.
    """

    def __init__(
        self,
        minimum_history: int = 10,
        recent_window: int = 10,
    ):
        if minimum_history <= 0:
            raise ValueError(
                "Minimum history must be greater than 0."
            )

        self.minimum_history = minimum_history

        self.feature_builder = (
            RouletteMLFeatureBuilder(
                recent_window=recent_window
            )
        )

    def build_dataset(
        self,
        spins: list[int],
    ) -> RouletteMLDataset:
        """
        Example:

        Spins:
        [1, 2, 3, ..., 17]

        Features from spins 1-10
            -> target spin 11

        Features from spins 1-11
            -> target spin 12

        etc.
        """
        validate_spin_history(spins)

        X = []
        y = []

        if len(spins) <= self.minimum_history:
            return RouletteMLDataset(
                X=X,
                y=y,
            )

        for target_index in range(
            self.minimum_history,
            len(spins),
        ):
            history = spins[
                :target_index
            ]

            target = spins[
                target_index
            ]

            features = (
                self.feature_builder
                .build_features(history)
            )

            X.append(features)
            y.append(target)

        return RouletteMLDataset(
            X=X,
            y=y,
        )

    def chronological_split(
        self,
        dataset: RouletteMLDataset,
        train_ratio: float = 0.8,
    ) -> RouletteMLSplit:
        """
        Chronological split.

        Older observations become training data.
        Newer observations become testing data.
        """

        if not 0 < train_ratio < 1:
            raise ValueError(
                "Train ratio must be between 0 and 1."
            )

        if len(dataset.X) != len(dataset.y):
            raise ValueError(
                "Feature and target counts do not match."
            )

        total_rows = len(dataset.X)

        if total_rows < 2:
            raise ValueError(
                "At least two dataset rows are required "
                "for train/test splitting."
            )

        split_index = int(
            total_rows * train_ratio
        )

        if split_index <= 0:
            split_index = 1

        if split_index >= total_rows:
            split_index = total_rows - 1

        return RouletteMLSplit(
            X_train=dataset.X[:split_index],
            X_test=dataset.X[split_index:],
            y_train=dataset.y[:split_index],
            y_test=dataset.y[split_index:],
        )