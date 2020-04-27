from flask_restful import reqparse


user_create_parser = reqparse.RequestParser()
user_create_parser.add_argument('name', type=str, required=True, help='User name', location='json')
user_create_parser.add_argument('role_ids', type=list, help='User role IDs', location='json')


user_update_parser = reqparse.RequestParser()
user_update_parser.add_argument('name', type=str, help='User name', location='json', store_missing=False)
user_update_parser.add_argument('update_roles', type=bool, help='Whether to update roles or not', location='json',
                                default=False)
user_update_parser.add_argument('role_ids', type=list, help='User role IDs', location='json',
                                store_missing=False)


unit_create_parser = reqparse.RequestParser()
unit_create_parser.add_argument('name', type=str, required=True, help='Unit name', location='json')
unit_create_parser.add_argument('permission_ids', type=list, help='Unit permission IDs', location='json')
unit_create_parser.add_argument('perms_all_required', type=bool, help='Are all permissions required to access unit',
                                location='json', default=False)


unit_update_parser = reqparse.RequestParser()
unit_update_parser.add_argument('name', type=str, help='Unit name', location='json')
unit_update_parser.add_argument('update_permissions', type=bool, help='Whether to update permissions or not',
                                location='json', default=False)
unit_update_parser.add_argument('permission_ids', type=list, help='Unit permission IDs', location='json',
                                store_missing=False)
unit_update_parser.add_argument('perms_all_required', type=bool, help='Are all permissions required to access unit',
                                location='json', default=False)
