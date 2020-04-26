from flask_restful import Resource


class UserApi(Resource):
    def get(self, id):
        return 'get_user'

    def put(self, id):
        return 'put_user'

    def delete(self, id):
        return 'delete_user'


class UserListApi(Resource):
    def get(self):
        return 'get_user_list'

    def post(self):
        return 'post_user_list'
