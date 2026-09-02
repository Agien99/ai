from app.ml.features import (
    RouletteMLFeatureBuilder,
)
from app.ml.models import RouletteMLModel
from app.ml.ranking import (
    RouletteMLBetRanker,
)
from app.roulette import validate_spin_history


class RouletteMLEngine:
    """
    Generate complete standardized ML
    roulette predictions.
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

        self.ranker = RouletteMLBetRanker()

    def predict_from_features(
        self,
        features: list[float],
        spin_count: int = 0,
    ) -> dict:

        probabilities = (
            self.model
            .predict_number_probabilities(
                features
            )
        )

        predictions = self.ranker.rank(
            probabilities
        )

        ranked_numbers = sorted(
            probabilities.items(),
            key=lambda item: (
                -item[1],
                item[0],
            ),
        )

        return {
            "strategy":
                f"ml_{self.model.model_name}",

            "model":
                self.model.model_name,

            "spin_count":
                spin_count,

            "number_probabilities": [
                {
                    "number": number,
                    "probability": probability,
                }
                for number, probability
                in ranked_numbers
            ],

            "predictions": predictions,
        }

    def predict(
        self,
        spins: list[int],
    ) -> dict:

        validate_spin_history(spins)

        if not spins:
            raise ValueError(
                "Spin history cannot be empty."
            )

        features = (
            self.feature_builder
            .build_features(spins)
        )

        return self.predict_from_features(
            features,
            spin_count=len(spins),
        )