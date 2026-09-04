from unittest.mock import MagicMock

from app.database_service import DatabaseService


def create_mock_connection():
    connection = MagicMock()
    cursor = MagicMock()

    connection.__enter__.return_value = connection
    connection.cursor.return_value.__enter__.return_value = cursor

    return connection, cursor


def test_execute(monkeypatch):
    connection, cursor = create_mock_connection()

    monkeypatch.setattr(
        "app.database_service.DatabaseConfig.get_connection",
        lambda: connection,
    )

    DatabaseService.execute(
        "update sessions set status = %s where session_id = %s",
        ("ACTIVE", "session-1"),
    )

    cursor.execute.assert_called_once_with(
        "update sessions set status = %s where session_id = %s",
        ("ACTIVE", "session-1"),
    )

    connection.commit.assert_called_once()


def test_fetch_one(monkeypatch):
    connection, cursor = create_mock_connection()

    cursor.description = [
        MagicMock(name="session_id"),
        MagicMock(name="status"),
    ]

    cursor.description[0].name = "session_id"
    cursor.description[1].name = "status"

    cursor.fetchone.return_value = (
        "session-1",
        "ACTIVE",
    )

    monkeypatch.setattr(
        "app.database_service.DatabaseConfig.get_connection",
        lambda: connection,
    )

    result = DatabaseService.fetch_one(
        "select session_id, status from sessions where session_id = %s",
        ("session-1",),
    )

    assert result == {
        "session_id": "session-1",
        "status": "ACTIVE",
    }


def test_fetch_one_returns_none(monkeypatch):
    connection, cursor = create_mock_connection()

    cursor.fetchone.return_value = None

    monkeypatch.setattr(
        "app.database_service.DatabaseConfig.get_connection",
        lambda: connection,
    )

    result = DatabaseService.fetch_one(
        "select * from sessions where session_id = %s",
        ("missing",),
    )

    assert result is None


def test_fetch_all(monkeypatch):
    connection, cursor = create_mock_connection()

    cursor.description = [
        MagicMock(name="spin_index"),
        MagicMock(name="number"),
    ]

    cursor.description[0].name = "spin_index"
    cursor.description[1].name = "number"

    cursor.fetchall.return_value = [
        (1, 17),
        (2, 7),
    ]

    monkeypatch.setattr(
        "app.database_service.DatabaseConfig.get_connection",
        lambda: connection,
    )

    result = DatabaseService.fetch_all(
        "select spin_index, number from spins",
    )

    assert result == [
        {
            "spin_index": 1,
            "number": 17,
        },
        {
            "spin_index": 2,
            "number": 7,
        },
    ]