from .base import BaseLogic


class UnitLogic(BaseLogic):
    def __init__(self, unit_class, session):
        super(UnitLogic, self).__init__(unit_class, session)

    def is_unit_in_db(self, unit_name):
        return self.session.query(self.Cls).filter(self.Cls.name == unit_name).first() is not None

    def add_to_db(self, unit_name):
        unit = self.Cls(name=unit_name)
        self.session.add(unit)
        self.session.commit()
        return unit
