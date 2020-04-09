from flask_dynrbac.exc import DynRBACNotFoundException


class BaseLogic(object):
    def __init__(self, cls, session):
        self.Cls = cls
        self.session = session

    def get_all(self):
        return self.session.query(self.Cls).all()

    def get_by_id(self, id, raise_on_not_found=True):
        mdl = self.session.query(self.Cls).filter(self.Cls.id == id).first()
        if mdl is None and raise_on_not_found:
            raise DynRBACNotFoundException('Entity {entity} with ID {id} has not been found.'
                                           .format(entity=self.Cls.__class__.__name__, id=id))


