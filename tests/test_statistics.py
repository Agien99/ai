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

def test_dozen_frequency():
    spins = [
        1, 7, 12,
        13, 18, 24,
        25, 31, 36,
        0,
        5,
    ]

    stats = RouletteStatistics(spins)

    frequency = stats.get_dozen_frequency()

    assert frequency["dozen_1"] == 4
    assert frequency["dozen_2"] == 3
    assert frequency["dozen_3"] == 3
    assert frequency["zero"] == 1

def test_dozen_frequency_empty_history():
    stats = RouletteStatistics([])

    frequency = stats.get_dozen_frequency()

    assert frequency == {
        "dozen_1": 0,
        "dozen_2": 0,
        "dozen_3": 0,
        "zero": 0,
    }

def test_column_frequency():
    spins = [
        1, 4, 7,
        2, 5, 8,
        3, 6, 9,
        0,
        34, 35, 36,
    ]

    stats = RouletteStatistics(spins)

    frequency = stats.get_column_frequency()

    assert frequency["column_1"] == 4
    assert frequency["column_2"] == 4
    assert frequency["column_3"] == 4
    assert frequency["zero"] == 1

def test_column_frequency_empty_history():
    stats = RouletteStatistics([])

    frequency = stats.get_column_frequency()

    assert frequency == {
        "column_1": 0,
        "column_2": 0,
        "column_3": 0,
        "zero": 0,
    }

def test_street_activity():
    spins = [
        1, 2,
        5, 6, 6,
        17, 18,
        34,
        0,
    ]

    stats = RouletteStatistics(spins)

    activity = stats.get_street_activity()

    assert activity[(1, 2, 3)] == 2
    assert activity[(4, 5, 6)] == 3
    assert activity[(16, 17, 18)] == 2
    assert activity[(34, 35, 36)] == 1

    assert activity[(7, 8, 9)] == 0

    assert len(activity) == 12

def test_street_activity_empty_history():
    stats = RouletteStatistics([])

    activity = stats.get_street_activity()

    assert len(activity) == 12
    assert all(value == 0 for value in activity.values())

def test_split_activity():
    spins = [
        1,
        2,
        5,
        5,
        36,
        0,
    ]

    stats = RouletteStatistics(spins)

    activity = stats.get_split_activity()

    assert activity[(1, 2)] == 2
    assert activity[(1, 4)] == 1

    assert activity[(4, 5)] == 2
    assert activity[(5, 6)] == 2
    assert activity[(2, 5)] == 3
    assert activity[(5, 8)] == 2

    assert activity[(35, 36)] == 1
    assert activity[(33, 36)] == 1

    assert len(activity) == 57

def test_split_activity_empty_history():
    stats = RouletteStatistics([])

    activity = stats.get_split_activity()

    assert len(activity) == 57
    assert all(value == 0 for value in activity.values())

def test_corner_activity():
    spins = [
        1,
        2,
        5,
        5,
        6,
        36,
        0,
    ]

    stats = RouletteStatistics(spins)

    activity = stats.get_corner_activity()

    assert activity[(1, 2, 4, 5)] == 4
    assert activity[(2, 3, 5, 6)] == 4

    assert activity[(4, 5, 7, 8)] == 2
    assert activity[(5, 6, 8, 9)] == 3

    assert activity[(32, 33, 35, 36)] == 1

    assert len(activity) == 22

def test_corner_activity_empty_history():
    stats = RouletteStatistics([])

    activity = stats.get_corner_activity()

    assert len(activity) == 22
    assert all(value == 0 for value in activity.values())

def test_combined_statistics_summary():
    spins = [
        12, 7, 31, 4, 18,
        22, 7, 14, 0, 27,
        7, 12,
    ]

    stats = RouletteStatistics(spins)

    summary = stats.get_summary()

    assert summary["spin_count"] == 12

    assert "number_frequency" in summary
    assert "recent_frequency" in summary
    assert "spins_since_last_appearance" in summary
    assert "hot_numbers" in summary
    assert "cold_numbers" in summary
    assert "dozen_frequency" in summary
    assert "column_frequency" in summary
    assert "street_activity" in summary
    assert "split_activity" in summary
    assert "corner_activity" in summary

    assert summary["number_frequency"][7] == 3
    assert summary["number_frequency"][12] == 2

    assert len(summary["street_activity"]) == 12
    assert len(summary["split_activity"]) == 57
    assert len(summary["corner_activity"]) == 22

def test_summary_recent_windows():
    spins = [
        1, 2, 3, 4, 5,
        6, 7, 8, 9, 10,
    ]

    stats = RouletteStatistics(spins)

    summary = stats.get_summary()

    assert summary["recent_frequency"]["last_5"][6] == 1
    assert summary["recent_frequency"]["last_5"][10] == 1
    assert summary["recent_frequency"]["last_5"][1] == 0

    assert summary["recent_frequency"]["last_10"][1] == 1
    assert summary["recent_frequency"]["last_20"][1] == 1

def test_statistics_invalid_roulette_number():
    try:
        RouletteStatistics([1, 7, 37])
        assert False
    except ValueError as error:
        assert str(error) == (
            "Invalid roulette number at position 2: 37"
        )

def test_statistics_negative_number():
    try:
        RouletteStatistics([1, -1, 12])
        assert False
    except ValueError as error:
        assert str(error) == (
            "Invalid roulette number at position 1: -1"
        )

def test_statistics_non_integer_spin():
    try:
        RouletteStatistics([1, "7", 12])
        assert False
    except ValueError as error:
        assert str(error) == (
            "Invalid roulette number at position 1: 7"
        )

def test_statistics_history_must_be_list():
    try:
        RouletteStatistics((1, 7, 12))
        assert False
    except ValueError as error:
        assert str(error) == (
            "Spin history must be provided as a list."
        )

def test_empty_statistics_summary():
    stats = RouletteStatistics([])

    summary = stats.get_summary()

    assert summary["spin_count"] == 0

    assert all(
        value == 0
        for value in summary["number_frequency"].values()
    )

    assert all(
        value is None
        for value in summary[
            "spins_since_last_appearance"
        ].values()
    )

    assert summary["dozen_frequency"] == {
        "dozen_1": 0,
        "dozen_2": 0,
        "dozen_3": 0,
        "zero": 0,
    }

    assert summary["column_frequency"] == {
        "column_1": 0,
        "column_2": 0,
        "column_3": 0,
        "zero": 0,
    }

def test_full_statistics_engine():
    spins = [
        7, 12, 31, 4, 18,
        22, 7, 14, 0, 27,
        7, 12, 5, 6, 36,
    ]

    stats = RouletteStatistics(spins)

    summary = stats.get_summary()

    # Basic session statistics
    assert summary["spin_count"] == 15

    # Number frequency
    assert summary["number_frequency"][7] == 3
    assert summary["number_frequency"][12] == 2
    assert summary["number_frequency"][0] == 1

    # Recent frequency
    recent_5 = summary["recent_frequency"]["last_5"]

    # Last 5 spins:
    # 7, 12, 5, 6, 36
    assert recent_5[7] == 1
    assert recent_5[12] == 1
    assert recent_5[5] == 1
    assert recent_5[6] == 1
    assert recent_5[36] == 1

    # Spins since last appearance
    since_last = summary[
        "spins_since_last_appearance"
    ]

    assert since_last[36] == 0
    assert since_last[6] == 1
    assert since_last[5] == 2
    assert since_last[12] == 3
    assert since_last[7] == 4

    # Hot numbers
    assert summary["hot_numbers"][0] == (7, 3)
    assert summary["hot_numbers"][1] == (12, 2)

    # Dozens
    dozen_frequency = summary["dozen_frequency"]

    assert dozen_frequency["zero"] == 1
    assert sum(dozen_frequency.values()) == 15

    # Columns
    column_frequency = summary["column_frequency"]

    assert column_frequency["zero"] == 1
    assert sum(column_frequency.values()) == 15

    # Streets
    street_activity = summary["street_activity"]

    assert len(street_activity) == 12
    assert street_activity[(4, 5, 6)] == 3

    # Splits
    split_activity = summary["split_activity"]

    assert len(split_activity) == 57
    assert split_activity[(5, 6)] == 2

    # Corners
    corner_activity = summary["corner_activity"]

    assert len(corner_activity) == 22
    assert corner_activity[(4, 5, 7, 8)] == 5

def test_statistics_does_not_modify_original_history():
    spins = [1, 7, 12, 18]

    stats = RouletteStatistics(spins)

    spins.append(36)

    assert stats.spins == [1, 7, 12, 18]
    assert stats.get_number_frequency()[36] == 0