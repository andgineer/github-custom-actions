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

    You should implement `main()` method in the subclass.

    You can define custom inputs and / or outputs types in the subclass.
    You can do nothing in the subclass if you don't need typed inputs and outputs.

    Note these are just types, instances of these types are automatically created in the `__init__` method.

    Usage:
    ```python
    class MyInputs(ActionInputs):
        my_input: str
        '''My input description'''

        my_path: Path
        '''My path description'''

    class MyOutputs(ActionOutputs):
        runner_os: str
        '''Runner OS description'''

    class MyAction(ActionBase):
        inputs: MyInputs
        outputs: MyOutputs

        def main(self):
            if self.inputs.my_path is None:
                raise ValueError("my-path is required")
            self.inputs.my_path.mkdir(exist_ok=True)
            self.outputs.runner_os = self.env.runner_os
            self.summary.text += (
                self.render(
                    "### {{ inputs.my_input }}.\\n"
                    "Have a nice day, {{ inputs['name'] }}!"
                )
            )

    if __name__ == "__main__":
        MyAction().run()
    ```
    """

    inputs: ActionInputs
    outputs: ActionOutputs
    env: GithubVars

    def __init__(self) -> None:
        """Initialize inputs, outputs according to the type than could be set in subclass."""
        types = get_type_hints(self.__class__)
        self.inputs = types["inputs"]()
        self.outputs = types["outputs"]()
        self.env = GithubVars()

        base_dir = Path(__file__).resolve().parent
        templates_dir = base_dir / "templates"
        self.environment = Environment(loader=FileSystemLoader(str(templates_dir)))

    summary = FileTextProperty("github_step_summary")

    def main(self) -> None:
        """Business logic of the action.

        Is called by `run()` method.
        """
        raise NotImplementedError

    def run(self) -> None:
        """Run the action.

        `run()` calls the `main()` method of the action with the necessary boilerplate to catch and
        report exceptions.

        Usage:
        ```python
        if __name__ == "__main__":
            MyAction().run()
        ```

        `main()` is where you implement the business logic of your action.
        """
        try:
            self.main()
        except Exception:  # pylint: disable=broad-except
            traceback.print_exc(file=sys.stderr)
            sys.exit(1)

    def render(self, template: str, **kwargs: Any) -> str:
        """Render the template from the string with Jinja.

        `kwargs` are the template context variables.

        Also includes to the context the action's `inputs`, `outputs`, and `env`.

        So you can use something like:
        ```python
        self.render("### {{ inputs.name }}!\\nHave a nice day!")
        ```

        """
        return Template(template.replace("\\n", "\n")).render(
            env=self.env,
            inputs=self.inputs,
            outputs=self.outputs,
            **kwargs,
        )

    def render_template(self, template_name: str, **kwargs: Any) -> str:
        """Render template from the `templates` directory.

        `template_name` is the name of the template file without the extension.
        `kwargs` are the template context variables.

        Also includes to the context the action's `inputs`, `outputs`, and `env`.

        Usage:
        ```python
        self.render_template("executor.json", image="ubuntu-latest")
        ```
        """
        template = self.environment.get_template(template_name)
        return template.render(env=self.env, inputs=self.inputs, outputs=self.outputs, **kwargs)
