from app.ml.dataset import (
    RouletteMLDatasetBuilder,
)
from app.ml.models import (
    RouletteGradientBoosting,
    RouletteLogisticRegression,
    RouletteRandomForest,
    RouletteXGBoost,
)


class RouletteMLTrainingPipeline:
    """
    Handle training and retraining of
    roulette ML models.
    """

    def __init__(
        self,
        minimum_history: int = 10,
        recent_window: int = 10,
    ):

        self.dataset_builder = (
            RouletteMLDatasetBuilder(
                minimum_history=minimum_history,
                recent_window=recent_window,
            )
        )

    def create_models(self) -> dict:

        return {
            "logistic_regression":
                RouletteLogisticRegression(),

            "random_forest":
                RouletteRandomForest(),

            "gradient_boosting":
                RouletteGradientBoosting(),

            "xgboost":
                RouletteXGBoost(),
        }

    def train_model(
        self,
        model,
        spins: list[int],
    ):

        dataset = (
            self.dataset_builder
            .build_dataset(spins)
        )

        if len(dataset.X) < 2:
            raise ValueError(
                "Insufficient ML training data."
            )

        model.fit(
            dataset.X,
            dataset.y,
        )

        return model

    def retrain_model(
        self,
        model,
        spins: list[int],
    ):
        """
        Full retraining using all currently
        available historical data.
        """

        return self.train_model(
            model,
            spins,
        )

    def chronological_training_split(
        self,
        spins: list[int],
        train_ratio: float = 0.8,
    ):

        dataset = (
            self.dataset_builder
            .build_dataset(spins)
        )

        return (
            self.dataset_builder
            .chronological_split(
                dataset,
                train_ratio=train_ratio,
            )
        )


def select_best_model(
    benchmark: dict,
) -> str | None:
    """
    Select best model using average
    roulette-category hit rate.
    """

    models = benchmark.get(
        "models",
        {}
    )

    if not models:
        return None

    best_name = None
    best_score = -1.0

    for model_name, result in models.items():

        category_rates = result[
            "category_hit_rates"
        ]

        scores = [
            category_rates[
                category
            ]["hit_rate"]
            for category in [
                "dozens",
                "columns",
                "streets",
                "splits",
                "corners",
            ]
        ]

        average_score = (
            sum(scores)
            / len(scores)
        )

        if average_score > best_score:

            best_score = average_score
            best_name = model_name

    return best_name