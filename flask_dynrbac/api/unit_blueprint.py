from flask_restful import Resource


class UnitApi(Resource):
    def get(self, id):
        return 'get_unit'

    def put(self, id):
        return 'put_unit'

    def delete(self, id):
        return 'delete_unit'


class UnitListApi(Resource):
    def get(self):
        return 'get_unit_list'

    def post(self):
        return 'post_unit_list'
