from flask_restful import Resource, abort
from flask import current_app

from flask_dynrbac.exc import DynRBACNotFoundException
from flask_dynrbac.api.argparsers import role_update_parser, role_create_parser


def _logic():
    return current_app.rbac.role_logic


class RoleApi(Resource):
    def _get_or_abort(self, id):
        try:
            return _logic().get_by_id(id)
        except DynRBACNotFoundException:
            return abort(404)

    def get(self, id):
        return self._get_or_abort(id).to_dict()

    def put(self, id):
        kw = role_update_parser.parse_args(strict=True)
        role = self._get_or_abort(id)

        _logic().update_role(role, **kw)

        return '', 204

    def delete(self, id):
        role = self._get_or_abort(id)
        _logic().delete(role)

        return '', 204


class RoleListApi(Resource):
    def get(self):
        return [role.to_dict() for role in _logic().get_all()]

    def post(self):
        kw = role_create_parser.parse_args(strict=True)
        role = _logic().create_role(**kw)
        return role.to_dict()
