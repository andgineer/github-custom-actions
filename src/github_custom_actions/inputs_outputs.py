"""Github Actions helper functions.

We want to support Python 3.7 that you still have on some self-hosted action runners.
So no fancy features like walrus operator, @cached_property, etc.
"""

import os
from pathlib import Path
from github_custom_actions.file_attr_dict_vars import FileAttrDictVars
from github_custom_actions.env_attr_dict_vars import EnvAttrDictVars


INPUT_PREFIX = "INPUT_"


class ActionInputs(EnvAttrDictVars):
    """GitHub Action input variables.

    Usage:
        ```python
        class MyInputs(ActionInputs):
            my_input: str

        action = ActionBase(inputs=MyInputs())
        print(action.inputs.my_input)
        print(action.inputs["my-input"])  # the same as above
        ```

    With attributes, you can only access explicitly declared vars, with dict-like access you can access any var.
    This way you can find your balance between strictly defined vars and flexibility.

    Attribute names are converted to `kebab-case`.
    So `action.inputs.my_input` is the same as `action.inputs["my-input"]`.

    If you need to access a `snake_case` named input `my_input`, you should
    use dict-style only: `action.inputs["my_input"]`.
    But it's common to use `kebab-case` in GitHub Actions input names.

    By GitHub convention, all input names are upper-cased in the environment and prefixed with "INPUT_".
    So `actions.inputs.my_input` or `actions.inputs['my-input']` will be the variable `INPUT_MY-INPUT`
    in the environment.
    The ActionInputs does the conversion automatically.

    Uses lazy loading of the values.
    So the value is read from the environment only when accessed and only once,
    and saved in the object's internal dict."""

    # pylint: disable=abstract-method  # we want RO implementation that raises NotImplementedError on write

    def _external_name(self, name: str) -> str:
        """Convert variable name to the external form."""
        return INPUT_PREFIX + name.upper()


class ActionOutputs(FileAttrDictVars):
    """GitHub Actions output variables.

    Usage:
       ```python
       class MyOutputs(ActionOutputs):
           my_output: str

       action = ActionBase(outputs=MyOutputs())
       action.outputs["my-output"] = "value"
       action.outputs.my_output = "value"  # the same as above
       ```

    With attributes, you can only access explicitly declared vars,
    with dict-like access you can access any var.
    This way you can find your balance between strictly defined vars and flexibility.

    Attribute names are converted to `kebab-case`.
    So `action.outputs.my_output` is the same as `action.outputs["my-output"]`.

    If you need to access a `snake_case` named output like `my_output` you should
    use dict-style only: `action.outputs["my_output"]`.
    But it's common to use `kebab-case` in GitHub Actions output names.

    Each output var assignment changes the GitHub outputs file
    (the path is defined as `action.env.github_output`).
    """

    def __init__(self) -> None:
        super().__init__(Path(os.environ["GITHUB_OUTPUT"]))
