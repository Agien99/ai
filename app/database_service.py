from typing import Any

from app.database import DatabaseConfig


class DatabaseService:
    @staticmethod
    def execute(
        query: str,
        params: tuple | None = None,
    ) -> None:
        with DatabaseConfig.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, params)

            connection.commit()

    @staticmethod
    def execute_returning_one(
        query: str,
        params: tuple | None = None,
    ) -> dict[str, Any] | None:
        with DatabaseConfig.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, params)

                if cursor.description is None:
                    return None

                row = cursor.fetchone()

                if row is None:
                    return None

                columns = [
                    description.name
                    for description in cursor.description
                ]

                return dict(zip(columns, row))

    @staticmethod
    def fetch_one(
        query: str,
        params: tuple | None = None,
    ) -> dict[str, Any] | None:
        with DatabaseConfig.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, params)

                row = cursor.fetchone()

                if row is None:
                    return None

                columns = [
                    description.name
                    for description in cursor.description
                ]

                return dict(zip(columns, row))

    @staticmethod
    def fetch_all(
        query: str,
        params: tuple | None = None,
    ) -> list[dict[str, Any]]:
        with DatabaseConfig.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, params)

                rows = cursor.fetchall()

                columns = [
                    description.name
                    for description in cursor.description
                ]

                return [
                    dict(zip(columns, row))
                    for row in rows
                ]