from .base import BaseLogic
from flask_dynrbac.exc import DynRBACNotFoundException


class RoleLogic(BaseLogic):
    def __init__(self, role_class, user_class, permission_class, session):
        super(RoleLogic, self).__init__(role_class, session)
        self.Role = role_class
        self.User = user_class
        self.Permission = permission_class

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

    def update_role(self, role, **kwargs):
        if 'name' in kwargs:
            role.name = kwargs['name']

        if kwargs.get('update_users', False) and 'user_ids' in kwargs:
            new_user_ids = kwargs['user_ids'] or []
            old_users = set(role.users)
            new_users = set(self.session.query(self.User).filter(self.User.id.in_(new_user_ids)).all())
            role.users.extend(new_users - old_users)
            for user in old_users - new_users:
                role.users.remove(user)

        if kwargs.get('update_permissions', False) and 'permission_ids' in kwargs:
            new_perm_ids = kwargs['permission_ids'] or []
            old_permissions = set(role.permissions)
            new_permissions = set(self.session.query(self.Permission).filter(self.Permission.id.in_(new_perm_ids))
                                  .all())
            role.permissions.extend(new_permissions - old_permissions)
            for perm in old_permissions - new_permissions:
                role.permissions.remove(perm)

        if kwargs.get('update_parents', False) and 'parent_ids' in kwargs:
            new_parent_ids = kwargs['parent_ids'] or []
            old_parents = set(role.parents)
            new_parents = set(self.session.query(self.Role).filter(self.Role.id.in_(new_parent_ids)).all())
            role.parents.extend(new_parents - old_parents)
            for parent in old_parents - new_parents:
                role.parents.remove(parent)

        if kwargs.get('update_children', False) and 'child_ids' in kwargs:
            new_child_ids = kwargs['child_ids'] or []
            old_children = set(role.children)
            new_children = set(self.session.query(self.Role).filter(self.Role.id.in_(new_child_ids)).all())
            role.children.extend(new_children - old_children)
            for child in old_children - new_children:
                role.children.remove(child)

        if kwargs.get('update_incompatible', False) and 'incompatible_ids' in kwargs:
            new_incompatible_ids = kwargs['incompatible_ids'] or []
            old_incompatibles = set(role.incompatible_roles)
            new_incompatibles = set(self.session.query(self.Role).filter(self.Role.id.in_(new_incompatible_ids)).all())
            role.incompatible_roles.extend(new_incompatibles - old_incompatibles)
            for role in old_incompatibles - new_incompatibles:
                role.incompatible_roles.remove(role)

        self.session.add(role)
        self.session.commit()

    def create_role(self, **kwargs):
        role = self.Role(name=kwargs['name'])

        user_ids = kwargs['user_ids'] or []
        users = self.session.query(self.User).filter(self.User.id.in_(user_ids)).all()
        role.users.extend(users)

        permission_ids = kwargs['permission_ids'] or []
        permissions = self.session.query(self.Permission).filter(self.Permission.id.in_(permission_ids)).all()
        role.permissions.extend(permissions)

        parent_ids = kwargs['parent_ids'] or []
        parents = self.session.query(self.Role).filter(self.Role.id.in_(parent_ids)).all()
        role.parents.extend(parents)

        child_ids = kwargs['child_ids'] or []
        children = self.session.query(self.Role).filter(self.Role.id.in_(child_ids)).all()
        role.children.extend(children)

        incompatible_ids = kwargs['incompatible_ids'] or []
        incompatibles = self.session.query(self.Role).filter(self.Role.id.in_(incompatible_ids)).all()
        role.incompatible_roles.extend(incompatibles)

        self.session.add(role)
        self.session.commit()

        return role
