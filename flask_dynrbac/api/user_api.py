from flask_restful import Resource, abort
from flask import current_app

from flask_dynrbac.exc import DynRBACNotFoundException
from flask_dynrbac.api.argparsers import user_update_parser, user_create_parser


def _logic():
    return current_app.rbac.user_logic


class UserApi(Resource):
    def _get_or_abort(self, id):
        try:
            return _logic().get_by_id(id)
        except DynRBACNotFoundException:
            return abort(404)

    def get(self, id):
        return self._get_or_abort(id).to_dict()

    def put(self, id):
        kw = user_update_parser.parse_args(strict=True)
        user = self._get_or_abort(id)

        _logic().update_user(user, **kw)

        return '', 204

    def delete(self, id):
        user = self._get_or_abort(id)
        _logic().delete(user)

        return '', 204


class UserListApi(Resource):
    def get(self):
        return [user.to_dict() for user in _logic().get_all()]

    def post(self):
        kw = user_create_parser.parse_args(strict=True)
        user = _logic().create_user(**kw)
        return user.to_dict()
