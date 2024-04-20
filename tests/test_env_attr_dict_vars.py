from unittest.mock import patch

import pytest

from github_custom_actions.env_attr_dict_vars import EnvAttrDictVars


@pytest.fixture
def setup_env_vars():
    """Setup test environment variables."""
    with patch.dict('os.environ', {
        'INPUT_DOCUMENTED-VAR': 'test_value',
        'INPUT_TEST_VAR': 'test_value2',
        'INPUT_UNDECLATED-VAR': 'test_value3'
    }):
        yield


class MyTextFileVars(EnvAttrDictVars):
    documented_var: str

    def __init__(self) -> None:
        super().__init__(prefix='INPUT_')


def test_env_attr_dict_vars_attribute_access(setup_env_vars):
    vars = MyTextFileVars()
    assert vars.documented_var == 'test_value'


def test_env_attr_dict_vars_undeclared_attribute_access(setup_env_vars):
    vars = MyTextFileVars()
    with pytest.raises(AttributeError):
        assert vars.undeclated_var == 'test_value'


def test_env_attr_dict_vars_dict_access(setup_env_vars):
    vars = MyTextFileVars()
    assert vars['documented-var'] == 'test_value'
    assert vars['test_var'] == 'test_value2'



def test_env_attr_dict_vars_name_conversion():
    vars = MyTextFileVars()
    assert vars._attr_to_var_name('test_var') == 'test-var'
    assert vars._external_name('test_var') == 'INPUT_TEST_VAR'


def test_env_attr_dict_vars_setting_variable():
    vars = MyTextFileVars()
    with pytest.raises(NotImplementedError):
        vars['new_var'] = 'new_value'


def test_env_attr_dict_vars_deleting_variable():
    vars = MyTextFileVars()
    with pytest.raises(NotImplementedError):
        del vars['documented_var']


def test_env_attr_dict_vars_iterating_variables():
    vars = MyTextFileVars()
    with pytest.raises(NotImplementedError):
        for key in vars:
            pass

