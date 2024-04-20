from github_custom_actions.action_base import ActionBase
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

    assert action.vars.github_output.read_text() == "my_output=output_value\nmy-output=output_value2"


def test_input_caching(action, monkeypatch):
    """Test that input is loaded from env var only once."""
    monkeypatch.delenv("INPUT_MY-INPUT")
    with pytest.raises(AttributeError):
        assert action.inputs.my_input == "value1"

    monkeypatch.setenv("INPUT_MY-INPUT", "value1")
    assert action.inputs.my_input == "value1"

    monkeypatch.delenv("INPUT_MY-INPUT")
    assert action.inputs.my_input == "value1"  # from cache
