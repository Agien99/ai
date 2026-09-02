from app.session import RouletteSession


def test_new_session_creation():
    session = RouletteSession()

    assert session.session_id is not None
    assert session.status == "NEW"

    assert session.initial_spins == []
    assert session.spins == []

    assert session.started_at is not None
    assert session.ended_at is None

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