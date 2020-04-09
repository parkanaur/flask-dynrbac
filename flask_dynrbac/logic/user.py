from .base import BaseLogic


class UserLogic(BaseLogic):
    def __init__(self, user_class, session):
        super(UserLogic, self).__init__(user_class, session)
