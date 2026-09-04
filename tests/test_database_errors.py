import pytest
import psycopg

from app.database_errors import (
    DatabaseConnectionError,
    DatabaseDuplicateError,
    DatabaseReferenceError,
    DatabaseValidationError,
)
from app.database_service import (
    DatabaseService,
)


def test_unique_violation_translation():
    error = psycopg.errors.UniqueViolation()

    with pytest.raises(
        DatabaseDuplicateError
    ):
        DatabaseService._translate_database_error(
            error
        )


def test_foreign_key_violation_translation():
    error = (
        psycopg.errors.ForeignKeyViolation()
    )

    with pytest.raises(
        DatabaseReferenceError
    ):
        DatabaseService._translate_database_error(
            error
        )


def test_check_violation_translation():
    error = psycopg.errors.CheckViolation()

    with pytest.raises(
        DatabaseValidationError
    ):
        DatabaseService._translate_database_error(
            error
        )


def test_operational_error_translation():
    error = psycopg.OperationalError()

    with pytest.raises(
        DatabaseConnectionError
    ):
        DatabaseService._translate_database_error(
            error
        )