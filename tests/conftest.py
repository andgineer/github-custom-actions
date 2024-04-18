import pytest
from github_custom_actions.inputs_outputs import ActionInputs
from github_custom_actions.action_base import ActionBase
import tempfile
from unittest.mock import patch
from pathlib import Path


@pytest.fixture
def inputs():
    with tempfile.TemporaryDirectory() as temp_dir:
        input_env = {
            "INPUT_MY-INPUT": "value1",
            "INPUT_ANOTHER-INPUT": "value2",
            "GITHUB_STEP_SUMMARY": str(Path(temp_dir) / "summary.txt")
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
