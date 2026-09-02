from app.ml.ranking import (
    RouletteMLBetRanker,
)


def test_ml_bet_ranking_counts():

    probabilities = {
        number: 1 / 37
        for number in range(37)
    }

    ranker = RouletteMLBetRanker()

    predictions = ranker.rank(
        probabilities
    )

    assert len(
        predictions["dozens"]
    ) == 2

    assert len(
        predictions["columns"]
    ) == 2

    assert len(
        predictions["streets"]
    ) == 6

    assert len(
        predictions["splits"]
    ) == 12

    assert len(
        predictions["corners"]
    ) == 5


def test_high_probability_numbers_affect_dozen():

    probabilities = {
        number: 0.0
        for number in range(37)
    }

    probabilities[1] = 0.4
    probabilities[2] = 0.3
    probabilities[20] = 0.2
    probabilities[30] = 0.1

    ranker = RouletteMLBetRanker()

    predictions = ranker.rank(
        probabilities
    )

    assert (
        predictions["dozens"][0]["dozen"]
        == 1
    )