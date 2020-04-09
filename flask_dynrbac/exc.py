class DynRBACInitWarning(Warning):
    """Custom warning which is thrown during initialization if SQLAlchemy is not initialized or Role/Permission/
    User classes are not supplied."""
    pass


class DynRBACNotFoundException(Exception):
    """Custom exception which is thrown when some object with the given ID is not found in the database."""
    pass
