import sys
import traceback
from pathlib import Path
from typing import Any, get_type_hints

from jinja2 import Template, Environment, FileSystemLoader

from github_custom_actions.inputs_outputs import ActionOutputs, ActionInputs
from github_custom_actions.github_vars import GithubVars


class FileTextProperty:
    """Property descriptor read / write from a file."""

    def __init__(self, var_name: str) -> None:
        """Initialize the property descriptor.

        `var_name` is the name of the object's `vars` attribute with the path to the file.
        """
        self.var_name = var_name

    def __get__(self, obj: Any, objtype: Any = None) -> str:
        path = getattr(obj.env, self.var_name)
        try:
            return path.read_text()  # type: ignore
        except FileNotFoundError:
            return ""

    def __set__(self, obj: Any, value: str) -> None:
        path = getattr(obj.env, self.var_name)
        try:
            path.write_text(value)
        except FileNotFoundError:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(value)


class ActionBase:
    """Base class for GitHub Actions.

    Implement main() method in the subclass.
    """

    inputs: ActionInputs
    outputs: ActionOutputs
    env: GithubVars

    def __init__(self) -> None:
        # Initialize inputs, outputs according to the type than could be set in subclass.
        types = get_type_hints(self.__class__)
        self.inputs = types["inputs"]()
        self.outputs = types["outputs"]()
        self.env = GithubVars()

        base_dir = Path(__file__).resolve().parent
        templates_dir = base_dir / "templates"
        self.environment = Environment(loader=FileSystemLoader(str(templates_dir)))

    summary = FileTextProperty("github_step_summary")

    def main(self) -> None:
        """Main method."""
        raise NotImplementedError

    def run(self) -> None:
        """Run main method."""
        try:
            self.main()
        except Exception:  # pylint: disable=broad-except
            traceback.print_exc(file=sys.stderr)
            sys.exit(1)

    def render(self, template: str) -> str:
        """Render template with context including inputs, outputs, and env."""
        return Template(template.replace("\\n", "\n")).render(
            env=self.env,
            inputs=self.inputs,
            outputs=self.outputs,
        )
