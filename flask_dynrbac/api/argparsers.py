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
unit_update_parser.add_argument('name', type=str, help='Unit name', location='json', store_missing=False)
unit_update_parser.add_argument('update_permissions', type=bool, help='Whether to update permissions or not',
                                location='json', default=False)
unit_update_parser.add_argument('permission_ids', type=list, help='Unit permission IDs', location='json',
                                store_missing=False)
unit_update_parser.add_argument('perms_all_required', type=bool, help='Are all permissions required to access unit',
                                location='json', store_missing=False)

permission_create_parser = reqparse.RequestParser()
permission_create_parser.add_argument('name', type=str, help='Permission name', location='json')
permission_create_parser.add_argument('unit_ids', type=list, help='Permission unit IDs', location='json')
permission_create_parser.add_argument('role_ids', type=list, help='Permission role IDs', location='json')

permission_update_parser = reqparse.RequestParser()
permission_update_parser.add_argument('name', type=str, help='Permission name', location='json', store_missing=False)
permission_update_parser.add_argument('update_roles', type=bool, help='Whether to update roles or not',
                                      location='json', default=False)
permission_update_parser.add_argument('role_ids', type=list, help='Permission roles IDs', location='json',
                                      store_missing=False)
permission_update_parser.add_argument('update_units', type=bool, help='Whether to update units or not',
                                      location='json', default=False)
permission_update_parser.add_argument('unit_ids', type=list, help='Permission unit IDs', location='json',
                                      store_missing=False)

role_create_parser = reqparse.RequestParser()
role_create_parser.add_argument('name', type=str, help='Role name', location='json')
role_create_parser.add_argument('permission_ids', type=list, help='Role permission IDs', location='json')
role_create_parser.add_argument('parent_ids', type=list, help='Parent role IDs', location='json')
role_create_parser.add_argument('child_ids', type=list, help='Child role IDs', location='json')
role_create_parser.add_argument('incompatible_ids', type=list, help='Incompatible role IDs', location='json')
role_create_parser.add_argument('user_ids', type=list, help='Role user IDs', location='json')

role_update_parser = reqparse.RequestParser()
role_update_parser.add_argument('name', type=str, help='Role name', location='json')
role_update_parser.add_argument('update_permissions', type=bool, help='Whether to update permissions or not',
                                location='json', default=False)
role_update_parser.add_argument('update_parents', type=bool, help='Whether to update parents or not', location='json',
                                default=False)
role_update_parser.add_argument('update_children', type=bool, help='Whether to update children or not', location='json',
                                default=False)
role_update_parser.add_argument('update_users', type=bool, help='Whether to update users or not', location='json',
                                default=False)
role_update_parser.add_argument('update_incompatible', type=bool, help='Whether to update incompatible roles or not',
                                location='json', default=False)
role_update_parser.add_argument('permission_ids', type=list, help='Role permission IDs', location='json',
                                store_missing=False)
role_update_parser.add_argument('parent_ids', type=list, help='Parent role IDs', location='json',
                                store_missing=False)
role_update_parser.add_argument('child_ids', type=list, help='Child role IDs', location='json',
                                store_missing=False)
role_update_parser.add_argument('incompatible_ids', type=list, help='Incompatible role IDs', location='json',
                                store_missing=False)
role_update_parser.add_argument('user_ids', type=list, help='Role user IDs', location='json',
                                store_missing=False)
