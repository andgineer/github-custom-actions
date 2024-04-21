import sys
import traceback
from pathlib import Path
from typing import Any, Optional

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
        path = getattr(obj.vars, self.var_name)
        try:
            return path.read_text()  # type: ignore
        except FileNotFoundError:
            return ""

    def __set__(self, obj: Any, value: str) -> None:
        path = getattr(obj.vars, self.var_name)
        try:
            path.write_text(value)
        except FileNotFoundError:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(value)


class ActionBase:
    """Base class for GitHub Actions.

    Implement main() method in the subclass.
    """

    vars: GithubVars

    def __init__(
        self, inputs: Optional[ActionInputs] = None, outputs: Optional[ActionOutputs] = None
    ) -> None:
        # (!) AttrDictVars() works as dict so empty one is False.
        # This is why we cannot use usual shorthand "or" here
        self.inputs = inputs if inputs is not None else ActionInputs()
        self.outputs = outputs if outputs is not None else ActionOutputs()
        self.vars = GithubVars()

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
        """Render template with context including inputs, outputs, and vars."""
        return Template(template.replace("\\n", "\n")).render(
            vars=self.vars,
            inputs=self.inputs,
            outputs=self.outputs,
        )
