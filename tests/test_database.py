import os

import pytest

from app.database import DatabaseConfig


def test_database_url_missing(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)

    with pytest.raises(
        ValueError,
        match="DATABASE_URL environment variable is not configured.",
    ):
        DatabaseConfig.get_database_url()


def test_database_url_available(monkeypatch):
    test_url = (
        "postgresql://user:password@localhost/"
        "roulette_ai?sslmode=require"
    )

    monkeypatch.setenv("DATABASE_URL", test_url)

    assert DatabaseConfig.get_database_url() == test_url