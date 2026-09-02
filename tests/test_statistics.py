from app.statistics import RouletteStatistics


def test_statistics_creation():
    spins = [
        12, 7, 31, 4, 18,
        22, 9, 14, 0, 27,
    ]

    stats = RouletteStatistics(spins)

    assert stats.spins == spins
    assert len(stats.spins) == 10