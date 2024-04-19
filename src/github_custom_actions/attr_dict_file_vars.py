import typing
from collections.abc import MutableMapping
from pathlib import Path
from typing import Dict, Iterator, List, Optional, Any

INPUT_PREFIX = "INPUT_"


class AttrDictFileVars(MutableMapping):  # type: ignore
    """Dual access vars in a file.

    Stored as `key=value` lines in a text file.

    Access with attributes or as dict.
    Dict-like access possible for any var name - they will be auto-created in the file on first access.
    Attribute access only for explicitly declared vars.

    On attributes access convert camel_case of the attributes names to kebab-case.
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

    _type_hints_cache: Dict[str, Dict[str, Any]] = {}

    def __init__(self, vars_file: Path, kebab_names: bool = True) -> None:
        """ "Text files with vars.

        `kebab_names` if True, attribute names on save will use kebab-case.
        For dict-like access do not convert names.
        """
        self.vars_file: Path = vars_file
        self.kebab_names: bool = kebab_names
        self._var_keys: Optional[Dict[str, str]] = None
        self._type_hints_cache: Dict[str, Dict[str, Any]] = {}

    def __getattribute__(self, name: str) -> Any:
        try:
            return object.__getattribute__(self, name)
        except AttributeError as exc:
            type_hints = self.__class__._get_type_hints()
            if name in type_hints:
                value = self[name]
                self.__dict__[name] = value
                return value
            raise AttributeError(f"Unknown {name}") from exc

    @classmethod
    def _get_type_hints(cls) -> Dict[str, Any]:
        class_name = cls.__name__
        if class_name not in cls._type_hints_cache:
            cls._type_hints_cache[class_name] = typing.get_type_hints(cls)
        return cls._type_hints_cache[class_name]

    def __getitem__(self, key: str) -> str:
        try:
            return self._get_var_keys[key]
        except KeyError:
            self._get_var_keys[key] = ""
            self._save_var_file()
            return ""

    def __setitem__(self, key: str, value: str) -> None:
        """Access dict-style.

        vars["key"] = "value"
        """
        self._get_var_keys[key] = value
        self._save_var_file()

    def __setattr__(self, name: str, value: Any) -> None:
        """Access attribute-style.

        vars.key = "value"
        """
        type_hints = self.__class__._get_type_hints()
        if name in type_hints and not name.startswith("_"):
            # if self.kebab_names:
            #     name = name.replace("_", "-")
            self[name] = value  # use __setitem__ to save the file
        else:
            super().__setattr__(name, value)

    def __delitem__(self, key: str) -> None:
        del self._get_var_keys[key]
        self._save_var_file()

    def __iter__(self) -> Iterator[str]:
        return iter(self._get_var_keys)

    def __len__(self) -> int:
        return len(self._get_var_keys)

    def __contains__(self, key: object) -> bool:
        return key in self._get_var_keys

    @property
    def _get_var_keys(self) -> Dict[str, str]:
        """Load key-value pairs from a file, returning {} if the file does not exist."""
        if self._var_keys is None:
            try:
                content = self.vars_file.read_text(encoding="utf-8")
                self._var_keys = dict(
                    (line.split("=", 1) for line in content.splitlines() if "=" in line)
                )
            except FileNotFoundError:
                self._var_keys = {}
        return self._var_keys

    def _save_var_file(self) -> None:
        self.vars_file.parent.mkdir(parents=True, exist_ok=True)
        lines: List[str] = [f"{key}={value}" for key, value in self._get_var_keys.items()]
        self.vars_file.write_text("\n".join(lines), encoding="utf-8")
