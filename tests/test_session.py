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