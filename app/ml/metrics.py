class RouletteMLMetrics:
    """
    Calculate number-level ML performance metrics.
    """

    def __init__(self):
        self.records = []

    def add_prediction(
        self,
        probabilities: dict[int, float],
        actual_number: int,
    ):

        if actual_number not in range(37):
            raise ValueError(
                f"Invalid roulette number: "
                f"{actual_number}"
            )

        ranked = sorted(
            probabilities.items(),
            key=lambda item: (
                -item[1],
                item[0],
            ),
        )

        ranked_numbers = [
            number
            for number, _
            in ranked
        ]

        self.records.append({
            "actual_number": actual_number,

            "actual_probability":
                probabilities[
                    actual_number
                ],

            "rank":
                ranked_numbers.index(
                    actual_number
                ) + 1,
        })

    def get_summary(self) -> dict:

        if not self.records:
            return {
                "prediction_count": 0,
                "top_1_accuracy": 0.0,
                "top_3_accuracy": 0.0,
                "top_5_accuracy": 0.0,
                "average_actual_probability": 0.0,
            }

        total = len(self.records)

        top_1 = sum(
            record["rank"] <= 1
            for record in self.records
        )

        top_3 = sum(
            record["rank"] <= 3
            for record in self.records
        )

        top_5 = sum(
            record["rank"] <= 5
            for record in self.records
        )

        average_probability = (
            sum(
                record[
                    "actual_probability"
                ]
                for record in self.records
            )
            / total
        )

        return {
            "prediction_count": total,

            "top_1_accuracy":
                top_1 / total,

            "top_3_accuracy":
                top_3 / total,

            "top_5_accuracy":
                top_5 / total,

            "average_actual_probability":
                average_probability,
        }