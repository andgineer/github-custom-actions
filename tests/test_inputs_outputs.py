import tempfile
from unittest.mock import patch
from pathlib import Path
from github_custom_actions.action_base import ActionBase
import pytest


@pytest.fixture
def inputs():
    input_env = {
        "INPUT_MY_INPUT": "value1",
        "INPUT_ANOTHER_INPUT": "value2"
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


def test_input_proxy_retrieval(inputs, outputs):
    """Test retrieval of input values."""
    action = ActionBase()
    assert action.input["my_input"] == "value1"
    assert action.input["another_input"] == "value2"


def test_output_proxy_set_and_get(inputs, outputs):
    """Test setting and getting output values."""
    action = ActionBase()
    action.output["my_output"] = "output_value"

    assert outputs.read_text() == "my_output=output_value"


def test_input_proxy_immutable(inputs, outputs):
    """Test that input proxy does not allow setting or deleting items."""
    action = ActionBase()
    with pytest.raises(ValueError):
        action.input["my_input"] = "new_value"

    with pytest.raises(ValueError):
        del action.input["my_input"]

