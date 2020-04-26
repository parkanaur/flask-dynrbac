from helpers import send_and_assert, send_request


def test_get_all(sample_filled_app, api_url):
    app, db, rbac, dmg = sample_filled_app

    users = send_request(app, api_url + '/users').get_json()
    assert len(users) == 10
    for user in users:
        assert 'name' in user
        assert 'id' in user
        assert 'roles' in user
        assert len(user['roles']) >= 1
