from app.evaluation import (
    PredictionEvaluationRecord,
)
from app.prediction_item_repository import (
    PredictionItemRepository,
)
from app.prediction_run_repository import (
    PredictionRunRepository,
)


class EvaluationStorageService:
    CATEGORY_HIT_FIELDS = {
        "DOZENS": "dozen_hit",
        "COLUMNS": "column_hit",
        "STREETS": "street_hit",
        "SPLITS": "split_hit",
        "CORNERS": "corner_hit",
    }

    @staticmethod
    def save_evaluation(
        prediction_run_id: str,
        actual_spin_id: str,
        evaluation: PredictionEvaluationRecord,
    ) -> None:
        # Link the prediction run to the actual
        # spin that evaluated it.
        PredictionRunRepository.evaluate_prediction_run(
            prediction_run_id,
            actual_spin_id,
        )

        items = (
            PredictionItemRepository
            .get_prediction_items(
                prediction_run_id
            )
        )

        for item in items:
            category = item["category"]

            # ML number probabilities are not
            # category HIT/MISS predictions.
            if category == "NUMBER_PROBABILITIES":
                continue

            hit_field = (
                EvaluationStorageService
                .CATEGORY_HIT_FIELDS
                .get(category)
            )

            if hit_field is None:
                continue

            is_hit = getattr(
                evaluation,
                hit_field,
            )

            (
                PredictionItemRepository
                .update_evaluation(
                    str(
                        item[
                            "prediction_item_id"
                        ]
                    ),
                    is_hit,
                )
            )