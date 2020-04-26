from flask_restful import Resource, abort, reqparse
from flask import current_app
from flask_dynrbac.exc import DynRBACNotFoundException


def _logic():
    return current_app.rbac.user_logic


_parser = reqparse.RequestParser()
_parser.add_argument('name', type=str, help='User name', location='json', store_missing=False)
_parser.add_argument('update_roles', type=bool, help='Whether to update roles or not', location='json',
                     store_missing=False)
_parser.add_argument('role_ids', type=list, help='User role IDs {error_msg}', location='json', store_missing=False)


class UserApi(Resource):
    def _get_or_abort(self, id):
        try:
            return _logic().get_by_id(id)
        except DynRBACNotFoundException:
            return abort(404)

    def get(self, id):
        return self._get_or_abort(id).to_dict()

    def put(self, id):
        kw = _parser.parse_args(strict=True)
        user = self._get_or_abort(id)

        _logic().update_user(user, **kw)

        return '', 204

    def delete(self, id):
        return '', 204


class UserListApi(Resource):
    def get(self):
        return [user.to_dict() for user in _logic().get_all()]

    def post(self):
        return 'post_user_list'
