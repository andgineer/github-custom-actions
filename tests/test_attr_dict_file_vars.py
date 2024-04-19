import pytest
from pathlib import Path
from github_custom_actions.attr_dict_file_vars import AttrDictFileVars


@pytest.fixture
def temp_vars_file(tmp_path):
    return tmp_path / "my_vars.txt"


def test_attr_dict_file_vars_access_documented_vars_as_attributes(temp_vars_file):
    class MyAttrDictFileVars(AttrDictFileVars):
        documented_var: str

        def __init__(self) -> None:
            super().__init__(temp_vars_file)

    vars = MyAttrDictFileVars()
    vars.documented_var = "value2"
    assert vars.documented_var == "value2"
    assert temp_vars_file.read_text() == "documented-var=value2"


def test_attr_dict_file_vars_access_undocumented_vars_as_dict(temp_vars_file):
    class MyAttrDictFileVars(AttrDictFileVars):
        documented_var: str

    vars = MyAttrDictFileVars(temp_vars_file)
    vars["undocumented_var"] = "value1"
    assert vars["undocumented_var"] == "value1"
    assert temp_vars_file.read_text() == "undocumented_var=value1"


def test_attr_dict_file_vars_access_mixed_vars_as_attributes_and_dict(temp_vars_file):
    class MyAttrDictFileVars(AttrDictFileVars):
        documented_var: str

    vars = MyAttrDictFileVars(temp_vars_file)
    vars["undocumented_var"] = "value1"
    vars.documented_var = "value2"

    assert vars["undocumented_var"] == "value1"
    assert vars.documented_var == "value2"

    assert temp_vars_file.read_text() == "undocumented_var=value1\ndocumented-var=value2"


def test_attr_dict_file_vars_delete_var(temp_vars_file):
    class MyAttrDictFileVars(AttrDictFileVars):
        documented_var: str

    vars = MyAttrDictFileVars(temp_vars_file)
    vars["undocumented_var"] = "value1"
    vars.documented_var = "value2"
    assert temp_vars_file.read_text() == "undocumented_var=value1\ndocumented-var=value2"

    del vars["undocumented_var"]
    assert "undocumented_var" not in vars
    assert vars.documented_var == "value2"
    assert temp_vars_file.read_text() == "documented-var=value2"


def test_attr_dict_file_vars_file_not_found(tmp_path):
    non_existent_file = tmp_path / "non_existent.txt"
    vars = AttrDictFileVars(non_existent_file)
    assert vars["some_var"] == ""
    vars["some_var"] = "value"
    assert vars["some_var"] == "value"
    assert non_existent_file.read_text() == "some_var=value"


def test_attr_dict_file_vars_unexisted_attribute(temp_vars_file):
    class MyAttrDictFileVars(AttrDictFileVars):
        documented_var: str

    vars = MyAttrDictFileVars(temp_vars_file)
    with pytest.raises(AttributeError):
        vars.undocumented_var


def test_attr_dict_file_vars_iterator(temp_vars_file):
    class MyAttrDictFileVars(AttrDictFileVars):
        documented_var: str

    vars = MyAttrDictFileVars(temp_vars_file)
    vars["undocumented_var"] = "value1"
    vars.documented_var = "value2"

    assert list(vars) == ["undocumented_var", "documented-var"]
