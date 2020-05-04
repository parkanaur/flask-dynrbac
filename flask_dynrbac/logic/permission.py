from .base import BaseLogic


class PermissionLogic(BaseLogic):
    def __init__(self, permission_class, role_class, unit_class, session):
        super(PermissionLogic, self).__init__(permission_class, session)
        self.Permission = permission_class
        self.Role = role_class
        self.Unit = unit_class

    def create_permission(self, **kwargs):
        perm = self.Permission(name=kwargs['name'])

        unit_ids = kwargs.get('unit_ids') or []
        units = self.session.query(self.Unit).filter(self.Unit.id.in_(unit_ids)).all() or []
        perm.units.extend(units)

        role_ids = kwargs.get('role_ids') or []
        roles = self.session.query(self.Role).filter(self.Role.id.in_(role_ids)).all() or []
        perm.roles.extend(roles)

        self.session.add(perm)
        self.session.commit()

        return perm

    def update_permission(self, permission, **kwargs):
        if 'name' in kwargs:
            permission.name = kwargs['name']

        if 'update_units' in kwargs and kwargs['update_units'] and 'unit_ids' in kwargs:
            new_unit_ids = kwargs['unit_ids'] or []
            old_units = set(permission.units)
            new_units = set(self.session.query(self.Unit).filter(self.Unit.id.in_(new_unit_ids)).all())
            permission.units.extend(new_units - old_units)
            for unit in old_units - new_units:
                permission.units.remove(unit)

        if 'update_roles' in kwargs and kwargs['update_roles'] and 'role_ids' in kwargs:
            new_role_ids = kwargs['role_ids'] or []
            old_roles = set(permission.roles)
            new_roles = set(self.session.query(self.Role).filter(self.Role.id.in_(new_role_ids)).all())
            permission.roles.extend(new_roles - old_roles)
            for role in old_roles - new_roles:
                permission.roles.remove(role)

        self.session.add(permission)
        self.session.commit()
