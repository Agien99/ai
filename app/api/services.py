from typing import Any

from app.api.errors import APIError
from app.baseline import RouletteBaselineEngine
from app.evaluation import (
    PredictionEvaluationEngine,
    PredictionEvaluationRecord,
)
from app.evaluation_storage_service import (
    EvaluationStorageService,
)
from app.ml.engine import RouletteMLEngine
from app.ml.persistence import (
    RouletteMLModelPersistence,
)
from app.model_version_repository import (
    ModelVersionRepository,
)
from app.prediction import PredictionEngine
from app.prediction_item_repository import (
    PredictionItemRepository,
)
from app.prediction_run_repository import (
    PredictionRunRepository,
)
from app.session import RouletteSession
from app.statistics import RouletteStatistics


class APIStatisticsService:
    @staticmethod
    def _group_activity_to_list(
        activity: dict,
        group_name: str,
    ) -> list[dict]:
        return [
            {
                group_name: list(group),
                "count": count,
            }
            for group, count in activity.items()
        ]

    @staticmethod
    def build_statistics(
        session: RouletteSession,
    ) -> dict:
        statistics = RouletteStatistics(
            session.spins
        )

        summary = statistics.get_summary()

        return {
            "spin_count": summary[
                "spin_count"
            ],
            "number_frequency": summary[
                "number_frequency"
            ],
            "recent_frequency": summary[
                "recent_frequency"
            ],
            "spins_since_last_appearance":
                summary[
                    "spins_since_last_appearance"
                ],
            "hot_numbers": [
                {
                    "number": number,
                    "frequency": frequency,
                }
                for number, frequency
                in summary["hot_numbers"]
            ],
            "cold_numbers": [
                {
                    "number": number,
                    "frequency": frequency,
                }
                for number, frequency
                in summary["cold_numbers"]
            ],
            "dozen_frequency": summary[
                "dozen_frequency"
            ],
            "column_frequency": summary[
                "column_frequency"
            ],
            "street_activity":
                APIStatisticsService
                ._group_activity_to_list(
                    summary[
                        "street_activity"
                    ],
                    "street",
                ),
            "split_activity":
                APIStatisticsService
                ._group_activity_to_list(
                    summary[
                        "split_activity"
                    ],
                    "split",
                ),
            "corner_activity":
                APIStatisticsService
                ._group_activity_to_list(
                    summary[
                        "corner_activity"
                    ],
                    "corner",
                ),
        }


class APIPredictionService:
    CATEGORY_MAP = {
        "dozens": "DOZENS",
        "columns": "COLUMNS",
        "streets": "STREETS",
        "splits": "SPLITS",
        "corners": "CORNERS",
    }

    BASELINE_METHODS = {
        "baseline_random":
            "generate_random_output",
        "baseline_frequency":
            "generate_frequency_output",
        "baseline_hot":
            "generate_hot_output",
        "baseline_cold":
            "generate_cold_output",
    }

    @staticmethod
    def _generate_v1(
        spins: list[int],
        recent_window: int,
    ) -> dict:
        engine = PredictionEngine(spins)

        output = engine.build_prediction_output(
            recent_window=recent_window
        )

        return {
            "strategy": "v1",
            "predictions": output[
                "predictions"
            ],
            "number_probabilities": None,
            "model_version_id": None,
        }

    @staticmethod
    def _generate_baseline(
        spins: list[int],
        strategy: str,
        recent_window: int,
    ) -> dict:
        engine = RouletteBaselineEngine(
            spins,
            recent_window=recent_window,
        )

        method_name = (
            APIPredictionService
            .BASELINE_METHODS[strategy]
        )

        method = getattr(
            engine,
            method_name,
        )

        output = method()

        return {
            "strategy": strategy,
            "predictions": output[
                "predictions"
            ],
            "number_probabilities": None,
            "model_version_id": None,
        }

    @staticmethod
    def _generate_ml(
        spins: list[int],
        strategy: str,
        recent_window: int,
    ) -> dict:
        model_name = strategy.removeprefix(
            "ml_"
        )

        model_version = (
            ModelVersionRepository
            .get_active_model_version(
                model_name
            )
        )

        if model_version is None:
            raise APIError(
                status_code=404,
                message=(
                    "No active model version "
                    f"found for {model_name}."
                ),
            )

        artifact_path = model_version.get(
            "artifact_path"
        )

        if not artifact_path:
            raise APIError(
                status_code=409,
                message=(
                    "The active ML model does not "
                    "have a model artifact."
                ),
            )

        try:
            model = (
                RouletteMLModelPersistence.load(
                    artifact_path
                )
            )

        except ValueError as error:
            raise APIError(
                status_code=500,
                message=str(error),
            ) from error

        engine = RouletteMLEngine(
            model=model,
            recent_window=recent_window,
        )

        output = engine.predict(spins)

        return {
            "strategy": strategy,
            "predictions": output[
                "predictions"
            ],
            "number_probabilities": output[
                "number_probabilities"
            ],
            "model_version_id": str(
                model_version[
                    "model_version_id"
                ]
            ),
        }

    @staticmethod
    def generate(
        session: RouletteSession,
        strategy: str,
        recent_window: int = 10,
    ) -> dict:
        if session.status != "ACTIVE":
            raise APIError(
                status_code=409,
                message=(
                    "Predictions can only be "
                    "generated for an active "
                    "session."
                ),
            )

        if strategy == "v1":
            result = (
                APIPredictionService
                ._generate_v1(
                    session.spins,
                    recent_window,
                )
            )

        elif strategy.startswith(
            "baseline_"
        ):
            result = (
                APIPredictionService
                ._generate_baseline(
                    session.spins,
                    strategy,
                    recent_window,
                )
            )

        elif strategy.startswith("ml_"):
            result = (
                APIPredictionService
                ._generate_ml(
                    session.spins,
                    strategy,
                    recent_window,
                )
            )

        else:
            raise APIError(
                status_code=400,
                message=(
                    "Unsupported prediction "
                    "strategy."
                ),
            )

        prediction_for_spin_index = (
            len(session.spins) + 1
        )

        prediction_run = (
            PredictionRunRepository
            .create_prediction_run(
                session_id=session.session_id,
                strategy_key=strategy,
                prediction_for_spin_index=(
                    prediction_for_spin_index
                ),
                input_spin_count=len(
                    session.spins
                ),
                recent_window=recent_window,
                model_version_id=result[
                    "model_version_id"
                ],
            )
        )

        prediction_run_id = str(
            prediction_run[
                "prediction_run_id"
            ]
        )

        for (
            prediction_key,
            database_category,
        ) in (
            APIPredictionService
            .CATEGORY_MAP.items()
        ):
            (
                PredictionItemRepository
                .create_prediction_item(
                    prediction_run_id=(
                        prediction_run_id
                    ),
                    category=(
                        database_category
                    ),
                    payload=result[
                        "predictions"
                    ][prediction_key],
                )
            )

        if (
            result[
                "number_probabilities"
            ]
            is not None
        ):
            (
                PredictionItemRepository
                .create_prediction_item(
                    prediction_run_id=(
                        prediction_run_id
                    ),
                    category=(
                        "NUMBER_PROBABILITIES"
                    ),
                    payload=result[
                        "number_probabilities"
                    ],
                )
            )

        return {
            "prediction_run_id":
                prediction_run[
                    "prediction_run_id"
                ],
            "session_id":
                prediction_run[
                    "session_id"
                ],
            "strategy": strategy,
            "prediction_for_spin_index":
                prediction_run[
                    "prediction_for_spin_index"
                ],
            "input_spin_count":
                prediction_run[
                    "input_spin_count"
                ],
            "recent_window":
                prediction_run[
                    "recent_window"
                ],
            "model_version_id":
                prediction_run[
                    "model_version_id"
                ],
            "predictions": result[
                "predictions"
            ],
            "number_probabilities": result[
                "number_probabilities"
            ],
        }

    @staticmethod
    def get_latest(
        session_id: str,
    ) -> dict | None:
        prediction_run = (
            PredictionRunRepository
            .get_latest_prediction_run(
                session_id
            )
        )

        if prediction_run is None:
            return None

        items = (
            PredictionItemRepository
            .get_prediction_items(
                str(
                    prediction_run[
                        "prediction_run_id"
                    ]
                )
            )
        )

        return {
            "prediction_run":
                prediction_run,
            "prediction_items":
                items,
        }


class APIEvaluationService:
    CATEGORY_MAP = {
        "DOZENS": "dozens",
        "COLUMNS": "columns",
        "STREETS": "streets",
        "SPLITS": "splits",
        "CORNERS": "corners",
    }

    @staticmethod
    def evaluate(
        prediction_run_id: str,
        actual_spin_id: str,
        actual_number: int,
    ) -> PredictionEvaluationRecord:
        items = (
            PredictionItemRepository
            .get_prediction_items(
                prediction_run_id
            )
        )

        if not items:
            raise APIError(
                status_code=404,
                message=(
                    "Prediction items were "
                    "not found."
                ),
            )

        predictions: dict[
            str,
            Any,
        ] = {}

        for item in items:
            category = item["category"]

            prediction_key = (
                APIEvaluationService
                .CATEGORY_MAP.get(category)
            )

            if prediction_key is None:
                continue

            predictions[
                prediction_key
            ] = item["payload"]

        required = {
            "dozens",
            "columns",
            "streets",
            "splits",
            "corners",
        }

        if set(predictions) != required:
            raise APIError(
                status_code=500,
                message=(
                    "Stored prediction data "
                    "is incomplete."
                ),
            )

        engine = (
            PredictionEvaluationEngine()
        )

        evaluation = (
            engine.evaluate_prediction_set(
                predictions,
                actual_number,
            )
        )

        EvaluationStorageService.save_evaluation(
            prediction_run_id=(
                prediction_run_id
            ),
            actual_spin_id=actual_spin_id,
            evaluation=evaluation,
        )

        return evaluation