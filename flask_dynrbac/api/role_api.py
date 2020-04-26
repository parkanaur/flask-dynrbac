from flask_restful import Resource


class RoleApi(Resource):
    def get(self, id):
        return 'get_role'

    def put(self, id):
        return 'put_role'

    def delete(self, id):
        return 'delete_role'


class RoleListApi(Resource):
    def get(self):
        return 'get_role_list'

    def post(self):
        return 'post_role_list'
