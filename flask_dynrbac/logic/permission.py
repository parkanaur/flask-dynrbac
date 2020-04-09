from .base import BaseLogic


class PermissionLogic(BaseLogic):
    def __init__(self, permission_class, session):
        super(PermissionLogic, self).__init__(permission_class, session)
