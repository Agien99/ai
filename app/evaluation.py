from app.roulette import is_valid_number


class PredictionEvaluationEngine:
    """
    Evaluate previously generated roulette predictions
    against the next actual roulette result.

    This engine does not generate predictions.
    It only evaluates predictions that were already created.
    """

    def __init__(self):
        pass

    def validate_actual_number(
        self,
        actual_number: int,
    ) -> bool:
        """
        Validate the actual roulette result.
        """
        if not is_valid_number(actual_number):
            raise ValueError(
                f"Invalid roulette number: {actual_number}"
            )

        return True

    def __repr__(self):
        return "PredictionEvaluationEngine()"