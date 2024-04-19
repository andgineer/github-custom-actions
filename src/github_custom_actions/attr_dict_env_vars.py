import os
import typing
from pathlib import Path
from typing import Dict, Any


class AttrDictFileVars:
    """Dual access env vars.

    On read / write converts var names with `_name_from_external()` / `_external_name()` methods.
    They remove / add `_external_name_prefix` to the names.

    Access with attributes or as dict.
    Dict-like access just add `_external_name_prefix()" and do no other changes in the var name.
    Attribute access also do `_attr_to_var_name()` - by default it converts python attribute name
    from snake_case to kebab-case.
    With attributes you can only access explicitly declared vars.

    On attributes access convert camel_case of the attributes names to kebab-case with
    `_attr_to_var_name()` method.
    Because this is the only way to express with attributes the names with dash "-".
    Dict-like access does not modify names because for it we can use any style we want.

    This way you can find your balance between strictly defined vars and flexibility.

    Usage:
        class MyTextFileVars(TextFileVars):
            documented_var: str

            def __init__(self) -> None:
                super().__init__(Path("my_vars.txt"))

        vars = MyTextFileVars()
        vars["undocumented_var"] = "value1"
        vars.documented_var == "value2"

        Produce "my_vars.txt" with:
            documented-var=value1
            undocumented_var=value2
    """

    # todo: should be readonly
    _type_hints_cache: Dict[str, Dict[str, Any]] = {}
    _external_name_prefix = ""

    @classmethod
    def _get_type_hints(cls) -> Dict[str, Any]:
        # Use cls.__name__ to ensure each subclass uses its own cache entry
        if cls.__name__ not in cls._type_hints_cache:
            cls._type_hints_cache[cls.__name__] = typing.get_type_hints(cls)
        return cls._type_hints_cache[cls.__name__]

    def _attr_to_var_name(self, name: str) -> str:
        return name.replace("_", "-")

    def _external_name(self, name: str) -> str:
        """Convert variable name to the external form."""
        return self._external_name_prefix + name.upper()

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
            raise

    def __getitem__(self, key: str) -> Any:
        env_var_name = self._external_name(key)
        if env_var_name in os.environ:
            return os.environ[env_var_name]
        raise KeyError(f"{key} not found in environment variables")

    def __setitem__(self, key: str, value: Any) -> None:
        raise NotImplementedError("Setting environment variables is not supported.")

    def __delitem__(self, key: str) -> None:
        raise NotImplementedError("Deleting environment variables is not supported.")

    def __iter__(self) -> typing.Iterator[str]:
        raise NotImplementedError("Iterating over environment variables is not supported.")

    def __len__(self) -> int:
        raise NotImplementedError("Getting the number of environment variables is not supported.")

    def __contains__(self, key: object) -> bool:
        return self._external_name(self._attr_to_var_name(typing.cast(str, key))) in os.environ
