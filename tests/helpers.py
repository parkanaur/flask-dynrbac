def send_request(app, url, method='get'):
    with app.test_client() as client:
        with app.app_context():
            return getattr(client, method)(url)
