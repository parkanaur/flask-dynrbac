def test_get_all_entities(sample_filled_app):
    app, db, rbac, dmg = sample_filled_app

    assert len(rbac.get_all_roles()) == 5
    assert len(rbac.get_all_users()) == 10
    assert len(rbac.get_all_permissions()) == 5
    assert len(rbac.get_all_units()) == 5

    assert len(db.session.query(dmg.RolePermission).all()) == 5
    assert len(db.session.query(dmg.UserRole).all()) == 14
    assert len(db.session.query(dmg.UnitPermission).all()) == 5
