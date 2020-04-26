from flask_restful import Resource
from flask import current_app


def _ul():
    return current_app.rbac.user_logic


class UserApi(Resource):
    def get(self, id):
        return 'get_user'

    def put(self, id):
        return 'put_user'

    def delete(self, id):
        return 'delete_user'


class UserListApi(Resource):
    def get(self):
        return [user.to_dict() for user in _ul().get_all()]

    def post(self):
        return 'post_user_list'
