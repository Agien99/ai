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

    def get_comparison_summary(
        self,
    ) -> dict:
        """
        Build a comparison summary showing
        hit rates for every strategy by category.
        """

        rates = self.get_hit_rates_by_strategy()

        categories = [
            "dozens",
            "columns",
            "streets",
            "splits",
            "corners",
        ]

        summary = {
            category: {}
            for category in categories
        }

        for strategy, strategy_rates in rates.items():

            for category in categories:

                summary[category][strategy] = (
                    strategy_rates[
                        category
                    ]["hit_rate"]
                )

        return {
            "strategy_count": len(
                self.evaluators
            ),
            "comparison": summary,
        }

    def get_improvement_over_baselines(
        self,
        reference_strategy: str = "prediction_v1",
    ) -> dict:
        """
        Compare the reference strategy against
        every other strategy.

        Difference is returned both as:
        - decimal difference
        - percentage points
        """

        if reference_strategy not in self.evaluators:
            raise ValueError(
                f"Strategy not found: "
                f"{reference_strategy}"
            )

        rates = self.get_hit_rates_by_strategy()

        reference_rates = rates[
            reference_strategy
        ]

        categories = [
            "dozens",
            "columns",
            "streets",
            "splits",
            "corners",
        ]

        improvements = {}

        for strategy, strategy_rates in rates.items():

            if strategy == reference_strategy:
                continue

            improvements[strategy] = {}

            for category in categories:

                reference_rate = (
                    reference_rates[
                        category
                    ]["hit_rate"]
                )

                baseline_rate = (
                    strategy_rates[
                        category
                    ]["hit_rate"]
                )

                difference = (
                    reference_rate
                    - baseline_rate
                )

                improvements[strategy][category] = {
                    "reference_hit_rate":
                        reference_rate,

                    "baseline_hit_rate":
                        baseline_rate,

                    "difference":
                        difference,

                    "percentage_points":
                        difference * 100,
                }

        return improvements

    def validate_comparison_ready(
        self,
        reference_strategy: str = "prediction_v1",
    ) -> bool:
        """
        Validate that strategy comparison is fair
        and ready for analysis.
        """

        if reference_strategy not in self.evaluators:
            raise ValueError(
                f"Reference strategy not found: "
                f"{reference_strategy}"
            )

        if len(self.evaluators) < 2:
            raise ValueError(
                "At least two strategies are required "
                "for comparison."
            )

        evaluation_counts = {
            strategy: len(
                evaluator.evaluation_records
            )
            for strategy, evaluator
            in self.evaluators.items()
        }

        if any(
            count == 0
            for count in evaluation_counts.values()
        ):
            raise ValueError(
                "Every strategy must have at least "
                "one evaluation."
            )

        unique_counts = set(
            evaluation_counts.values()
        )

        if len(unique_counts) != 1:
            raise ValueError(
                "All strategies must be evaluated "
                "against the same number of spins."
            )

        return True

    def __repr__(self):
        return (
            "BaselineComparisonEngine("
            f"strategy_count="
            f"{len(self.evaluators)}"
            ")"
        )