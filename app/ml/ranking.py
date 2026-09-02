from app.roulette import (
    get_all_corners,
    get_all_splits,
    get_all_streets,
)


class RouletteMLBetRanker:
    """
    Convert probabilities for numbers 0-36
    into roulette betting-group rankings.
    """

    def validate_probabilities(
        self,
        probabilities: dict[int, float],
    ) -> bool:

        if not isinstance(probabilities, dict):
            raise ValueError(
                "Probabilities must be a dictionary."
            )

        if set(probabilities.keys()) != set(
            range(37)
        ):
            raise ValueError(
                "Probabilities must contain "
                "roulette numbers 0-36."
            )

        for probability in probabilities.values():

            if probability < 0:
                raise ValueError(
                    "Probability cannot be negative."
                )

        return True

    def _score_group(
        self,
        numbers,
        probabilities: dict[int, float],
    ) -> float:

        return sum(
            probabilities[number]
            for number in numbers
        )

    def rank(
        self,
        probabilities: dict[int, float],
    ) -> dict:

        self.validate_probabilities(
            probabilities
        )

        # -----------------------------------------
        # Dozens
        # -----------------------------------------

        dozens = {
            1: tuple(range(1, 13)),
            2: tuple(range(13, 25)),
            3: tuple(range(25, 37)),
        }

        dozen_scores = [
            {
                "dozen": dozen,
                "probability_score":
                    self._score_group(
                        numbers,
                        probabilities,
                    ),
            }
            for dozen, numbers
            in dozens.items()
        ]

        dozen_scores.sort(
            key=lambda item: (
                -item["probability_score"],
                item["dozen"],
            )
        )

        # -----------------------------------------
        # Columns
        # -----------------------------------------

        columns = {
            1: tuple(
                range(1, 37, 3)
            ),
            2: tuple(
                range(2, 37, 3)
            ),
            3: tuple(
                range(3, 37, 3)
            ),
        }

        column_scores = [
            {
                "column": column,
                "probability_score":
                    self._score_group(
                        numbers,
                        probabilities,
                    ),
            }
            for column, numbers
            in columns.items()
        ]

        column_scores.sort(
            key=lambda item: (
                -item["probability_score"],
                item["column"],
            )
        )

        # -----------------------------------------
        # Streets
        # -----------------------------------------

        street_scores = [
            {
                "street": street,
                "probability_score":
                    self._score_group(
                        street,
                        probabilities,
                    ),
            }
            for street
            in get_all_streets()
        ]

        street_scores.sort(
            key=lambda item: (
                -item["probability_score"],
                item["street"],
            )
        )

        # -----------------------------------------
        # Splits
        # -----------------------------------------

        split_scores = [
            {
                "split": split,
                "probability_score":
                    self._score_group(
                        split,
                        probabilities,
                    ),
            }
            for split
            in get_all_splits()
        ]

        split_scores.sort(
            key=lambda item: (
                -item["probability_score"],
                item["split"],
            )
        )

        # -----------------------------------------
        # Corners
        # -----------------------------------------

        corner_scores = [
            {
                "corner": corner,
                "probability_score":
                    self._score_group(
                        corner,
                        probabilities,
                    ),
            }
            for corner
            in get_all_corners()
        ]

        corner_scores.sort(
            key=lambda item: (
                -item["probability_score"],
                item["corner"],
            )
        )

        return {
            "dozens": dozen_scores[:2],
            "columns": column_scores[:2],
            "streets": street_scores[:6],
            "splits": split_scores[:12],
            "corners": corner_scores[:5],
        }