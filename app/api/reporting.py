from typing import Any

from app.model_metric_repository import (
    ModelMetricRepository,
)
from app.model_version_repository import (
    ModelVersionRepository,
)
from app.prediction_item_repository import (
    PredictionItemRepository,
)
from app.prediction_run_repository import (
    PredictionRunRepository,
)


class APIReportingService:
    CATEGORIES = [
        "DOZENS",
        "COLUMNS",
        "STREETS",
        "SPLITS",
        "CORNERS",
    ]

    @staticmethod
    def get_session_evaluations(
        session_id: str,
    ) -> dict:
        runs = (
            PredictionRunRepository
            .get_session_prediction_runs(
                session_id
            )
        )

        evaluated_runs = [
            run
            for run in runs
            if run["evaluated_at"]
            is not None
        ]

        evaluations = []

        for run in evaluated_runs:
            items = (
                PredictionItemRepository
                .get_prediction_items(
                    str(
                        run[
                            "prediction_run_id"
                        ]
                    )
                )
            )

            categories = {}

            for item in items:
                category = item[
                    "category"
                ]

                if (
                    category
                    not in
                    APIReportingService.CATEGORIES
                ):
                    continue

                categories[category] = {
                    "is_hit":
                        item["is_hit"],
                    "payload":
                        item["payload"],
                    "evaluated_at":
                        item[
                            "evaluated_at"
                        ],
                }

            evaluations.append({
                "prediction_run_id":
                    run[
                        "prediction_run_id"
                    ],
                "strategy":
                    run[
                        "strategy_key"
                    ],
                "prediction_for_spin_index":
                    run[
                        "prediction_for_spin_index"
                    ],
                "actual_spin_id":
                    run[
                        "actual_spin_id"
                    ],
                "evaluated_at":
                    run[
                        "evaluated_at"
                    ],
                "categories":
                    categories,
            })

        return {
            "session_id":
                session_id,
            "evaluation_count":
                len(evaluations),
            "evaluations":
                evaluations,
        }

    @staticmethod
    def get_strategy_comparison(
        session_id: str,
    ) -> dict:
        evaluation_data = (
            APIReportingService
            .get_session_evaluations(
                session_id
            )
        )

        strategy_stats: dict[
            str,
            Any,
        ] = {}

        for evaluation in (
            evaluation_data[
                "evaluations"
            ]
        ):
            strategy = evaluation[
                "strategy"
            ]

            if strategy not in strategy_stats:
                strategy_stats[
                    strategy
                ] = {
                    "evaluation_count": 0,
                    "categories": {
                        category: {
                            "hits": 0,
                            "misses": 0,
                        }
                        for category
                        in APIReportingService
                        .CATEGORIES
                    },
                }

            strategy_stats[
                strategy
            ]["evaluation_count"] += 1

            for (
                category,
                result,
            ) in evaluation[
                "categories"
            ].items():
                if result["is_hit"]:
                    strategy_stats[
                        strategy
                    ]["categories"][
                        category
                    ]["hits"] += 1
                else:
                    strategy_stats[
                        strategy
                    ]["categories"][
                        category
                    ]["misses"] += 1

        for strategy in strategy_stats.values():
            for category in (
                strategy[
                    "categories"
                ].values()
            ):
                total = (
                    category["hits"]
                    + category["misses"]
                )

                category[
                    "total"
                ] = total

                category[
                    "hit_rate"
                ] = (
                    category["hits"] / total
                    if total
                    else 0.0
                )

        return {
            "session_id":
                session_id,
            "strategy_count":
                len(strategy_stats),
            "strategies":
                strategy_stats,
        }

    @staticmethod
    def get_ml_performance() -> dict:
        versions = (
            ModelVersionRepository
            .get_all_model_versions()
        )

        result = []

        for version in versions:
            metrics = (
                ModelMetricRepository
                .get_model_metrics(
                    str(
                        version[
                            "model_version_id"
                        ]
                    )
                )
            )

            result.append({
                "model_version":
                    version,
                "metrics":
                    metrics,
            })

        return {
            "model_count":
                len(result),
            "models":
                result,
        }

    @staticmethod
    def get_models() -> dict:
        versions = (
            ModelVersionRepository
            .get_all_model_versions()
        )

        return {
            "model_version_count":
                len(versions),
            "models":
                versions,
        }