from .base import BaseLogic
from flask_dynrbac.exc import DynRBACNotFoundException


class UserLogic(BaseLogic):
    def __init__(self, user_class, permission_class, role_class, unit_class, session):
        super(UserLogic, self).__init__(user_class, session)
        self.User = self.Cls
        self.Permission = permission_class
        self.Role = role_class
        self.Unit = unit_class

    def get_user_roles(self, user_id):
        user = self.get_by_id(user_id)
        return user.roles

    def get_user_permissions(self, user_id):
        roles = self.get_user_roles(user_id)


    def has_unit_permission(self, user_id, unit):


        unit = self.session.query()
