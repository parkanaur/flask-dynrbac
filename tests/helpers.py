def send_request(app, url, method='get'):
    with app.test_client() as client:
        with app.app_context():
            return getattr(client, method)(url)


def send_and_assert(app, url, method='get', code=200, exp_string=b'Hello World!'):
    r = send_request(app, url, method)
    assert r.status_code == code, 'GOT ' + str(r.status_code)
    assert exp_string in r.data, 'GOT ' + r.data
    return r
