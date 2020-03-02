from . import util

from functools import wraps


class DynRBAC(object):
    """Allows for dynamic role-based access control (RBAC)
    by means of providing a decorator for using on some endpoint/method to
    register it, as well as HTTP API and an optional web interface for
    role handling.

    :param app: Flask app
    :param global_error_code: HTTP error code to return in case of permission mismatch. Defaults to 401
    """

    def __init__(self, app=None, global_error_code=401):
        """Initializes, configures and binds the extension instance to an app"""
        self.app = app
        self.global_error_code = global_error_code

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Configures the extension to be used later.

        :param app: Flask app
        """
        self._validate_requirements(app)

        app.extensions['dynrbac'] = self

    def _validate_requirements(self, app):
        """ Checks whether the supplied app fulfills the extension/domain model requirements.
            Throws a warning if some requirement is not met."""

        if app.extensions.get('sqlalchemy') is None:
            raise util.SQLAlchemyNotSuppliedWarning('Flask-SQLAlchemy is not initialized before DynRBAC. '
                                                    'DynRBAC requires SQLAlchemy for role and permission data '
                                                    'management.')

    def rbac(self, unit_name=None, check_hierarchy=False, error_code=None):
        """ Restricts access to a function based on a role/permission list.
            The list is retrieved from the app's database.

            :param unit_name: Optional name for a unit for database storage. Defaults to func name
            :param check_hierarchy: Allows for recursive check of user roles' parents' permissions.
            :param error_code: HTTP status code to return in case of permission mismatch. Defaults to
                `self.global_error_code`
            """

        if error_code is None:
            error_code = self.global_error_code

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):

                unit = unit_name if unit_name is not None else func.__name__
                return func(*args, **kwargs)

            return wrapper

        return decorator
