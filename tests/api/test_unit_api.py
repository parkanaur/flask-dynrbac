from helpers import send_and_assert, send_request


def test_get_list(sample_filled_app, api_url):
    app, db, rbac, dmg = sample_filled_app

    units = send_request(app, api_url + '/units').get_json()
    assert len(units) == 5
    for unit in units:
        assert 'name' in unit
        assert 'id' in unit
        assert 'permissions' in unit
        assert len(unit['permissions']) >= 1


def test_get_unit(sample_filled_app, api_url):
    app, db, rbac, dmg = sample_filled_app

    r = send_request(app, api_url + '/units/1')
    assert r.status_code == 200, 'GOT ' + str(r.status_code)
    unit = r.get_json()
    assert 'name' in unit
    assert 'id' in unit
    assert unit['id'] == 1
    assert 'permissions' in unit
    assert len(unit['permissions']) >= 1


# def test_put_user(sample_filled_app, api_url):
#     app, db, rbac, dmg = sample_filled_app
#
#     r = send_request(app, api_url + '/users/2', method='put', json={
#         'name': 'user_new_2',
#         'update_roles': True,
#         'role_ids': [1, 2, 3, 4]
#     })
#     assert r.status_code == 204, 'GOT ' + str(r.status_code) + ' ' + r.data
#
#     r = send_request(app, api_url + '/users/2')
#     assert r.status_code == 200, 'GOT ' + str(r.status_code)
#     user = r.get_json()
#     assert user['name'] == 'user_new_2'
#     for role in user['roles']:
#         assert role['id'] in [1, 2, 3, 4]
#
#     r = send_request(app, api_url + '/users/2', method='put', json={
#         'update_roles': False,
#         'role_ids': [1]
#     })
#
#     r = send_request(app, api_url + '/users/2')
#     user = r.get_json()
#     assert user['name'] == 'user_new_2'
#     assert len(user['roles']) == 4
#     for role in user['roles']:
#         assert role['id'] in [1, 2, 3, 4]
#
#     r = send_request(app, api_url + '/users/2', method='put', json={
#         'update_roles': True,
#         'role_ids': [1, 4]
#     })
#
#     r = send_request(app, api_url + '/users/2')
#     user = r.get_json()
#     assert len(user['roles']) == 2
#     for role in user['roles']:
#         assert role['id'] in [1, 4]
#
#
# def test_delete_user(sample_filled_app, api_url):
#     app, db, rbac, dmg = sample_filled_app
#
#     r = send_request(app, api_url + '/users/2', method='delete')
#     assert r.status_code == 204, 'GOT ' + str(r.status_code) + ' ' + r.data
#
#     r = send_request(app, api_url + '/users/2')
#     assert r.status_code == 404, 'GOT ' + str(r.status_code) + ' ' + r.data
#
#
# def test_create_user(sample_filled_app, api_url):
#     app, db, rbac, dmg = sample_filled_app
#
#     r = send_request(app, api_url + '/users', method='post', json={
#         'name': 'new_user_create',
#         'role_ids': [1, 2, 3]
#     })
#     assert r.status_code == 200, 'GOT ' + str(r.status_code) + ' ' + r.data
#     uid = r.get_json()['id']
#
#     r = send_request(app, api_url + '/users/' + str(uid))
#     assert r.status_code == 200, 'GOT ' + str(r.status_code) + ' ' + r.data
#     user = r.get_json()
#     assert user['name'] == 'new_user_create'
#     assert user['id'] == uid
#     assert len(user['roles']) == 3
#
#
# def test_create_user_empty_roles(sample_filled_app, api_url):
#     app, db, rbac, dmg = sample_filled_app
#
#     r = send_request(app, api_url + '/users', method='post', json={
#         'name': 'new_user_create'
#     })
#     assert r.status_code == 200, 'GOT ' + str(r.status_code) + ' ' + r.data
#     uid = r.get_json()['id']
#
#     r = send_request(app, api_url + '/users/' + str(uid))
#     assert r.status_code == 200, 'GOT ' + str(r.status_code) + ' ' + r.data
#     user = r.get_json()
#     assert user['name'] == 'new_user_create'
#     assert user['id'] == uid
#     assert len(user['roles']) == 0
