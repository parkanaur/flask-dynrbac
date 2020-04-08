def test_get_all_entities(sample_filled_app):
    app, db, rbac = sample_filled_app

    assert len(rbac.get_all_roles()) == 5
    assert len(rbac.get_all_users()) == 10
    assert len(rbac.get_all_permissions()) == 5
