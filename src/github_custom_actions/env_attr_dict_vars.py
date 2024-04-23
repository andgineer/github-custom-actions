import os
import typing
from pathlib import Path
from typing import Any
from github_custom_actions.attr_dict_vars import AttrDictVars


class EnvAttrDictVars(AttrDictVars):
    """Dual access env vars.

    Access to env vars as object attributes or as dict items.
    Do not allow to change vars so this is read-only source of env vars values.

    With attributes, you can only access explicitly declared vars, with dict - any.
    This way you can find your balance between strictly defined vars and flexibility.

    Usage:
        class MyVars(EnvAttrDictVars):
            documented_var: str

        vars = MyVars(prefix="INPUT_")
        print(vars["undocumented_var"])  # from os.environ["INPUT_UNDOCUMENTED_VAR"]
        print(vars.documented_var)  # from os.environ["INPUT_DOCUMENTED-VAR"]

    Attribute names converted with method `_attr_to_var_name()` - it converts python attribute
    name from snake_case to kebab-case.
    """

    def __getattribute__(self, name: str) -> Any:
        try:
            return super().__getattribute__(name)
        except AttributeError as exc:
            type_hints = self.__class__._get_type_hints()
            if name not in type_hints:
                raise AttributeError(f"Unknown {name}") from exc
            env_var_name = self._external_name(self._attr_to_var_name(name))
            if env_var_name in os.environ:
                value: typing.Optional[typing.Union[str, Path]] = os.environ[env_var_name]

                # If the type hint is Path, convert the value to Path
                if type_hints[name] is Path:
                    value = Path(value) if value else None
                self.__dict__[name] = value
                return value
            raise AttributeError(
                f"`{name}` ({env_var_name}) not found in environment variables"
            ) from exc

    def __getitem__(self, key: str) -> Any:
        env_var_name = self._external_name(key)
        if env_var_name in os.environ:
            return os.environ[env_var_name]
        raise KeyError(f"`{key}` ({env_var_name}) not found in environment variables")

    def __setitem__(self, key: str, value: Any) -> None:
        raise NotImplementedError("Setting environment variables is not supported.")

    def __delitem__(self, key: str) -> None:
        raise NotImplementedError("Deleting environment variables is not supported.")

    def __iter__(self) -> typing.Iterator[str]:
        raise NotImplementedError("Iterating over environment variables is not supported.")

    def __len__(self) -> int:
        raise NotImplementedError("Getting the number of environment variables is not supported.")

    def __contains__(self, key: object) -> bool:
        env_var_name = self._external_name(self._attr_to_var_name(typing.cast(str, key)))
        exists = env_var_name in os.environ
        if not exists:
            print(f"`{key}` ({env_var_name}) not found in environment variables")
        return exists
