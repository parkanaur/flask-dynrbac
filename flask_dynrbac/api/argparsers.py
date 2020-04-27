from flask_restful import reqparse


user_create_parser = reqparse.RequestParser()
user_create_parser.add_argument('name', type=str, required=True, help='User name', location='json')
user_create_parser.add_argument('role_ids', type=list, required=True, help='User role IDs', location='json')


user_update_parser = reqparse.RequestParser()
user_update_parser.add_argument('name', type=str, help='User name', location='json', store_missing=False)
user_update_parser.add_argument('update_roles', type=bool, help='Whether to update roles or not', location='json',
                                store_missing=False)
user_update_parser.add_argument('role_ids', type=list, help='User role IDs', location='json',
                                store_missing=False)
