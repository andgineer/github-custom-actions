from pathlib import Path

import pytest


def test_input_retrieval(action):
    """Test retrieval of input values."""
    assert action.inputs.my_input == "value1"
    assert action.inputs.another_input == "value2"


def test_output_set_and_read(action):
    """Test setting and getting output values."""
    action.outputs["my_output"] = "output_value"
    with pytest.raises(AttributeError):
        action.outputs.my_output2 = "output_value2"
    action.outputs.my_output = "output_value2"

    assert action.env.github_output.read_text() == "my_output=output_value\nmy-output=output_value2"


def test_input_caching(action, monkeypatch):
    """Test that input is loaded from env var only once."""
    monkeypatch.delenv("INPUT_MY-INPUT")
    with pytest.raises(AttributeError):
        assert action.inputs.my_input == "value1"

    monkeypatch.setenv("INPUT_MY-INPUT", "value1")
    assert action.inputs.my_input == "value1"

    monkeypatch.delenv("INPUT_MY-INPUT")
    assert action.inputs.my_input == "value1"  # from cache


def test_output_dict_exact(action):
    action.outputs["snake_eatsCamel-NOT-kebab"] = "a"
    assert action.env.github_output.read_text() == "snake_eatsCamel-NOT-kebab=a"


def test_output_path_conversion(action):
    """Test that Path objects are preserved and can be used with Path operations."""
    test_path = Path("/test/path/to/reports")
    action.outputs["reports_path"] = test_path

    # Verify it's saved as string to file
    assert action.env.github_output.read_text() == "reports_path=/test/path/to/reports"

    # Verify the Path object is preserved for operations
    retrieved_path = action.outputs["reports_path"]
    assert isinstance(retrieved_path, Path)
    assert retrieved_path == test_path

    # Verify Path operations work
    subpath = retrieved_path / "subdir"
    assert isinstance(subpath, Path)
    assert str(subpath) == "/test/path/to/reports/subdir"

    # Test with attribute access
    action.outputs.my_output = Path("/another/path")
    expected = "reports_path=/test/path/to/reports\nmy-output=/another/path"
    assert action.env.github_output.read_text() == expected

    # Verify attribute access also preserves Path
    assert isinstance(action.outputs.my_output, Path)


def test_output_number_conversion(action):
    """Test that numbers are preserved and converted to strings when saved."""
    action.outputs["count"] = 42
    # Verify it's saved as string to file
    assert action.env.github_output.read_text() == "count=42"
    # Verify the number is preserved for operations
    assert action.outputs["count"] == 42
    assert isinstance(action.outputs["count"], int)

    action.outputs["pi"] = 3.14159
    assert action.env.github_output.read_text() == "count=42\npi=3.14159"
    # Verify float is preserved
    assert action.outputs["pi"] == 3.14159
    assert isinstance(action.outputs["pi"], float)
