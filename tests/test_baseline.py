from app.baseline import RouletteBaselineEngine


TEST_SPINS = [
    7, 14, 21, 7, 8,
    17, 32, 7, 14, 5,
    26, 17, 8, 7, 30,
]


# =========================================================
# Step 1 - Baseline Engine
# =========================================================


def test_baseline_engine_creation():
    engine = RouletteBaselineEngine(TEST_SPINS)

    assert isinstance(
        engine,
        RouletteBaselineEngine,
    )

    assert engine.spins == TEST_SPINS
    assert engine.recent_window == 10


def test_baseline_engine_copies_spins():
    spins = TEST_SPINS.copy()

    engine = RouletteBaselineEngine(spins)

    spins.append(36)

    assert engine.spins != spins
    assert 36 not in engine.spins


def test_baseline_invalid_spin():
    try:
        RouletteBaselineEngine(
            [1, 2, 3, 37]
        )
        assert False

    except ValueError as error:
        assert "Invalid roulette number" in str(error)


def test_baseline_invalid_recent_window():
    try:
        RouletteBaselineEngine(
            TEST_SPINS,
            recent_window=0,
        )
        assert False

    except ValueError as error:
        assert str(error) == (
            "Recent window must be greater than 0."
        )


def test_recent_spins():
    engine = RouletteBaselineEngine(
        TEST_SPINS,
        recent_window=5,
    )

    assert engine._recent_spins() == (
        TEST_SPINS[-5:]
    )


# =========================================================
# Step 2 - Random Baseline
# =========================================================


def test_random_baseline_counts():
    engine = RouletteBaselineEngine(TEST_SPINS)

    predictions = (
        engine.generate_random_baseline(seed=42)
    )

    assert len(predictions["dozens"]) == 2
    assert len(predictions["columns"]) == 2
    assert len(predictions["streets"]) == 6
    assert len(predictions["splits"]) == 12
    assert len(predictions["corners"]) == 5


def test_random_baseline_no_duplicates():
    engine = RouletteBaselineEngine(TEST_SPINS)

    predictions = (
        engine.generate_random_baseline(seed=42)
    )

    dozens = [
        item["dozen"]
        for item in predictions["dozens"]
    ]

    columns = [
        item["column"]
        for item in predictions["columns"]
    ]

    streets = [
        item["street"]
        for item in predictions["streets"]
    ]

    splits = [
        item["split"]
        for item in predictions["splits"]
    ]

    corners = [
        item["corner"]
        for item in predictions["corners"]
    ]

    assert len(dozens) == len(set(dozens))
    assert len(columns) == len(set(columns))
    assert len(streets) == len(set(streets))
    assert len(splits) == len(set(splits))
    assert len(corners) == len(set(corners))


def test_random_baseline_same_seed_is_deterministic():
    engine = RouletteBaselineEngine(TEST_SPINS)

    first = engine.generate_random_baseline(
        seed=42
    )

    second = engine.generate_random_baseline(
        seed=42
    )

    assert first == second


# =========================================================
# Step 3 - Frequency Baseline
# =========================================================


def test_frequency_baseline_counts():
    engine = RouletteBaselineEngine(TEST_SPINS)

    predictions = (
        engine.generate_frequency_baseline()
    )

    assert len(predictions["dozens"]) == 2
    assert len(predictions["columns"]) == 2
    assert len(predictions["streets"]) == 6
    assert len(predictions["splits"]) == 12
    assert len(predictions["corners"]) == 5


def test_frequency_baseline_highest_frequency_first():
    spins = [
        1, 2, 3,
        1, 2, 3,
        1, 2, 3,
        20,
    ]

    engine = RouletteBaselineEngine(spins)

    predictions = (
        engine.generate_frequency_baseline()
    )

    assert predictions["dozens"][0]["dozen"] == 1

    assert (
        predictions["streets"][0]["street"]
        == (1, 2, 3)
    )


def test_frequency_baseline_contains_frequency():
    engine = RouletteBaselineEngine(TEST_SPINS)

    predictions = (
        engine.generate_frequency_baseline()
    )

    assert "frequency" in predictions["dozens"][0]
    assert "frequency" in predictions["columns"][0]
    assert "frequency" in predictions["streets"][0]
    assert "frequency" in predictions["splits"][0]
    assert "frequency" in predictions["corners"][0]


# =========================================================
# Step 4 - Hot Baseline
# =========================================================


def test_hot_baseline_counts():
    engine = RouletteBaselineEngine(
        TEST_SPINS,
        recent_window=5,
    )

    predictions = engine.generate_hot_baseline()

    assert len(predictions["dozens"]) == 2
    assert len(predictions["columns"]) == 2
    assert len(predictions["streets"]) == 6
    assert len(predictions["splits"]) == 12
    assert len(predictions["corners"]) == 5


def test_hot_baseline_uses_recent_window():
    spins = [
        1, 1, 1, 1, 1,
        1, 1, 1, 1, 1,
        25, 25, 25, 25, 25,
    ]

    engine = RouletteBaselineEngine(
        spins,
        recent_window=5,
    )

    predictions = engine.generate_hot_baseline()

    assert predictions["dozens"][0]["dozen"] == 3


# =========================================================
# Step 5 - Cold Baseline
# =========================================================


def test_cold_baseline_counts():
    engine = RouletteBaselineEngine(TEST_SPINS)

    predictions = (
        engine.generate_cold_baseline()
    )

    assert len(predictions["dozens"]) == 2
    assert len(predictions["columns"]) == 2
    assert len(predictions["streets"]) == 6
    assert len(predictions["splits"]) == 12
    assert len(predictions["corners"]) == 5


def test_cold_baseline_lowest_frequency_first():
    spins = [
        1, 2, 3,
        1, 2, 3,
        1, 2, 3,
        20,
    ]

    engine = RouletteBaselineEngine(spins)

    predictions = (
        engine.generate_cold_baseline()
    )

    predicted_dozens = [
        item["dozen"]
        for item in predictions["dozens"]
    ]

    assert 3 in predicted_dozens


def test_cold_baseline_frequency_is_lowest_first():
    engine = RouletteBaselineEngine(TEST_SPINS)

    predictions = (
        engine.generate_cold_baseline()
    )

    frequencies = [
        item["frequency"]
        for item in predictions["streets"]
    ]

    assert frequencies == sorted(frequencies)