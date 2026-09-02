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

def test_spins_since_last_appearance():
    spins = [
        12, 5, 17, 8, 31, 5, 22,
    ]

    stats = RouletteStatistics(spins)

    result = stats.get_spins_since_last_appearance()

    assert result[22] == 0
    assert result[5] == 1
    assert result[31] == 2
    assert result[8] == 3
    assert result[17] == 4
    assert result[12] == 6

    assert result[36] is None

    assert len(result) == 37

def test_hot_numbers():
    spins = [
        7, 12, 7, 31, 7,
        12, 18, 22, 12, 7,
    ]

    stats = RouletteStatistics(spins)

    hot = stats.get_hot_numbers(3)

    assert hot[0] == (7, 4)
    assert hot[1] == (12, 3)
    assert hot[2] == (18, 1)


def test_cold_numbers():
    spins = [
        7, 12, 7, 31, 7,
        12, 18, 22, 12, 7,
    ]

    stats = RouletteStatistics(spins)

    cold = stats.get_cold_numbers(3)

    assert cold == [
        (0, 0),
        (1, 0),
        (2, 0),
    ]


def test_hot_numbers_default_limit():
    stats = RouletteStatistics([
        7, 7, 7,
        12, 12,
        31,
    ])

    hot = stats.get_hot_numbers()

    assert len(hot) == 5
    assert hot[0] == (7, 3)
    assert hot[1] == (12, 2)


def test_hot_and_cold_invalid_limit():
    stats = RouletteStatistics([7, 12, 31])

    try:
        stats.get_hot_numbers(0)
        assert False
    except ValueError as error:
        assert str(error) == "Limit must be a positive integer."

    try:
        stats.get_cold_numbers(0)
        assert False
    except ValueError as error:
        assert str(error) == "Limit must be a positive integer."