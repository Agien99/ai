from app.statistics import RouletteStatistics
from app.roulette import (
    get_all_corners,
    get_all_splits,
    get_all_streets,
    get_corners_for_number,
    get_splits_for_number,
    get_street,
)

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

    def score_dozens(
        self,
        recent_window: int = 10,
    ) -> list[dict]:
        """
        Score all three roulette dozens.

        Returns a ranked list from highest score to lowest.
        Zero is excluded because it does not belong to a dozen.
        """
        summary = self.get_statistics_summary()

        total_spins = summary["spin_count"]

        recent_frequency = self.statistics.get_recent_frequency(
            recent_window
        )

        dozen_frequency = summary["dozen_frequency"]

        results = []

        for dozen in range(1, 4):
            key = f"dozen_{dozen}"

            total_hits = dozen_frequency[key]

            recent_hits = 0

            for number, count in recent_frequency.items():
                if number == 0:
                    continue

                if 1 <= number <= 12 and dozen == 1:
                    recent_hits += count

                elif 13 <= number <= 24 and dozen == 2:
                    recent_hits += count

                elif 25 <= number <= 36 and dozen == 3:
                    recent_hits += count

            actual_recent_window = min(
                recent_window,
                total_spins,
            )

            frequency_score = self.calculate_frequency_score(
                total_hits,
                total_spins,
            )

            recency_score = self.calculate_recency_score(
                recent_hits,
                actual_recent_window,
            )

            activity_score = self.calculate_activity_score(
                total_hits,
                total_spins,
            )

            prediction_score = self.calculate_prediction_score(
                frequency_score,
                recency_score,
                activity_score,
            )

            results.append({
                "dozen": dozen,
                "total_hits": total_hits,
                "recent_hits": recent_hits,
                "frequency_score": frequency_score,
                "recency_score": recency_score,
                "activity_score": activity_score,
                "prediction_score": prediction_score,
            })

        return sorted(
            results,
            key=lambda item: (
                -item["prediction_score"],
                item["dozen"],
            ),
        )

    def score_columns(
        self,
        recent_window: int = 10,
    ) -> list[dict]:
        """
        Score all three roulette columns.

        Returns a ranked list from highest score to lowest.
        Zero is excluded because it does not belong to a column.
        """
        summary = self.get_statistics_summary()

        total_spins = summary["spin_count"]

        recent_frequency = self.statistics.get_recent_frequency(
            recent_window
        )

        column_frequency = summary["column_frequency"]

        results = []

        for column in range(1, 4):
            key = f"column_{column}"

            total_hits = column_frequency[key]

            recent_hits = 0

            for number, count in recent_frequency.items():
                if number == 0:
                    continue

                remainder = number % 3

                if remainder == 1:
                    number_column = 1
                elif remainder == 2:
                    number_column = 2
                else:
                    number_column = 3

                if number_column == column:
                    recent_hits += count

            actual_recent_window = min(
                recent_window,
                total_spins,
            )

            frequency_score = self.calculate_frequency_score(
                total_hits,
                total_spins,
            )

            recency_score = self.calculate_recency_score(
                recent_hits,
                actual_recent_window,
            )

            activity_score = self.calculate_activity_score(
                total_hits,
                total_spins,
            )

            prediction_score = self.calculate_prediction_score(
                frequency_score,
                recency_score,
                activity_score,
            )

            results.append({
                "column": column,
                "total_hits": total_hits,
                "recent_hits": recent_hits,
                "frequency_score": frequency_score,
                "recency_score": recency_score,
                "activity_score": activity_score,
                "prediction_score": prediction_score,
            })

        return sorted(
            results,
            key=lambda item: (
                -item["prediction_score"],
                item["column"],
            ),
        )

    def score_streets(
        self,
        recent_window: int = 10,
    ) -> list[dict]:
        """
        Score all 12 standard roulette streets.

        Returns a ranked list from highest score to lowest.
        Zero is ignored because it does not belong to a standard street.
        """
        total_spins = len(self.statistics.spins)

        full_activity = (
            self.statistics.get_street_activity()
        )

        recent_spins = self.statistics.spins[
            -recent_window:
        ]

        recent_activity = {
            street: 0
            for street in get_all_streets()
        }

        for number in recent_spins:
            street = get_street(number)

            if street is not None:
                recent_activity[street] += 1

        actual_recent_window = min(
            recent_window,
            total_spins,
        )

        results = []

        for street in get_all_streets():
            total_hits = full_activity[street]
            recent_hits = recent_activity[street]

            frequency_score = (
                self.calculate_frequency_score(
                    total_hits,
                    total_spins,
                )
            )

            recency_score = (
                self.calculate_recency_score(
                    recent_hits,
                    actual_recent_window,
                )
            )

            activity_score = (
                self.calculate_activity_score(
                    total_hits,
                    total_spins,
                )
            )

            prediction_score = (
                self.calculate_prediction_score(
                    frequency_score,
                    recency_score,
                    activity_score,
                )
            )

            results.append({
                "street": street,
                "total_hits": total_hits,
                "recent_hits": recent_hits,
                "frequency_score": frequency_score,
                "recency_score": recency_score,
                "activity_score": activity_score,
                "prediction_score": prediction_score,
            })

        return sorted(
            results,
            key=lambda item: (
                -item["prediction_score"],
                item["street"],
            ),
        )

    def score_splits(
        self,
        recent_window: int = 10,
    ) -> list[dict]:
        """
        Score all 57 standard roulette splits.

        A single spin may contribute to multiple split candidates.
        Zero is ignored because standard splits cover 1-36 only.
        """
        total_spins = len(self.statistics.spins)

        full_activity = (
            self.statistics.get_split_activity()
        )

        recent_spins = self.statistics.spins[
            -recent_window:
        ]

        recent_activity = {
            split: 0
            for split in get_all_splits()
        }

        for number in recent_spins:
            splits = get_splits_for_number(number)

            for split in splits:
                recent_activity[split] += 1

        actual_recent_window = min(
            recent_window,
            total_spins,
        )

        results = []

        for split in get_all_splits():
            total_hits = full_activity[split]
            recent_hits = recent_activity[split]

            frequency_score = (
                self.calculate_frequency_score(
                    total_hits,
                    total_spins,
                )
            )

            recency_score = (
                self.calculate_recency_score(
                    recent_hits,
                    actual_recent_window,
                )
            )

            activity_score = (
                self.calculate_activity_score(
                    total_hits,
                    total_spins,
                )
            )

            prediction_score = (
                self.calculate_prediction_score(
                    frequency_score,
                    recency_score,
                    activity_score,
                )
            )

            results.append({
                "split": split,
                "total_hits": total_hits,
                "recent_hits": recent_hits,
                "frequency_score": frequency_score,
                "recency_score": recency_score,
                "activity_score": activity_score,
                "prediction_score": prediction_score,
            })

        return sorted(
            results,
            key=lambda item: (
                -item["prediction_score"],
                item["split"],
            ),
        )

    def score_corners(
        self,
        recent_window: int = 10,
    ) -> list[dict]:
        """
        Score all 22 standard roulette corners.

        A single spin may contribute to multiple corner candidates.
        Zero is ignored because standard corners cover 1-36 only.
        """
        total_spins = len(self.statistics.spins)

        full_activity = (
            self.statistics.get_corner_activity()
        )

        recent_spins = self.statistics.spins[
            -recent_window:
        ]

        recent_activity = {
            corner: 0
            for corner in get_all_corners()
        }

        for number in recent_spins:
            corners = get_corners_for_number(number)

            for corner in corners:
                recent_activity[corner] += 1

        actual_recent_window = min(
            recent_window,
            total_spins,
        )

        results = []

        for corner in get_all_corners():
            total_hits = full_activity[corner]
            recent_hits = recent_activity[corner]

            frequency_score = (
                self.calculate_frequency_score(
                    total_hits,
                    total_spins,
                )
            )

            recency_score = (
                self.calculate_recency_score(
                    recent_hits,
                    actual_recent_window,
                )
            )

            activity_score = (
                self.calculate_activity_score(
                    total_hits,
                    total_spins,
                )
            )

            prediction_score = (
                self.calculate_prediction_score(
                    frequency_score,
                    recency_score,
                    activity_score,
                )
            )

            results.append({
                "corner": corner,
                "total_hits": total_hits,
                "recent_hits": recent_hits,
                "frequency_score": frequency_score,
                "recency_score": recency_score,
                "activity_score": activity_score,
                "prediction_score": prediction_score,
            })

        return sorted(
            results,
            key=lambda item: (
                -item["prediction_score"],
                item["corner"],
            ),
        )

        def rank_predictions(
            self,
            predictions: list[dict],
            key_name: str,
            limit: int | None = None,
        ) -> list[dict]:
            """
            Rank prediction candidates by prediction score.

            Highest score comes first.

            Ties are resolved deterministically using the
            candidate key.

            If limit is provided, only the top N predictions
            are returned.
            """
            ranked = sorted(
                predictions,
                key=lambda item: (
                    -item["prediction_score"],
                    item[key_name],
                ),
            )

            if limit is None:
                return ranked

            return ranked[:limit]

    def __repr__(self):
        return (
            f"PredictionEngine("
            f"spin_count={len(self.statistics.spins)}"
            f")"
        )