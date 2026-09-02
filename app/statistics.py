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

    def get_spins_since_last_appearance(self) -> dict[int, int | None]:
        """
        Return how many spins have occurred since each roulette number
        last appeared.

        Returns:
            0 if the number was the most recent spin.
            None if the number has never appeared.
        """
        result = {
            number: None
            for number in range(37)
        }

        for distance, number in enumerate(reversed(self.spins)):
            if result[number] is None:
                result[number] = distance

        return result

    def get_hot_numbers(self, limit: int = 5) -> list[tuple[int, int]]:
        """
        Return the most frequently appearing roulette numbers.

        Each result is:
            (number, frequency)
        """
        if not isinstance(limit, int) or limit <= 0:
            raise ValueError("Limit must be a positive integer.")

        frequency = self.get_number_frequency()

        ranked = sorted(
            frequency.items(),
            key=lambda item: (-item[1], item[0]),
        )

        return ranked[:limit]


    def get_cold_numbers(self, limit: int = 5) -> list[tuple[int, int]]:
        """
        Return the least frequently appearing roulette numbers.

        Each result is:
            (number, frequency)
        """
        if not isinstance(limit, int) or limit <= 0:
            raise ValueError("Limit must be a positive integer.")

        frequency = self.get_number_frequency()

        ranked = sorted(
            frequency.items(),
            key=lambda item: (item[1], item[0]),
        )

        return ranked[:limit]

    def __repr__(self):
        return (
            f"RouletteStatistics("
            f"spin_count={len(self.spins)}"
            f")"
        )