from flask_dynrbac.exc import DynRBACNotFoundException


class BaseLogic(object):
    def __init__(self, cls, session):
        self.Cls = cls
        self.session = session

    def get_all(self):
        return self.session.query(self.Cls).all()

    def _get_and_check(self, id, raise_on_not_found):
        mdl = self.session.query(self.Cls).filter(self.Cls.id == id).first()
        if mdl is None and raise_on_not_found:
            raise DynRBACNotFoundException('Entity {entity} with ID {id} has not been found.'
                                           .format(entity=self.Cls.__name__, id=id))
        return mdl

    def get_by_id(self, id, raise_on_not_found=True):
        return self._get_and_check(id, raise_on_not_found)

    def get_by_name(self, name, raise_on_not_found=True):
        mdl = self.session.query(self.Cls).filter(self.Cls.name == name).first()
        if mdl is None and raise_on_not_found:
            raise DynRBACNotFoundException('Entity {entity} with name {name} has not been found.'
                                           .format(entity=self.Cls.__name__, name=name))

        return mdl

    def delete_by_id(self, id, raise_on_not_found=True):
        mdl = self._get_and_check(id, raise_on_not_found)

        self.session.delete(mdl)
        self.session.commit()

    def delete(self, object):
        self.session.delete(object)
        self.session.commit()
