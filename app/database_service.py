from typing import Any

import psycopg
from psycopg.errors import (
    CheckViolation,
    ForeignKeyViolation,
    UniqueViolation,
)

from app.database import DatabaseConfig
from app.database_errors import (
    DatabaseConnectionError,
    DatabaseDuplicateError,
    DatabaseReferenceError,
    DatabaseValidationError,
)


class DatabaseService:
    @staticmethod
    def _translate_database_error(
        error: Exception,
    ) -> None:
        if isinstance(error, UniqueViolation):
            raise DatabaseDuplicateError(
                "Duplicate database record."
            ) from error

        if isinstance(error, ForeignKeyViolation):
            raise DatabaseReferenceError(
                "Referenced database record does not exist."
            ) from error

        if isinstance(error, CheckViolation):
            raise DatabaseValidationError(
                "Database validation constraint failed."
            ) from error

        if isinstance(error, psycopg.OperationalError):
            raise DatabaseConnectionError(
                "Unable to communicate with PostgreSQL."
            ) from error

        raise error

    @staticmethod
    def execute(
        query: str,
        params: tuple | None = None,
    ) -> None:
        try:
            with DatabaseConfig.get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        query,
                        params,
                    )

                connection.commit()

        except Exception as error:
            DatabaseService._translate_database_error(
                error
            )

    @staticmethod
    def execute_returning_one(
        query: str,
        params: tuple | None = None,
    ) -> dict[str, Any] | None:
        try:
            with DatabaseConfig.get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        query,
                        params,
                    )

                    if cursor.description is None:
                        return None

                    row = cursor.fetchone()

                    if row is None:
                        return None

                    columns = [
                        description.name
                        for description
                        in cursor.description
                    ]

                    return dict(
                        zip(
                            columns,
                            row,
                        )
                    )

        except Exception as error:
            DatabaseService._translate_database_error(
                error
            )

    @staticmethod
    def fetch_one(
        query: str,
        params: tuple | None = None,
    ) -> dict[str, Any] | None:
        try:
            with DatabaseConfig.get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        query,
                        params,
                    )

                    row = cursor.fetchone()

                    if row is None:
                        return None

                    columns = [
                        description.name
                        for description
                        in cursor.description
                    ]

                    return dict(
                        zip(
                            columns,
                            row,
                        )
                    )

        except Exception as error:
            DatabaseService._translate_database_error(
                error
            )

    @staticmethod
    def fetch_all(
        query: str,
        params: tuple | None = None,
    ) -> list[dict[str, Any]]:
        try:
            with DatabaseConfig.get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        query,
                        params,
                    )

                    rows = cursor.fetchall()

                    columns = [
                        description.name
                        for description
                        in cursor.description
                    ]

                    return [
                        dict(
                            zip(
                                columns,
                                row,
                            )
                        )
                        for row in rows
                    ]

        except Exception as error:
            DatabaseService._translate_database_error(
                error
            )