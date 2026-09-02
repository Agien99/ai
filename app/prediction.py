from app.statistics import RouletteStatistics


class PredictionEngine:
    """
    Generate ranked roulette bet-group predictions
    from session statistics.

    Version 1 uses deterministic scoring only.
    Machine learning will be added in a later phase.
    """

    def __init__(self, spins: list[int]):
        self.statistics = RouletteStatistics(spins)

    def get_statistics_summary(self) -> dict:
        """
        Return the statistical summary used by
        the prediction engine.
        """
        return self.statistics.get_summary()

    def calculate_frequency_score(
        self,
        total_hits: int,
        total_spins: int,
    ) -> float:
        """
        Calculate a normalized frequency score.

        Returns a value between 0.0 and 1.0.
        """
        if total_spins <= 0:
            return 0.0

        return total_hits / total_spins

    def calculate_recency_score(
        self,
        recent_hits: int,
        recent_window_size: int,
    ) -> float:
        """
        Calculate a normalized recent-frequency score.

        Returns a value between 0.0 and 1.0.
        """
        if recent_window_size <= 0:
            return 0.0

        return recent_hits / recent_window_size

    def calculate_activity_score(
        self,
        activity_count: int,
        total_spins: int,
    ) -> float:
        """
        Calculate a normalized bet-group activity score.

        Returns a value between 0.0 and 1.0.
        """
        if total_spins <= 0:
            return 0.0

        return activity_count / total_spins

    def calculate_prediction_score(
        self,
        frequency_score: float,
        recency_score: float,
        activity_score: float,
    ) -> float:
        """
        Combine the three V1 scoring components.

        V1 uses equal weighting.
        """
        return (
            frequency_score
            + recency_score
            + activity_score
        )

    def __repr__(self):
        return (
            f"PredictionEngine("
            f"spin_count={len(self.statistics.spins)}"
            f")"
        )