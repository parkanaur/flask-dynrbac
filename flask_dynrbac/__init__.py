from . import util


class DynRBAC(object):
    """Allows for dynamic role-based access control (RBAC)
    by means of providing a decorator for using on some endpoint/method to
    register it, as well as HTTP API and an optional web interface for
    role handling."""

    def __init__(self, app=None):
        self.app = app

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if app.extensions.get('sqlalchemy') is None:
            raise util.SQLAlchemyNotSuppliedWarning('Flask-SQLAlchemy is not initialized before DynRBAC. '
                                                    'DynRBAC requires SQLAlchemy for role and permission data '
                                                    'storage.')

    def rbac(self, func):
        pass
