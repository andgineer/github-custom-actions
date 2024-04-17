import tempfile
from unittest.mock import patch
from pathlib import Path
from github_custom_actions.action_base import ActionBase
import pytest

from github_custom_actions.inputs_outputs import ActionInputs


@pytest.fixture
def inputs():
    input_env = {
        "INPUT_MY-INPUT": "value1",
        "INPUT_ANOTHER-INPUT": "value2"
    }
    with patch.dict('os.environ', input_env):
        yield


@pytest.fixture
def outputs():
    with tempfile.TemporaryDirectory() as temp_dir:
        github_output = Path(temp_dir) / "output.txt"
        output_env = {
            "GITHUB_OUTPUT": str(github_output)
        }
        with patch.dict('os.environ', output_env):
            yield github_output


class Inputs(ActionInputs):
    my_input: str
    another_input: str


@pytest.fixture(scope="function")
def action(inputs, outputs):
    return ActionBase(inputs=Inputs())


def test_input_retrieval(action):
    """Test retrieval of input values."""
    assert action.inputs.my_input == "value1"
    assert action.inputs.another_input == "value2"


def test_output_set_and_get(inputs, outputs):
    """Test setting and getting output values."""
    action = ActionBase()
    action.outputs["my_output"] = "output_value"

    assert outputs.read_text() == "my_output=output_value"


def test_input_caching(action, monkeypatch):
    """Test that input is loaded from env var only once."""
    monkeypatch.delenv("INPUT_MY-INPUT")
    with pytest.raises(AttributeError):
        assert action.inputs.my_input == "value1"

    monkeypatch.setenv("INPUT_MY-INPUT", "value1")
    assert action.inputs.my_input == "value1"

    monkeypatch.delenv("INPUT_MY-INPUT")
    assert action.inputs.my_input == "value1"  # from cache
