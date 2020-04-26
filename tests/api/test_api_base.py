from flask_dynrbac.api import generate_rbac_api
from helpers import send_request, send_and_assert


def test_api_urls(app):
    api = generate_rbac_api(app)

    send_and_assert(app, '/api/rbac/users', exp_string=b'get_user_list')
    send_and_assert(app, '/api/rbac/units/14', 'put', exp_string=b'put_unit')
    send_and_assert(app, '/api/rbac/permissions', 'post', exp_string=b'post_permission_list')
    send_and_assert(app, '/api/rbac/roles/16', 'delete', exp_string=b'delete_role')


def test_api_custom_url_prefix(app, rbac):
    api = generate_rbac_api(app, url_prefix='/custom_api/custom_rbac/')

    send_and_assert(app, '/custom_api/custom_rbac/users', exp_string=b'get_user_list')
    send_and_assert(app, '/custom_api/custom_rbac/units/14', 'put', exp_string=b'put_unit')
    send_and_assert(app, '/custom_api/custom_rbac/permissions', 'post', exp_string=b'post_permission_list')
    send_and_assert(app, '/custom_api/custom_rbac/roles/16', 'delete', exp_string=b'delete_role')
