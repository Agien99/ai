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

    def get_recent_frequency(self, window: int) -> dict[int, int]:
        """
        Return number frequency for the most recent spins.

        If the requested window is larger than the available history,
        the entire available history is used.
        """
        if not isinstance(window, int) or window <= 0:
            raise ValueError("Window must be a positive integer.")

        recent_spins = self.spins[-window:]

        frequency = {
            number: 0
            for number in range(37)
        }

        for number in recent_spins:
            frequency[number] += 1

        return frequency

    def __repr__(self):
        return (
            f"RouletteStatistics("
            f"spin_count={len(self.spins)}"
            f")"
        )