def test_get_all_entities(sample_filled_app):
    app, db, rbac, dmg = sample_filled_app

    assert len(rbac.get_all_roles()) == 5
    assert len(rbac.get_all_users()) == 10
    assert len(rbac.get_all_permissions()) == 5
    assert len(rbac.get_all_units()) == 5

    assert len(db.session.query(dmg.RolePermission).all()) == 5
    assert len(db.session.query(dmg.UserRole).all()) == 13
    assert len(db.session.query(dmg.UnitPermission).all()) == 5


def test_new_units_addition(sample_filled_app):
    app, db, rbac, dmg = sample_filled_app
    rbac.create_permission_for_missing_units = True

    @app.route('/unit6')
    @rbac.rbac(unit_name='unit6')
    def unit6():
        return 'unit6!'

    rbac.create_permission_for_missing_units = False

    @app.route('/unit7')
    @rbac.rbac(unit_name='unit7')
    def unit7():
        return 'unit7'

    units = rbac.get_all_units()
    assert len(units) == 7
    assert units[5].name == 'unit6'
    assert units[5].permissions[0].name == 'can_access_unit6'
    assert units[6].name == 'unit7'
    assert len(units[6].permissions) == 0
