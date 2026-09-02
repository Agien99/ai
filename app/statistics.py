class RouletteStatistics:
    """
    Analyze roulette spin history without modifying the session.
    """

    def __init__(self, spins: list[int]):
        self.spins = spins.copy()

    def get_number_frequency(self) -> dict[int, int]:
        """
        Return the frequency of every roulette number from 0 to 36.

        Numbers that have not appeared will have a frequency of 0.
        """
        frequency = {
            number: 0
            for number in range(37)
        }

        for number in self.spins:
            frequency[number] += 1

        return frequency

    def __repr__(self):
        return (
            f"RouletteStatistics("
            f"spin_count={len(self.spins)}"
            f")"
        )