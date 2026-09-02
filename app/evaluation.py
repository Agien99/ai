from dataclasses import dataclass
from datetime import datetime

from app.roulette import is_valid_number


@dataclass
class PredictionEvaluationRecord:
    """
    Represents one prediction evaluation event.

    A prediction must already exist before the
    actual roulette result is evaluated.
    """

    actual_number: int
    evaluated_at: datetime

    dozen_hit: bool = False
    column_hit: bool = False
    street_hit: bool = False
    split_hit: bool = False
    corner_hit: bool = False


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

    def create_evaluation_record(
        self,
        actual_number: int,
    ) -> PredictionEvaluationRecord:
        """
        Create a new evaluation record for
        an actual roulette result.

        HIT / MISS values start as False and
        will be filled by later evaluation steps.
        """
        self.validate_actual_number(actual_number)

        return PredictionEvaluationRecord(
            actual_number=actual_number,
            evaluated_at=datetime.now(),
        )

    def __repr__(self):
        return "PredictionEvaluationEngine()"