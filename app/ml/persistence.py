from pathlib import Path

import joblib

from app.ml.models import RouletteMLModel


class RouletteMLModelPersistence:
    """
    Save and load trained roulette ML models.
    """

    @staticmethod
    def save(
        model: RouletteMLModel,
        filepath: str,
    ) -> str:

        if not isinstance(
            model,
            RouletteMLModel,
        ):
            raise ValueError(
                "Model must be a RouletteMLModel."
            )

        if not model.is_fitted:
            raise ValueError(
                "Cannot save an unfitted model."
            )

        path = Path(filepath)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        joblib.dump(
            model,
            path,
        )

        return str(path)

    @staticmethod
    def load(
        filepath: str,
    ) -> RouletteMLModel:

        path = Path(filepath)

        if not path.exists():
            raise ValueError(
                f"Model file not found: "
                f"{filepath}"
            )

        model = joblib.load(
            path
        )

        if not isinstance(
            model,
            RouletteMLModel,
        ):
            raise ValueError(
                "Invalid roulette ML model file."
            )

        return model