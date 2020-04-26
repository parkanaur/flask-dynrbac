from flask_restful import Resource
from flask import current_app, jsonify


class PermissionApi(Resource):
    def get(self, id):
        return 'get_permission'

    def put(self, id):
        return 'put_permission'

    def delete(self, id):
        return 'delete_permission'


class PermissionListApi(Resource):
    def get(self):
        return 'get_permission_list'

    def post(self):
        return 'post_permission_list'
