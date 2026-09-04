from app.database_service import (
    DatabaseService,
)


def get_database_service() -> type[DatabaseService]:
    return DatabaseService