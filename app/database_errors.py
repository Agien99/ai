class DatabaseServiceError(Exception):
    """Base exception for database service errors."""


class DatabaseConnectionError(DatabaseServiceError):
    """Raised when the PostgreSQL connection fails."""


class DatabaseDuplicateError(DatabaseServiceError):
    """Raised when a unique constraint is violated."""


class DatabaseReferenceError(DatabaseServiceError):
    """Raised when a foreign key constraint is violated."""


class DatabaseValidationError(DatabaseServiceError):
    """Raised when a database check constraint is violated."""