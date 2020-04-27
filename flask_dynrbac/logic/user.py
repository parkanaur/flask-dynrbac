from .base import BaseLogic
from flask_dynrbac.exc import DynRBACNotFoundException


class UserLogic(BaseLogic):
    def __init__(self, user_class, permission_class, role_class, unit_class, session, role_logic):
        super(UserLogic, self).__init__(user_class, session)
        self.User = self.Cls
        self.Permission = permission_class
        self.Role = role_class
        self.Unit = unit_class
        self._role_logic = role_logic

    def get_user_roles(self, user_id, with_children=True):
        user = self.get_by_id(user_id)
        roles = user.roles
        if with_children:
            for i in range(len(roles)):
                roles.extend(self._role_logic.get_whole_child_tree_inclusive(roles[i]))

        return roles

    def get_user_permissions(self, user_id, with_children=True):
        roles = self.get_user_roles(user_id, with_children)
        permissions = {}
        for role in roles:
            for perm in role.permissions:
                if perm.id in permissions:
                    continue
                permissions[perm.id] = perm

        return list(permissions.values())

    def has_unit_permission(self, user_id, unit, with_children=True):
        unit = self.session.query(self.Unit).filter(self.Unit.name == unit).first()
        user_perms = set(map(lambda perm: perm.name, self.get_user_permissions(user_id, with_children)))
        unit_perms = set(map(lambda perm: perm.name, unit.permissions))

        ok_perms = len(unit_perms.intersection(user_perms))

        if unit.perms_all_required:
            return ok_perms == len(unit_perms)
        else:
            return ok_perms >= 1

    def update_user(self, user, **kwargs):
        if 'name' in kwargs:
            user.name = kwargs['name']
        if 'update_roles' in kwargs and kwargs['update_roles'] and 'role_ids' in kwargs:
            new_role_ids = kwargs['role_ids'] or []
            old_roles = set(user.roles)
            new_roles = set(self.session.query(self.Role).filter(self.Role.id.in_(new_role_ids)).all())
            user.roles.extend(new_roles - old_roles)
            for role in old_roles - new_roles:
                user.roles.remove(role)
        self.session.add(user)
        self.session.commit()

    def create_user(self, **kwargs):
        user = self.User(name=kwargs['name'])
        role_ids = kwargs['role_ids'] or []
        roles = self.session.query(self.Role).filter(self.Role.id.in_(role_ids)).all()
        user.roles.extend(roles)

        self.session.add(user)
        self.session.commit()

        return user
