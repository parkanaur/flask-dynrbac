class DynRBACInitWarning(Warning):
    """Custom warning which is thrown during initialization if SQLAlchemy is not initialized or Role/Permission/
    User classes are not supplied."""
    pass
