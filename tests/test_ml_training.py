from app.ml.models import (
    RouletteRandomForest,
)
from app.ml.persistence import (
    RouletteMLModelPersistence,
)
from app.ml.training import (
    RouletteMLTrainingPipeline,
)


def build_long_spin_history():

    return [
        number % 37
        for number in range(100)
    ]


def test_ml_training_pipeline():

    pipeline = (
        RouletteMLTrainingPipeline()
    )

    model = RouletteRandomForest(
        random_state=42
    )

    trained = pipeline.train_model(
        model,
        build_long_spin_history(),
    )

    assert trained.is_fitted is True


def test_ml_model_persistence(
    tmp_path,
):

    pipeline = (
        RouletteMLTrainingPipeline()
    )

    model = RouletteRandomForest(
        random_state=42
    )

    pipeline.train_model(
        model,
        build_long_spin_history(),
    )

    filepath = (
        tmp_path
        / "roulette_model.joblib"
    )

    RouletteMLModelPersistence.save(
        model,
        str(filepath),
    )

    loaded = (
        RouletteMLModelPersistence.load(
            str(filepath)
        )
    )

    assert loaded.is_fitted is True

    assert (
        loaded.model_name
        == "random_forest"
    )