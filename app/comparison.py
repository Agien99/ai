from app.evaluation import (
    PredictionEvaluationEngine,
    PredictionEvaluationRecord,
)


class BaselineComparisonEngine:
    """
    Compare multiple prediction strategies against
    the same actual roulette result.

    Each strategy has its own evaluation engine so
    HIT / MISS statistics remain separated.
    """

    def __init__(self):
        self.evaluators = {}

    def build_strategy_output(
        self,
        strategy: str,
        predictions: dict,
    ) -> dict:
        """
        Wrap any prediction set in the standardized
        strategy structure.

        This is especially useful for Prediction
        Engine V1.
        """
        if not isinstance(strategy, str):
            raise ValueError(
                "Strategy must be a string."
            )

        if not strategy.strip():
            raise ValueError(
                "Strategy cannot be empty."
            )

        if not isinstance(predictions, dict):
            raise ValueError(
                "Predictions must be a dictionary."
            )

        return {
            "strategy": strategy,
            "predictions": predictions,
        }

    def validate_strategy_output(
        self,
        strategy_output: dict,
    ) -> bool:
        """
        Validate standardized strategy output.
        """
        if not isinstance(strategy_output, dict):
            raise ValueError(
                "Strategy output must be a dictionary."
            )

        if "strategy" not in strategy_output:
            raise ValueError(
                "Missing strategy label."
            )

        if "predictions" not in strategy_output:
            raise ValueError(
                "Missing predictions."
            )

        strategy = strategy_output["strategy"]

        if not isinstance(strategy, str):
            raise ValueError(
                "Strategy must be a string."
            )

        if not strategy.strip():
            raise ValueError(
                "Strategy cannot be empty."
            )

        if not isinstance(
            strategy_output["predictions"],
            dict,
        ):
            raise ValueError(
                "Predictions must be a dictionary."
            )

        return True

    def _get_evaluator(
        self,
        strategy: str,
    ) -> PredictionEvaluationEngine:
        """
        Return the evaluator assigned to a strategy.

        Create one if the strategy has not yet
        been evaluated.
        """
        if strategy not in self.evaluators:
            self.evaluators[
                strategy
            ] = PredictionEvaluationEngine()

        return self.evaluators[strategy]

    def evaluate_strategy(
        self,
        strategy_output: dict,
        actual_number: int,
    ) -> PredictionEvaluationRecord:
        """
        Evaluate one strategy against one actual
        roulette result.
        """
        self.validate_strategy_output(
            strategy_output
        )

        strategy = strategy_output["strategy"]

        evaluator = self._get_evaluator(
            strategy
        )

        return evaluator.evaluate_prediction_set(
            strategy_output["predictions"],
            actual_number,
        )

    def evaluate_same_spin(
        self,
        strategy_outputs: list[dict],
        actual_number: int,
    ) -> dict:
        """
        Evaluate multiple strategies against
        exactly the same actual roulette result.
        """
        if not isinstance(
            strategy_outputs,
            list,
        ):
            raise ValueError(
                "Strategy outputs must be a list."
            )

        results = {}

        for strategy_output in strategy_outputs:

            self.validate_strategy_output(
                strategy_output
            )

            strategy = strategy_output[
                "strategy"
            ]

            if strategy in results:
                raise ValueError(
                    f"Duplicate strategy: {strategy}"
                )

            results[strategy] = (
                self.evaluate_strategy(
                    strategy_output,
                    actual_number,
                )
            )

        return results

    def get_hit_miss_counts_by_strategy(
        self,
    ) -> dict:
        """
        Return HIT / MISS counts separately
        for every evaluated strategy.
        """
        return {
            strategy: evaluator.get_hit_miss_counts()
            for strategy, evaluator
            in self.evaluators.items()
        }

    def get_hit_rates_by_strategy(
        self,
    ) -> dict:
        """
        Return hit rates separately
        for every evaluated strategy.
        """
        return {
            strategy: evaluator.get_hit_rates()
            for strategy, evaluator
            in self.evaluators.items()
        }

    def __repr__(self):
        return (
            "BaselineComparisonEngine("
            f"strategy_count="
            f"{len(self.evaluators)}"
            ")"
        )