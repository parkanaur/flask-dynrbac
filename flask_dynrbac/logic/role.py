from .base import BaseLogic
from flask_dynrbac.exc import DynRBACNotFoundException


class RoleLogic(BaseLogic):
    def __init__(self, role_class, session):
        super(RoleLogic, self).__init__(role_class, session)

    def get_all_users_for_role(self, role_name):
        role = self.get_by_name(role_name)
        return role.users

    def get_all_permissions_for_role(self, role_name, with_children=True):
        role = self.get_by_name(role_name)
        roles = [role] if not with_children else self.get_whole_child_tree_inclusive(role)

        return

    def get_whole_child_tree_inclusive(self, role):
        children = [role]
        for r in role.children:
            children.extend(self.get_whole_child_tree_inclusive(r))

        return children
