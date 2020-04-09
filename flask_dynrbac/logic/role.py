from .base import BaseLogic


class RoleLogic(BaseLogic):
    def __init__(self, role_class, session):
        super(RoleLogic, self).__init__(role_class, session)
