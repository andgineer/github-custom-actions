import os

import pytest
from unittest.mock import patch, MagicMock
from github_custom_actions.action_base import ActionBase, ActionInputs, ActionOutputs, GithubVars


def test_action_base_summary(action):
    action.summary = "test"
    action.summary += "1"
    assert action.env.github_step_summary.read_text() == "test1"


def test_outputs_single_line_constraint(test_action):
    with pytest.raises(ValueError, match="single-line"):
        test_action.outputs.test_output = "line1\nline2"


class MockInputs(ActionInputs):
    test_input: str
    """Test input description"""


class MockOutputs(ActionOutputs):
    test_output: str
    """Test output description"""


class MockAction(ActionBase):
    inputs: MockInputs
    outputs: MockOutputs

    def main(self):
        self.outputs.test_output = f"Hello, {self.inputs.test_input}!"


@pytest.fixture
def mock_env_vars():
    with patch.dict(
        os.environ,
        {
            "GITHUB_OUTPUT": "/tmp/github_output",
            "GITHUB_STEP_SUMMARY": "/tmp/github_step_summary",
            "RUNNER_OS": "Linux",
            # Add other required environment variables here
        },
    ):
        yield


@pytest.fixture
def test_action(mock_env_vars):
    return MockAction()


def test_action_initialization(test_action):
    assert isinstance(test_action.inputs, MockInputs)
    assert isinstance(test_action.outputs, MockOutputs)
    assert isinstance(test_action.env, GithubVars)


def test_main_method(test_action):
    test_action.inputs.test_input = "World"
    test_action.main()
    assert test_action.outputs.test_output == "Hello, World!"


def test_run_method_success(test_action):
    with patch.object(test_action, "main") as mock_main:
        test_action.run()
        mock_main.assert_called_once()


def test_run_method_failure(test_action):
    with patch.object(test_action, "main", side_effect=Exception("Test exception")):
        with pytest.raises(SystemExit) as exc_info:
            test_action.run()
        assert exc_info.value.code == 1


def test_render_method(test_action):
    test_action.inputs.test_input = "User"
    test_action.outputs.test_output = "Result"
    test_action.env.runner_os = "Linux"

    template = (
        "Hello, {{ inputs.test_input }}! Output: {{ outputs.test_output }}. OS: {{ env.runner_os }}"
    )
    result = test_action.render(template)
    assert result == "Hello, User! Output: Result. OS: Linux"


def test_render_template_method(test_action):
    test_action.inputs.test_input = "User"
    test_action.outputs.test_output = "Result"
    test_action.env.runner_os = "Linux"

    mock_template = MagicMock()
    mock_template.render.return_value = "Rendered template"

    with patch.object(
        test_action.environment, "get_template", return_value=mock_template
    ) as mock_get_template:
        result = test_action.render_template("test_template.j2", extra_var="Extra")

        mock_get_template.assert_called_once_with("test_template.j2")
        mock_template.render.assert_called_once_with(
            env=test_action.env,
            inputs=test_action.inputs,
            outputs=test_action.outputs,
            extra_var="Extra",
        )
        assert result == "Rendered template"


@pytest.mark.parametrize("file_exists", [True, False])
def test_file_text_property(test_action, tmp_path, file_exists):
    test_file = tmp_path / "test_file.txt"
    test_content = "Test content"

    if file_exists:
        test_file.write_text(test_content)

    with patch.object(test_action.env, "github_step_summary", test_file):
        if file_exists:
            assert test_action.summary == test_content
        else:
            assert test_action.summary == ""

        new_content = "New content"
        test_action.summary = new_content
        assert test_file.read_text() == new_content
