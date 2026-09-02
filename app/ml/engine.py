from app.ml.features import (
    RouletteMLFeatureBuilder,
)
from app.ml.models import RouletteMLModel
from app.roulette import validate_spin_history


class RouletteMLEngine:
    """
    Coordinate ML feature generation and
    standardized prediction output.
    """

    def __init__(
        self,
        model: RouletteMLModel,
        recent_window: int = 10,
    ):
        if not isinstance(
            model,
            RouletteMLModel,
        ):
            raise ValueError(
                "Model must be a RouletteMLModel."
            )

        self.model = model

        self.feature_builder = (
            RouletteMLFeatureBuilder(
                recent_window=recent_window
            )
        )

    def predict(
        self,
        spins: list[int],
    ) -> dict:
        """
        Generate standardized ML prediction output.
        """
        validate_spin_history(spins)

        if not spins:
            raise ValueError(
                "Spin history cannot be empty."
            )

        features = (
            self.feature_builder
            .build_features(spins)
        )

        probabilities = (
            self.model
            .predict_number_probabilities(
                features
            )
        )

        ranked_numbers = sorted(
            probabilities.items(),
            key=lambda item: (
                -item[1],
                item[0],
            ),
        )

        return {
            "model": self.model.model_name,
            "spin_count": len(spins),

            "number_probabilities": [
                {
                    "number": number,
                    "probability": probability,
                }
                for number, probability
                in ranked_numbers
            ],
        }