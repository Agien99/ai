from app.roulette import (
    get_column,
    get_dozen,
    validate_spin_history,
)


class RouletteMLFeatureBuilder:
    """
    Build machine-learning features from
    historical roulette spins.

    Features must only use past information.
    """

    def __init__(
        self,
        recent_window: int = 10,
    ):
        if recent_window <= 0:
            raise ValueError(
                "Recent window must be greater than 0."
            )

        self.recent_window = recent_window

    def build_features(
        self,
        spins: list[int],
    ) -> list[float]:
        """
        Convert historical spins into a fixed-length
        numerical feature vector.
        """
        validate_spin_history(spins)

        total_spins = len(spins)

        number_frequency = [
            0
            for _ in range(37)
        ]

        recent_frequency = [
            0
            for _ in range(37)
        ]

        spins_since_last = [
            total_spins + 1
            for _ in range(37)
        ]

        dozen_frequency = [
            0,
            0,
            0,
        ]

        column_frequency = [
            0,
            0,
            0,
        ]

        for number in spins:
            number_frequency[number] += 1

            dozen = get_dozen(number)

            if dozen is not None:
                dozen_frequency[
                    dozen - 1
                ] += 1

            column = get_column(number)

            if column is not None:
                column_frequency[
                    column - 1
                ] += 1

        recent_spins = spins[
            -self.recent_window:
        ]

        for number in recent_spins:
            recent_frequency[number] += 1

        for number in range(37):

            for distance, previous in enumerate(
                reversed(spins),
                start=0,
            ):
                if previous == number:
                    spins_since_last[
                        number
                    ] = distance
                    break

        features = []

        features.extend(number_frequency)
        features.extend(recent_frequency)
        features.extend(spins_since_last)
        features.extend(dozen_frequency)
        features.extend(column_frequency)

        features.append(total_spins)

        return [
            float(value)
            for value in features
        ]