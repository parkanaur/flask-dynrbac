class SQLAlchemyNotSuppliedWarning(Warning):
    """Custom warning which is thrown when Flask-SQLAlchemy is not initialized before DynRBAC"""
    def __init__(self, message):
        super(SQLAlchemyNotSuppliedWarning, self).__init__(message)
