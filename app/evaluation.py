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
        self.evaluation_records = []

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

    def evaluate_dozens(
        self,
        predicted_dozens: list[dict],
        actual_number: int,
    ) -> bool:
        """
        Evaluate whether the actual roulette number
        matches any predicted dozen.
        """
        self.validate_actual_number(actual_number)

        if actual_number == 0:
            return False

        if 1 <= actual_number <= 12:
            actual_dozen = 1
        elif 13 <= actual_number <= 24:
            actual_dozen = 2
        else:
            actual_dozen = 3

        return any(
            item["dozen"] == actual_dozen
            for item in predicted_dozens
        )

    def evaluate_dozens_for_record(
        self,
        record: PredictionEvaluationRecord,
        predicted_dozens: list[dict],
    ) -> PredictionEvaluationRecord:
        """
        Update an evaluation record with
        the dozen HIT / MISS result.
        """
        record.dozen_hit = self.evaluate_dozens(
            predicted_dozens,
            record.actual_number,
        )

        return record

    def evaluate_columns(
        self,
        predicted_columns: list[dict],
        actual_number: int,
    ) -> bool:
        """
        Evaluate whether the actual roulette number
        matches any predicted column.
        """
        self.validate_actual_number(actual_number)

        if actual_number == 0:
            return False

        remainder = actual_number % 3

        if remainder == 1:
            actual_column = 1
        elif remainder == 2:
            actual_column = 2
        else:
            actual_column = 3

        return any(
            item["column"] == actual_column
            for item in predicted_columns
        )


    def evaluate_columns_for_record(
        self,
        record: PredictionEvaluationRecord,
        predicted_columns: list[dict],
    ) -> PredictionEvaluationRecord:
        """
        Update an evaluation record with
        the column HIT / MISS result.
        """
        record.column_hit = self.evaluate_columns(
            predicted_columns,
            record.actual_number,
        )

        return record

    def evaluate_streets(
        self,
        predicted_streets: list[dict],
        actual_number: int,
    ) -> bool:
        """
        Evaluate whether the actual roulette number
        matches any predicted street.
        """
        self.validate_actual_number(actual_number)

        if actual_number == 0:
            return False

        return any(
            actual_number in item["street"]
            for item in predicted_streets
        )

    def evaluate_streets_for_record(
        self,
        record: PredictionEvaluationRecord,
        predicted_streets: list[dict],
    ) -> PredictionEvaluationRecord:
        """
        Update an evaluation record with
        the street HIT / MISS result.
        """
        record.street_hit = self.evaluate_streets(
            predicted_streets,
            record.actual_number,
        )

        return record

    def evaluate_splits(
        self,
        predicted_splits: list[dict],
        actual_number: int,
    ) -> bool:
        """
        Evaluate whether the actual roulette number
        matches any predicted split.
        """
        self.validate_actual_number(actual_number)

        if actual_number == 0:
            return False

        return any(
            actual_number in item["split"]
            for item in predicted_splits
        )


    def evaluate_splits_for_record(
        self,
        record: PredictionEvaluationRecord,
        predicted_splits: list[dict],
    ) -> PredictionEvaluationRecord:
        """
        Update an evaluation record with
        the split HIT / MISS result.
        """
        record.split_hit = self.evaluate_splits(
            predicted_splits,
            record.actual_number,
        )

        return record

    def evaluate_corners(
        self,
        predicted_corners: list[dict],
        actual_number: int,
    ) -> bool:
        """
        Evaluate whether the actual roulette number
        matches any predicted corner.
        """
        self.validate_actual_number(actual_number)

        if actual_number == 0:
            return False

        return any(
            actual_number in item["corner"]
            for item in predicted_corners
        )


    def evaluate_corners_for_record(
        self,
        record: PredictionEvaluationRecord,
        predicted_corners: list[dict],
    ) -> PredictionEvaluationRecord:
        """
        Update an evaluation record with
        the corner HIT / MISS result.
        """
        record.corner_hit = self.evaluate_corners(
            predicted_corners,
            record.actual_number,
        )

        return record

    def evaluate_prediction_set(
        self,
        predictions: dict,
        actual_number: int,
    ) -> PredictionEvaluationRecord:
        """
        Evaluate a complete prediction set against
        one actual roulette result.
        """
        record = self.create_evaluation_record(
            actual_number=actual_number
        )

        self.evaluate_dozens_for_record(
            record,
            predictions["dozens"],
        )

        self.evaluate_columns_for_record(
            record,
            predictions["columns"],
        )

        self.evaluate_streets_for_record(
            record,
            predictions["streets"],
        )

        self.evaluate_splits_for_record(
            record,
            predictions["splits"],
        )

        self.evaluate_corners_for_record(
            record,
            predictions["corners"],
        )

        self.evaluation_records.append(record)

        return record

    def get_hit_miss_counts(self) -> dict:
        """
        Calculate HIT / MISS counts from all
        completed prediction evaluations.
        """
        counts = {
            "dozens": {
                "hits": 0,
                "misses": 0,
            },
            "columns": {
                "hits": 0,
                "misses": 0,
            },
            "streets": {
                "hits": 0,
                "misses": 0,
            },
            "splits": {
                "hits": 0,
                "misses": 0,
            },
            "corners": {
                "hits": 0,
                "misses": 0,
            },
        }

        for record in self.evaluation_records:

            if record.dozen_hit:
                counts["dozens"]["hits"] += 1
            else:
                counts["dozens"]["misses"] += 1

            if record.column_hit:
                counts["columns"]["hits"] += 1
            else:
                counts["columns"]["misses"] += 1

            if record.street_hit:
                counts["streets"]["hits"] += 1
            else:
                counts["streets"]["misses"] += 1

            if record.split_hit:
                counts["splits"]["hits"] += 1
            else:
                counts["splits"]["misses"] += 1

            if record.corner_hit:
                counts["corners"]["hits"] += 1
            else:
                counts["corners"]["misses"] += 1

        return counts

    def get_hit_rates(self) -> dict:
        """
        Calculate hit rates for each prediction category.
        """
        counts = self.get_hit_miss_counts()

        rates = {}

        for category, result in counts.items():
            hits = result["hits"]
            misses = result["misses"]

            total = hits + misses

            if total == 0:
                hit_rate = 0.0
            else:
                hit_rate = hits / total

            rates[category] = {
                "hits": hits,
                "misses": misses,
                "total": total,
                "hit_rate": hit_rate,
            }

        return rates

    def get_session_evaluation_summary(self) -> dict:
        """
        Return a complete summary of all prediction
        evaluations completed in the current session.
        """
        rates = self.get_hit_rates()

        return {
            "evaluation_count": len(
                self.evaluation_records
            ),
            "dozens": rates["dozens"],
            "columns": rates["columns"],
            "streets": rates["streets"],
            "splits": rates["splits"],
            "corners": rates["corners"],
        }

    def __repr__(self):
        return "PredictionEvaluationEngine()"