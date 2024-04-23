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

    Attribute names converted to `kebab-case`.
    So `action.inputs.my_input` is the same as `action.inputs["my-input"]`.

    If you need to access `snake_case` named input `my_input` you should
    use dict-style only: `action.inputs["my_input"]`.
    But it's common to use `kebab-case` in GitHub Actions inputs names.

    By github convention all input names are upper-cased in environment and prefixed with "INPUT_".
    So `actions.inputs.my_input` or `actions.inputs['my-input']` will be variable `INPUT_MY-INPUT` in environment.
    The ActionInputs does the conversion automatically.

    Use lazy loading of the values.
    So the value is read from environment only when accessed and only once, and saved in the object internal dict.
    """

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

    Attribute names converted to `kebab-case`.
    So `action.outputs.my_output` is the same as `action.outputs["my-output"]`.

    If you need to access `snake_case` named output `my_output` you should
    use dict-style only: `action.outputs["my-output"]`.
    But it's common to use `kebab-case` in GitHub Actions outputs names.

    Each outputs vars assignment change the Github outputs file (the path is defined as `action.env.github_output`).
    """

    def __init__(self) -> None:
        super().__init__(Path(os.environ["GITHUB_OUTPUT"]))
