from .base import BaseLogic


class UnitLogic(BaseLogic):
    def __init__(self, unit_class, permission_class, session):
        super(UnitLogic, self).__init__(unit_class, session)
        self.Unit = self.Cls
        self.Permission = permission_class

    def is_unit_in_db(self, unit_name):
        return self.session.query(self.Cls).filter(self.Cls.name == unit_name).first() is not None

    def add_to_db(self, unit_name):
        unit = self.Cls(name=unit_name)
        self.session.add(unit)
        self.session.commit()
        return unit

    def create_unit(self, **kwargs):
        unit = self.Unit(name=kwargs['name'])
        permission_ids = kwargs.get('permission_ids') or []
        permissions = self.session.query(self.Permission).filter(self.Permission.id.in_(permission_ids)).all() or []
        unit.permissions.extend(permissions)
        unit.perms_all_required = kwargs.get('perms_all_required') or False

        self.session.add(unit)
        self.session.commit()

        return unit

    def update_unit(self, unit, **kwargs):
        if 'name' in kwargs:
            unit.name = kwargs['name']
        if 'perms_all_required' in kwargs:
            unit.perms_all_required = kwargs['perms_all_required']
        if 'update_permissions' in kwargs and kwargs['update_permissions'] and 'permission_ids' in kwargs:
            new_perm_ids = kwargs['permission_ids'] or []
            old_perms = set(unit.permissions)
            new_perms = set(self.session.query(self.Permission).filter(self.Permission.id.in_(new_perm_ids)).all())
            unit.permissions.extend(new_perms - old_perms)
            for perm in old_perms - new_perms:
                unit.permissions.remove(perm)

        self.session.add(unit)
        self.session.commit()
