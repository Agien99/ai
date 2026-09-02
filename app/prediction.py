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

    def __repr__(self):
        return (
            f"PredictionEngine("
            f"spin_count={len(self.statistics.spins)}"
            f")"
        )