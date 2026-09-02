import random

from app.roulette import (
    get_all_corners,
    get_all_splits,
    get_all_streets,
    get_column,
    get_corners_for_number,
    get_dozen,
    get_splits_for_number,
    get_street,
    validate_spin_history,
)


class RouletteBaselineEngine:
    """
    Generate simple baseline prediction strategies.

    These baselines will later be compared against
    Prediction Engine V1.

    Baselines:
    - Random
    - Frequency-only
    - Hot
    - Cold
    """

    def __init__(
        self,
        spins: list[int],
        recent_window: int = 10,
    ):
        validate_spin_history(spins)

        if recent_window <= 0:
            raise ValueError(
                "Recent window must be greater than 0."
            )

        self.spins = spins.copy()
        self.recent_window = recent_window

    # =========================================================
    # Shared Helpers
    # =========================================================

    def _recent_spins(self) -> list[int]:
        """
        Return the most recent spins based on
        the configured recent window.
        """
        return self.spins[-self.recent_window:]

    def _sort_scores(
        self,
        scores: dict,
        reverse: bool = True,
    ) -> list:
        """
        Sort score dictionary.

        Ties are resolved using the natural value
        of the roulette group so results remain
        deterministic.
        """
        if reverse:
            return sorted(
                scores.items(),
                key=lambda item: (
                    -item[1],
                    item[0],
                ),
            )

        return sorted(
            scores.items(),
            key=lambda item: (
                item[1],
                item[0],
            ),
        )

    # =========================================================
    # Step 2 - Random Baseline
    # =========================================================

    def generate_random_baseline(
        self,
        seed: int | None = None,
    ) -> dict:
        """
        Generate random predictions using the same
        prediction counts as Prediction Engine V1.

        Counts:
        - 2 dozens
        - 2 columns
        - 6 streets
        - 12 splits
        - 5 corners
        """
        rng = random.Random(seed)

        dozens = [1, 2, 3]
        columns = [1, 2, 3]

        streets = get_all_streets()
        splits = get_all_splits()
        corners = get_all_corners()

        selected_dozens = rng.sample(
            dozens,
            2,
        )

        selected_columns = rng.sample(
            columns,
            2,
        )

        selected_streets = rng.sample(
            streets,
            6,
        )

        selected_splits = rng.sample(
            splits,
            12,
        )

        selected_corners = rng.sample(
            corners,
            5,
        )

        return {
            "dozens": [
                {
                    "dozen": dozen,
                }
                for dozen in selected_dozens
            ],
            "columns": [
                {
                    "column": column,
                }
                for column in selected_columns
            ],
            "streets": [
                {
                    "street": street,
                }
                for street in selected_streets
            ],
            "splits": [
                {
                    "split": split,
                }
                for split in selected_splits
            ],
            "corners": [
                {
                    "corner": corner,
                }
                for corner in selected_corners
            ],
        }

    # =========================================================
    # Frequency Scoring Helpers
    # =========================================================

    def _calculate_group_frequencies(
        self,
        spins: list[int],
    ) -> dict:
        """
        Calculate frequency counts for every
        roulette prediction category.
        """

        dozen_scores = {
            1: 0,
            2: 0,
            3: 0,
        }

        column_scores = {
            1: 0,
            2: 0,
            3: 0,
        }

        street_scores = {
            street: 0
            for street in get_all_streets()
        }

        split_scores = {
            split: 0
            for split in get_all_splits()
        }

        corner_scores = {
            corner: 0
            for corner in get_all_corners()
        }

        for number in spins:

            if number == 0:
                continue

            dozen = get_dozen(number)

            if dozen is not None:
                dozen_scores[dozen] += 1

            column = get_column(number)

            if column is not None:
                column_scores[column] += 1

            street = get_street(number)

            if street is not None:
                street_scores[street] += 1

            for split in get_splits_for_number(number):
                split_scores[split] += 1

            for corner in get_corners_for_number(number):
                corner_scores[corner] += 1

        return {
            "dozens": dozen_scores,
            "columns": column_scores,
            "streets": street_scores,
            "splits": split_scores,
            "corners": corner_scores,
        }

    def _build_ranked_prediction(
        self,
        scores: dict,
        reverse: bool,
    ) -> dict:
        """
        Build predictions from group scores.

        reverse=True:
            Highest score first.

        reverse=False:
            Lowest score first.
        """

        ranked_dozens = self._sort_scores(
            scores["dozens"],
            reverse=reverse,
        )

        ranked_columns = self._sort_scores(
            scores["columns"],
            reverse=reverse,
        )

        ranked_streets = self._sort_scores(
            scores["streets"],
            reverse=reverse,
        )

        ranked_splits = self._sort_scores(
            scores["splits"],
            reverse=reverse,
        )

        ranked_corners = self._sort_scores(
            scores["corners"],
            reverse=reverse,
        )

        return {
            "dozens": [
                {
                    "dozen": group,
                    "frequency": score,
                }
                for group, score
                in ranked_dozens[:2]
            ],

            "columns": [
                {
                    "column": group,
                    "frequency": score,
                }
                for group, score
                in ranked_columns[:2]
            ],

            "streets": [
                {
                    "street": group,
                    "frequency": score,
                }
                for group, score
                in ranked_streets[:6]
            ],

            "splits": [
                {
                    "split": group,
                    "frequency": score,
                }
                for group, score
                in ranked_splits[:12]
            ],

            "corners": [
                {
                    "corner": group,
                    "frequency": score,
                }
                for group, score
                in ranked_corners[:5]
            ],
        }

    # =========================================================
    # Step 3 - Frequency-Only Baseline
    # =========================================================

    def generate_frequency_baseline(self) -> dict:
        """
        Generate predictions using only total
        historical frequency.

        Most frequently occurring groups are selected.
        """

        scores = self._calculate_group_frequencies(
            self.spins
        )

        return self._build_ranked_prediction(
            scores,
            reverse=True,
        )

    # =========================================================
    # Step 4 - Hot Baseline
    # =========================================================

    def generate_hot_baseline(self) -> dict:
        """
        Generate predictions using only recent
        roulette activity.

        Groups appearing most frequently inside
        the recent window are treated as HOT.
        """

        recent_spins = self._recent_spins()

        scores = self._calculate_group_frequencies(
            recent_spins
        )

        return self._build_ranked_prediction(
            scores,
            reverse=True,
        )

    # =========================================================
    # Step 5 - Cold Baseline
    # =========================================================

    def generate_cold_baseline(self) -> dict:
        """
        Generate predictions using groups with the
        lowest total historical frequency.

        Groups appearing least frequently are
        treated as COLD.
        """

        scores = self._calculate_group_frequencies(
            self.spins
        )

        return self._build_ranked_prediction(
            scores,
            reverse=False,
        )

    def __repr__(self):
        return (
            "RouletteBaselineEngine("
            f"spin_count={len(self.spins)}, "
            f"recent_window={self.recent_window}"
            ")"
        )