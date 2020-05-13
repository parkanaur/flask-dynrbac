from .permission_api import PermissionApi, PermissionListApi
from .role_api import RoleApi, RoleListApi
from .unit_api import UnitApi, UnitListApi
from .user_api import UserApi, UserListApi

from flask_restful import Api


def generate_rbac_api(app, url_prefix='/api/rbac'):
    """Adds API routes to the provided app. The routes will be available
    under the supplied URL prefix (defaults to '/api/rbac').
    E.g.: `127.0.0.1/api/rbac/permissions`, or `127.0.0.1/api/rbac/users/<id>`

    :param app: Flask app
    :param url_prefix: URL prefix for API
    """
    api = Api(app)

    url_prefix = url_prefix.rstrip('/')

    api.add_resource(PermissionApi, url_prefix + '/permissions/<id>')
    api.add_resource(PermissionListApi, url_prefix + '/permissions')

    api.add_resource(RoleApi, url_prefix + '/roles/<id>')
    api.add_resource(RoleListApi, url_prefix + '/roles')

    api.add_resource(UserApi, url_prefix + '/users/<id>')
    api.add_resource(UserListApi, url_prefix + '/users')

    api.add_resource(UnitApi, url_prefix + '/units/<id>')
    api.add_resource(UnitListApi, url_prefix + '/units')

    return api
