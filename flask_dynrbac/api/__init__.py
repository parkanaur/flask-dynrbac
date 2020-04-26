from .permission_api import PermissionApi, PermissionListApi
from .role_api import RoleApi, RoleListApi
from .unit_api import UnitApi, UnitListApi
from .user_api import UserApi, UserListApi

from flask_restful import Api


def generate_rbac_api(app, url_prefix='/api/rbac'):
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
