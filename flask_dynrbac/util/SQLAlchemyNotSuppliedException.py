class SQLAlchemyNotSuppliedException(Exception):
    """Custom exception which is thrown when Flask-SQLAlchemy is not initialized before DynRBAC"""
    def __init__(self, message):
        super(SQLAlchemyNotSuppliedException, self).__init__(message)
