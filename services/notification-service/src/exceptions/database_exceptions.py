class DatabaseQueryError(Exception):
    """Raised when a query on the database fails"""

    pass


class DatabaseIntegrityError(Exception):
    """Raised when the database throws an integrity error"""

    pass
