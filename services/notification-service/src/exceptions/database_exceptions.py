class DatabaseQueryError(Exception):
    """Raised when a query on the database fails"""

    pass


class DatabaseIntegrityError(Exception):
    """Raised when the database throws an integrity error"""

    pass


class DuplicateEntryError(Exception):
    """Raised when an entry with the same name is already in the db"""

    pass


class MissingEntryError(Exception):
    """Raised when an entry is not found"""

    pass
