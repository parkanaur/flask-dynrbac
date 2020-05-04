from flask_restful import Resource, abort
from flask import current_app

from flask_dynrbac.exc import DynRBACNotFoundException
from flask_dynrbac.api.argparsers import permission_create_parser, permission_update_parser


def _logic():
    return current_app.rbac.permission_logic


class PermissionApi(Resource):
    def _get_or_abort(self, id):
        try:
            return _logic().get_by_id(id)
        except DynRBACNotFoundException:
            return abort(404)

    def get(self, id):
        return self._get_or_abort(id).to_dict()

    def put(self, id):
        kw = permission_update_parser.parse_args(strict=True)
        permission = self._get_or_abort(id)

        _logic().update_permission(permission, **kw)

        return '', 204

    def delete(self, id):
        permission = self._get_or_abort(id)
        _logic().delete(permission)

        return '', 204


class PermissionListApi(Resource):
    def get(self):
        return [permission.to_dict() for permission in _logic().get_all()]

    def post(self):
        kw = permission_create_parser.parse_args(strict=True)
        permission = _logic().create_permission(**kw)
        return permission.to_dict()
