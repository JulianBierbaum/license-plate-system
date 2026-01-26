class DatabaseError(Exception):
    """Base Database Exception"""

    pass


class DatabaseQueryError(DatabaseError):
    """Raised when a query on the database fails"""

    pass


class DatabaseIntegrityError(DatabaseError):
    """Raised when the database throws an integrity error"""

    pass


class DuplicateEntryError(DatabaseError):
    """Raised when an entry with the same name is already in the db"""

    pass


class MissingEntryError(DatabaseError):
    """Raised when an entry is not found"""

    pass
