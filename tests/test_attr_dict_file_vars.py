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

    vars["undocumented_var"] = "value3"
    assert temp_vars_file.read_text() == "undocumented_var=value3\ndocumented-var=value2"


def test_attr_dict_file_vars_contains(temp_vars_file):
    class MyAttrDictFileVars(AttrDictFileVars):
        documented_var: str

    vars = MyAttrDictFileVars(temp_vars_file)
    vars["undocumented_var"] = "value1"
    vars.documented_var = "value2"

    assert "undocumented_var" in vars
    assert "documented-var" in vars
    assert "documented_var" not in vars
    assert len(vars) == 2


def test_attr_dict_file_vars_write_external_names(temp_vars_file):
    class MyAttrDictFileVars(AttrDictFileVars):
        documented_var: str

        def _external_name(self, name: str) -> str:
            return f"EXT_{name}"

        def _name_from_external(self, name: str) -> str:
            return "_".join(name.split("_")[1:])

    vars = MyAttrDictFileVars(temp_vars_file)
    vars["undocumented_var"] = "value1"
    vars.documented_var = "value2"

    assert vars["undocumented_var"] == "value1"
    assert vars.documented_var == "value2"

    assert temp_vars_file.read_text() == "EXT_undocumented_var=value1\nEXT_documented-var=value2"


def test_attr_dict_file_vars_read_external_names(temp_vars_file):
    class MyAttrDictFileVars(AttrDictFileVars):
        documented_var: str

        def _external_name(self, name: str) -> str:
            return f"EXT_{name}"

        def _name_from_external(self, name: str) -> str:
            return "_".join(name.split("_")[1:])

    vars = MyAttrDictFileVars(temp_vars_file)
    temp_vars_file.write_text("EXT_undocumented_var=value1\nEXT_documented-var=value2")
    assert vars["undocumented_var"] == "value1"
    assert vars.documented_var == "value2"

    vars["undocumented_var"] = "value3"
    assert temp_vars_file.read_text() == "EXT_undocumented_var=value3\nEXT_documented-var=value2"


def test_attr_dict_file_vars_read_prefixed_names(temp_vars_file):
    class MyAttrDictFileVars(AttrDictFileVars):
        documented_var: str

        _external_name_prefix = "ext!_"

    vars = MyAttrDictFileVars(temp_vars_file)
    temp_vars_file.write_text("ext!_undocumented_var=value1\next!_documented-var=value2")
    assert vars["undocumented_var"] == "value1"
    assert vars.documented_var == "value2"

    vars["undocumented_var"] = "value3"
    assert temp_vars_file.read_text() == "ext!_undocumented_var=value3\next!_documented-var=value2"
