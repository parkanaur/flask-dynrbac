class BaseLogic(object):
    def __init__(self, cls, session):
        self.Cls = cls
        self.session = session

    def get_all(self):
        return self.session.query(self.Cls).all()

    def get_by_id(self, id):
        return self.session.query(self.Cls).filter(self.Cls.id == id).first()

