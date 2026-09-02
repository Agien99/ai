from app.evaluation import (
    PredictionEvaluationEngine,
)
from app.ml.engine import RouletteMLEngine
from app.ml.metrics import RouletteMLMetrics
from app.ml.training import (
    RouletteMLTrainingPipeline,
    select_best_model,
)


class RouletteMLBenchmark:
    """
    Train and evaluate ML models using
    chronological unseen test data.
    """

    def __init__(
        self,
        minimum_history: int = 10,
        recent_window: int = 10,
    ):

        self.pipeline = (
            RouletteMLTrainingPipeline(
                minimum_history=minimum_history,
                recent_window=recent_window,
            )
        )

    def run(
        self,
        spins: list[int],
        train_ratio: float = 0.8,
    ) -> dict:

        split = (
            self.pipeline
            .chronological_training_split(
                spins,
                train_ratio=train_ratio,
            )
        )

        if len(set(split.y_train)) < 2:
            raise ValueError(
                "Training split must contain "
                "at least two classes."
            )

        models = (
            self.pipeline.create_models()
        )

        report = {
            "training_rows":
                len(split.X_train),

            "testing_rows":
                len(split.X_test),

            "models": {},
        }

        for model_name, model in models.items():

            model.fit(
                split.X_train,
                split.y_train,
            )

            ml_engine = RouletteMLEngine(
                model
            )

            evaluator = (
                PredictionEvaluationEngine()
            )

            metrics = (
                RouletteMLMetrics()
            )

            for features, actual_number in zip(
                split.X_test,
                split.y_test,
            ):

                output = (
                    ml_engine
                    .predict_from_features(
                        features
                    )
                )

                evaluator.evaluate_prediction_set(
                    output["predictions"],
                    actual_number,
                )

                probabilities = {
                    item["number"]:
                        item["probability"]
                    for item
                    in output[
                        "number_probabilities"
                    ]
                }

                metrics.add_prediction(
                    probabilities,
                    actual_number,
                )

            report["models"][
                model_name
            ] = {
                "category_hit_rates":
                    evaluator.get_hit_rates(),

                "number_metrics":
                    metrics.get_summary(),
            }

        report[
            "best_model"
        ] = select_best_model(
            report
        )

        return report