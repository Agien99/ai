from abc import ABC, abstractmethod

from sklearn.ensemble import (
    GradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.linear_model import LogisticRegression


class RouletteMLModel(ABC):
    """
    Base interface for roulette ML models.
    """

    model_name = "base"

    def __init__(self):
        self.model = None
        self.is_fitted = False

    def fit(
        self,
        X: list[list[float]],
        y: list[int],
    ):
        if not X:
            raise ValueError(
                "Training features cannot be empty."
            )

        if not y:
            raise ValueError(
                "Training targets cannot be empty."
            )

        if len(X) != len(y):
            raise ValueError(
                "Training feature and target "
                "counts do not match."
            )

        if len(set(y)) < 2:
            raise ValueError(
                "Training data must contain at least "
                "two target classes."
            )

        self.model.fit(
            X,
            y,
        )

        self.is_fitted = True

        return self

    def predict_number_probabilities(
        self,
        features: list[float],
    ) -> dict[int, float]:
        """
        Return probabilities for every roulette
        number 0-36.

        Numbers not learned by the classifier
        receive probability 0.
        """

        if not self.is_fitted:
            raise ValueError(
                "Model has not been fitted."
            )

        probabilities = (
            self.model.predict_proba(
                [features]
            )[0]
        )

        classes = self.model.classes_

        result = {
            number: 0.0
            for number in range(37)
        }

        for number, probability in zip(
            classes,
            probabilities,
        ):
            result[int(number)] = float(
                probability
            )

        return result


class RouletteLogisticRegression(
    RouletteMLModel
):
    model_name = "logistic_regression"

    def __init__(self):
        super().__init__()

        self.model = LogisticRegression(
            max_iter=2000,
        )


class RouletteRandomForest(
    RouletteMLModel
):
    model_name = "random_forest"

    def __init__(
        self,
        random_state: int = 42,
    ):
        super().__init__()

        self.model = RandomForestClassifier(
            n_estimators=100,
            random_state=random_state,
        )


class RouletteGradientBoosting(
    RouletteMLModel
):
    model_name = "gradient_boosting"

    def __init__(
        self,
        random_state: int = 42,
    ):
        super().__init__()

        self.model = GradientBoostingClassifier(
            random_state=random_state,
        )


class RouletteXGBoost(
    RouletteMLModel
):
    model_name = "xgboost"

    def __init__(
        self,
        random_state: int = 42,
    ):
        super().__init__()

        try:
            from xgboost import XGBClassifier

        except ImportError as error:
            raise ImportError(
                "XGBoost is not installed."
            ) from error

        self.model = XGBClassifier(
            n_estimators=100,
            max_depth=4,
            learning_rate=0.1,
            random_state=random_state,
            eval_metric="mlogloss",
        )