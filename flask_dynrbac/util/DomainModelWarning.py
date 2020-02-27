class DomainModelWarning(Warning):
    """Custom warning which is thrown when some domain model class is missing or incorrectly defined"""
    def __init__(self, message):
        super(DomainModelWarning, self).__init__(message)
