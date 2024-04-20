"""Github Actions helper functions.

We want to support Python 3.7 that you still have on some self-hosted action runners.
So no fancy features like walrus operator, @cached_property, etc.
"""

import os
import typing
from pathlib import Path
from typing import Dict, Union, Optional, Any
from github_custom_actions.file_attr_dict_vars import FileAttrDictVars


INPUT_PREFIX = "INPUT_"


class DocumentedEnvVars:
    """Documented environment variables.

    Lazy load attributes from environment variables.
    Only described attributes are loaded.
    Attributes with type Path converted accordingly, it the value is "" set to None.
    """

    # todo: should be readonly
    _type_hints_cache: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def _get_type_hints(cls) -> Dict[str, Any]:
        # Use cls.__name__ to ensure each subclass uses its own cache entry
        if cls.__name__ not in cls._type_hints_cache:
            cls._type_hints_cache[cls.__name__] = typing.get_type_hints(cls)
        return cls._type_hints_cache[cls.__name__]

    def attribute_to_env_var(self, name: str) -> str:
        """Convert attribute name to environment variable name."""
        return name.upper()

    def __getattribute__(self, name: str) -> Any:
        try:
            return super().__getattribute__(name)
        except AttributeError as exc:
            type_hints = self.__class__._get_type_hints()
            if name not in type_hints:
                raise AttributeError(f"Unknown {name}") from exc
            env_var_name = self.attribute_to_env_var(name)
            if env_var_name in os.environ:
                value: Optional[Union[str, Path]] = os.environ[env_var_name]

                # If the type hint is Path, convert the value to Path
                if type_hints[name] is Path:
                    value = Path(value) if value else None
                self.__dict__[name] = value
                return value
            raise


class ActionInputs(DocumentedEnvVars):  # pylint: disable=too-few-public-methods
    """GitHub Action input variables.

    Usage:
        class MyInputs(ActionInputs):
            my_input: str

        action = ActionBase(inputs=MyInputs())
        # to get action input `my-input` from environment var `INPUT_MY-INPUT`
        print(action.inputs.my_input)
    """

    def attribute_to_env_var(self, name: str) -> str:
        return INPUT_PREFIX + name.upper().replace("_", "-")


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
