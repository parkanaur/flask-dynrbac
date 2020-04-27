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
        permission_ids = kwargs['permission_ids'] or []
        permissions = self.session.query(self.Permission).filter(self.Permission.id.in_(permission_ids)).all()
        unit.permissions.extend(permissions)
        unit.perms_all_required = kwargs['perms_all_required']

        self.session.add(unit)
        self.session.commit()

        return unit
