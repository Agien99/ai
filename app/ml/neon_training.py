from app.ml.dataset import (
    RouletteMLDataset,
    RouletteMLDatasetBuilder,
)
from app.ml.models import RouletteMLModel
from app.session_repository import (
    SessionRepository,
)
from app.spin_repository import SpinRepository


class NeonTrainingDataService:
    def __init__(
        self,
        minimum_history: int = 10,
        recent_window: int = 10,
    ):
        self.minimum_history = minimum_history

        self.dataset_builder = (
            RouletteMLDatasetBuilder(
                minimum_history=minimum_history,
                recent_window=recent_window,
            )
        )

    def load_training_sequences(
        self,
    ) -> list[list[int]]:
        sessions = (
            SessionRepository.get_all_sessions()
        )

        sequences = []

        for session in sessions:
            session_id = str(
                session["session_id"]
            )

            spin_rows = (
                SpinRepository
                .get_session_spins(
                    session_id
                )
            )

            spins = [
                row["number"]
                for row in spin_rows
            ]

            # We need at least one target spin
            # after the minimum history.
            if len(spins) <= self.minimum_history:
                continue

            sequences.append(spins)

        return sequences

    def build_training_dataset(
        self,
    ) -> RouletteMLDataset:
        sequences = (
            self.load_training_sequences()
        )

        all_X = []
        all_y = []

        for spins in sequences:
            dataset = (
                self.dataset_builder
                .build_dataset(spins)
            )

            all_X.extend(dataset.X)
            all_y.extend(dataset.y)

        return RouletteMLDataset(
            X=all_X,
            y=all_y,
        )


class NeonRetrainingService:
    def __init__(
        self,
        minimum_history: int = 10,
        recent_window: int = 10,
    ):
        self.training_data = (
            NeonTrainingDataService(
                minimum_history=minimum_history,
                recent_window=recent_window,
            )
        )

    def train_model(
        self,
        model: RouletteMLModel,
    ) -> RouletteMLModel:
        dataset = (
            self.training_data
            .build_training_dataset()
        )

        if not dataset.X:
            raise ValueError(
                "Not enough historical Neon "
                "data to train the model."
            )

        model.fit(
            dataset.X,
            dataset.y,
        )

        return model

    def retrain_model(
        self,
        model: RouletteMLModel,
    ) -> RouletteMLModel:
        # Retraining currently performs a full
        # rebuild using all stored historical
        # sessions.
        return self.train_model(model)