from app.session import RouletteSession


def test_new_session_creation():
    session = RouletteSession()

    assert session.session_id is not None
    assert session.status == "NEW"

    assert session.initial_spins == []
    assert session.spins == []

    assert session.started_at is not None
    assert session.ended_at is None


def test_start_session():
    session = RouletteSession()

    initial_spins = [
        12, 7, 31, 4, 18,
        22, 9, 14, 0, 27,
    ]

    session.start(initial_spins)

    assert session.status == "ACTIVE"
    assert session.initial_spins == initial_spins
    assert session.spins == initial_spins
    assert len(session.spins) == 10


def test_start_session_with_too_few_spins():
    session = RouletteSession()

    initial_spins = [12, 7, 31, 4, 18]

    try:
        session.start(initial_spins)
        assert False
    except ValueError as error:
        assert str(error) == "At least 10 previous spins are required."


def test_session_cannot_start_twice():
    session = RouletteSession()

    initial_spins = [
        12, 7, 31, 4, 18,
        22, 9, 14, 0, 27,
    ]

    session.start(initial_spins)

    try:
        session.start(initial_spins)
        assert False
    except ValueError as error:
        assert str(error) == "Session has already been started."


def test_add_spin_to_active_session():
    session = RouletteSession()

    initial_spins = [
        12, 7, 31, 4, 18,
        22, 9, 14, 0, 27,
    ]

    session.start(initial_spins)

    session.add_spin(17)

    assert len(session.spins) == 11
    assert session.spins[-1] == 17


def test_add_multiple_spins_sequentially():
    session = RouletteSession()

    initial_spins = [
        12, 7, 31, 4, 18,
        22, 9, 14, 0, 27,
    ]

    session.start(initial_spins)

    session.add_spin(17)
    session.add_spin(5)
    session.add_spin(29)

    assert session.spins[-3:] == [17, 5, 29]
    assert len(session.spins) == 13


def test_cannot_add_spin_before_session_started():
    session = RouletteSession()

    try:
        session.add_spin(17)
        assert False
    except ValueError as error:
        assert str(error) == (
            "Cannot add spin to a session that is not active."
        )


def test_cannot_add_invalid_spin():
    session = RouletteSession()

    initial_spins = [
        12, 7, 31, 4, 18,
        22, 9, 14, 0, 27,
    ]

    session.start(initial_spins)

    try:
        session.add_spin(40)
        assert False
    except ValueError as error:
        assert str(error) == "Invalid roulette number: 40"

def test_spin_sequence_order():
    session = RouletteSession()

    initial_spins = [
        12, 7, 31, 4, 18,
        22, 9, 14, 0, 27,
    ]

    session.start(initial_spins)

    session.add_spin(17)
    session.add_spin(5)
    session.add_spin(29)

    sequence = session.get_spin_sequence()

    assert sequence[0] == (1, 12)
    assert sequence[1] == (2, 7)
    assert sequence[9] == (10, 27)

    assert sequence[10] == (11, 17)
    assert sequence[11] == (12, 5)
    assert sequence[12] == (13, 29)

    assert len(sequence) == 13

def test_session_metadata():
    session = RouletteSession()

    initial_spins = [
        12, 7, 31, 4, 18,
        22, 9, 14, 0, 27,
    ]

    session.start(initial_spins)

    session.add_spin(17)
    session.add_spin(5)
    session.add_spin(29)

    metadata = session.get_metadata()

    assert metadata["session_id"] == session.session_id
    assert metadata["status"] == "ACTIVE"

    assert metadata["initial_spin_count"] == 10
    assert metadata["total_spin_count"] == 13
    assert metadata["new_spin_count"] == 3

    assert metadata["started_at"] == session.started_at
    assert metadata["ended_at"] is None

def test_end_active_session():
    session = RouletteSession()

    initial_spins = [
        12, 7, 31, 4, 18,
        22, 9, 14, 0, 27,
    ]

    session.start(initial_spins)

    session.end()

    assert session.status == "ENDED"
    assert session.ended_at is not None


def test_cannot_add_spin_after_session_ended():
    session = RouletteSession()

    initial_spins = [
        12, 7, 31, 4, 18,
        22, 9, 14, 0, 27,
    ]

    session.start(initial_spins)
    session.end()

    try:
        session.add_spin(17)
        assert False
    except ValueError as error:
        assert str(error) == (
            "Cannot add spin to a session that is not active."
        )


def test_cannot_end_new_session():
    session = RouletteSession()

    try:
        session.end()
        assert False
    except ValueError as error:
        assert str(error) == (
            "Cannot end a session that has not been started."
        )


def test_cannot_end_session_twice():
    session = RouletteSession()

    initial_spins = [
        12, 7, 31, 4, 18,
        22, 9, 14, 0, 27,
    ]

    session.start(initial_spins)
    session.end()

    try:
        session.end()
        assert False
    except ValueError as error:
        assert str(error) == "Session has already ended."

def test_new_session_is_independent_from_previous_session():
    session_a = RouletteSession()

    initial_spins_a = [
        12, 7, 31, 4, 18,
        22, 9, 14, 0, 27,
    ]

    session_a.start(initial_spins_a)

    session_a.add_spin(17)
    session_a.add_spin(5)

    session_a.end()

    session_b = RouletteSession()

    initial_spins_b = [
        3, 11, 26, 8, 19,
        32, 6, 15, 24, 1,
    ]

    session_b.start(initial_spins_b)

    assert session_a.session_id != session_b.session_id

    assert session_a.status == "ENDED"
    assert session_b.status == "ACTIVE"

    assert session_a.spins == [
        12, 7, 31, 4, 18,
        22, 9, 14, 0, 27,
        17, 5,
    ]

    assert session_b.spins == initial_spins_b

    assert 17 not in session_b.spins
    assert 5 not in session_b.spins

def test_start_session_with_invalid_number():
    session = RouletteSession()

    initial_spins = [
        12, 7, 31, 4, 18,
        22, 9, 14, 0, 40,
    ]

    try:
        session.start(initial_spins)
        assert False
    except ValueError as error:
        assert "Invalid roulette number" in str(error)


def test_start_session_with_non_integer():
    session = RouletteSession()

    initial_spins = [
        12, 7, 31, 4, 18,
        22, 9, 14, 0, "27",
    ]

    try:
        session.start(initial_spins)
        assert False
    except ValueError as error:
        assert "Invalid roulette number" in str(error)


def test_start_session_with_too_many_spins():
    session = RouletteSession()

    initial_spins = [
        1, 2, 3, 4, 5,
        6, 7, 8, 9, 10,
        11, 12, 13, 14, 15,
        16,
    ]

    try:
        session.start(initial_spins)
        assert False
    except ValueError as error:
        assert str(error) == "Maximum initial history is 15 spins."


def test_start_session_with_empty_history():
    session = RouletteSession()

    try:
        session.start([])
        assert False
    except ValueError as error:
        assert str(error) == "At least 10 previous spins are required."


def test_cannot_add_non_integer_spin():
    session = RouletteSession()

    initial_spins = [
        12, 7, 31, 4, 18,
        22, 9, 14, 0, 27,
    ]

    session.start(initial_spins)

    try:
        session.add_spin("17")
        assert False
    except ValueError as error:
        assert str(error) == "Invalid roulette number: 17"


def test_cannot_add_negative_spin():
    session = RouletteSession()

    initial_spins = [
        12, 7, 31, 4, 18,
        22, 9, 14, 0, 27,
    ]

    session.start(initial_spins)

    try:
        session.add_spin(-1)
        assert False
    except ValueError as error:
        assert str(error) == "Invalid roulette number: -1"


def test_metadata_after_session_ended():
    session = RouletteSession()

    initial_spins = [
        12, 7, 31, 4, 18,
        22, 9, 14, 0, 27,
    ]

    session.start(initial_spins)

    session.add_spin(17)
    session.add_spin(5)

    session.end()

    metadata = session.get_metadata()

    assert metadata["status"] == "ENDED"
    assert metadata["initial_spin_count"] == 10
    assert metadata["total_spin_count"] == 12
    assert metadata["new_spin_count"] == 2
    assert metadata["ended_at"] is not None

def test_full_session_lifecycle():
    session = RouletteSession()

    initial_spins = [
        12, 7, 31, 4, 18,
        22, 9, 14, 0, 27,
    ]

    # Start session
    session.start(initial_spins)

    assert session.status == "ACTIVE"
    assert len(session.spins) == 10

    # Add new observed spins
    session.add_spin(17)
    session.add_spin(5)
    session.add_spin(29)

    assert session.spins[-3:] == [17, 5, 29]
    assert len(session.spins) == 13

    # Check sequence
    sequence = session.get_spin_sequence()

    assert sequence[0] == (1, 12)
    assert sequence[-1] == (13, 29)

    # Check metadata
    metadata = session.get_metadata()

    assert metadata["status"] == "ACTIVE"
    assert metadata["initial_spin_count"] == 10
    assert metadata["total_spin_count"] == 13
    assert metadata["new_spin_count"] == 3

    # End session
    session.end()

    assert session.status == "ENDED"
    assert session.ended_at is not None

    # Metadata should update after ending
    metadata = session.get_metadata()

    assert metadata["status"] == "ENDED"
    assert metadata["ended_at"] is not None