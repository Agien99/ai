class RouletteStatistics:
    """
    Analyze roulette spin history without modifying the session.
    """

    def __init__(self, spins: list[int]):
        self.spins = spins.copy()

    def __repr__(self):
        return (
            f"RouletteStatistics("
            f"spin_count={len(self.spins)}"
            f")"
        )