from app.statistics import RouletteStatistics


def test_statistics_creation():
    spins = [
        12, 7, 31, 4, 18,
        22, 9, 14, 0, 27,
    ]

    stats = RouletteStatistics(spins)

    assert stats.spins == spins
    assert len(stats.spins) == 10

def test_number_frequency():
    spins = [
        12, 7, 31, 4, 18,
        22, 7, 14, 0, 27,
        7, 12,
    ]

    stats = RouletteStatistics(spins)

    frequency = stats.get_number_frequency()

    assert frequency[7] == 3
    assert frequency[12] == 2

    assert frequency[0] == 1
    assert frequency[31] == 1

    assert frequency[36] == 0

    assert len(frequency) == 37

def test_recent_frequency():
    spins = [
        12, 7, 31, 4, 18,
        22, 7, 14, 0, 27,
        7, 12,
    ]

    stats = RouletteStatistics(spins)

    frequency = stats.get_recent_frequency(5)

    # Last 5 spins are:
    # 14, 0, 27, 7, 12

    assert frequency[14] == 1
    assert frequency[0] == 1
    assert frequency[27] == 1
    assert frequency[7] == 1
    assert frequency[12] == 1

    assert frequency[31] == 0

    assert len(frequency) == 37


def test_recent_frequency_window_larger_than_history():
    spins = [
        12, 7, 31, 4, 18,
    ]

    stats = RouletteStatistics(spins)

    frequency = stats.get_recent_frequency(10)

    assert frequency[12] == 1
    assert frequency[7] == 1
    assert frequency[31] == 1
    assert frequency[4] == 1
    assert frequency[18] == 1


def test_recent_frequency_invalid_window():
    stats = RouletteStatistics([12, 7, 31])

    try:
        stats.get_recent_frequency(0)
        assert False
    except ValueError as error:
        assert str(error) == "Window must be a positive integer."