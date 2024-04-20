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
        class MyInputs(ActionInputs):
            my_input: str

        action = ActionBase(inputs=MyInputs())

        # to get action input `my-input` from environment var `INPUT_MY-INPUT`
        print(action.inputs.my_input)
        print(action.inputs["my-input"])  # the same as above
    """

    # pylint: disable=abstract-method  # we want RO implementation that raises NotImplementedError on write

    def __init__(self) -> None:
        super().__init__(prefix=INPUT_PREFIX)


class ActionOutputs(FileAttrDictVars):
    """GitHub Actions output variables.

    Usage:
        class MyOutputs(ActionOutputs):
            my_output: str

        action = ActionBase(outputs=MyOutputs())
        action.outputs["my-output"] = "value"
        action.outputs.my_output = "value"  # the same as above
    """

    def __init__(self) -> None:
        super().__init__(Path(os.environ["GITHUB_OUTPUT"]))
