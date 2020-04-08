import pytest


def test_register_endpoints(rbac):
    """Should register functions in internal dict"""

    @rbac.rbac(unit_name='name1')
    def x():
        pass

    @rbac.rbac()
    def y():
        pass

    r = rbac.registered_endpoints

    assert len(r) == 2
    assert 'name1' in r
    assert 'test_conf_logic_y' in r


def test_fail_register_same_unit_name(rbac):
    """Should fail if the same unit name is already in dict"""
    rbac.unique_unit_names_only = True
    
    with pytest.raises(KeyError):

        @rbac.rbac(unit_name='non-unique name')
        def x():
            pass

        @rbac.rbac(unit_name='non-unique name')
        def y():
            pass

