class DatabaseException(Exception):
    """Base exception for database errors"""

    pass


class DatabaseQueryError(DatabaseException):
    """Raised when a query on the database fails"""

    pass


class DatabaseIntegrityError(DatabaseException):
    """Raised when the database throws an integrity error"""

    pass
