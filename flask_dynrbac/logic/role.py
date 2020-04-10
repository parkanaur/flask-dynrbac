from .base import BaseLogic
from flask_dynrbac.exc import DynRBACNotFoundException


class RoleLogic(BaseLogic):
    def __init__(self, role_class, session):
        super(RoleLogic, self).__init__(role_class, session)

    def get_all_users_for_role(self, role_name):
        role = self.session.query(self.Cls).filter(self.Cls.name == role_name).first()
        if role is None:
            raise DynRBACNotFoundException('Entity {entity} with ID {id} has not been found.'
                                           .format(entity=self.Cls.__name__, id=id))
        return role.users
