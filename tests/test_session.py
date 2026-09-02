from app.session import RouletteSession


def test_new_session_creation():
    session = RouletteSession()

    assert session.session_id is not None
    assert session.status == "NEW"

    assert session.initial_spins == []
    assert session.spins == []

    assert session.started_at is not None
    assert session.ended_at is None