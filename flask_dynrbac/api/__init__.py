from .permission_blueprint import PermissionApi, PermissionListApi
from .role_blueprint import RoleApi, RoleListApi
from .unit_blueprint import UnitApi, UnitListApi
from .user_blueprint import UserApi, UserListApi

from flask_restful import Api

try:
    # py2
    import urlparse as _urlparse
except ImportError:
    import urllib.parse as _urlparse


def generate_rbac_api(app, url_prefix='/api/rbac'):
    api = Api(app)

    api.add_resource(PermissionApi, _urlparse.urljoin(url_prefix, '/permissions/<permission_id>'))
    api.add_resource(PermissionListApi, _urlparse.urljoin(url_prefix, '/permissions'))

    api.add_resource(RoleApi, _urlparse.urljoin(url_prefix, '/roles/<role_id>'))
    api.add_resource(RoleListApi, _urlparse.urljoin(url_prefix, '/roles'))

    api.add_resource(UserApi, _urlparse.urljoin(url_prefix, '/users/<user_id>'))
    api.add_resource(UserListApi, _urlparse.urljoin(url_prefix, '/users'))

    api.add_resource(UnitApi, _urlparse.urljoin(url_prefix, '/units/<unit_id>'))
    api.add_resource(UnitListApi, _urlparse.urljoin(url_prefix, '/units'))

    return api
