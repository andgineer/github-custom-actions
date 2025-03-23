from collections.abc import MutableMapping
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional

from github_custom_actions.attr_dict_vars import AttrDictVars


class FileAttrDictVars(AttrDictVars, MutableMapping):  # type: ignore
    """Dual access vars in a file.

    File contains vars as `key=value` lines.
    Access with attributes or as dict.

    With attributes, you can only access explicitly declared vars,
    with dict-like access you can access any var.
    This way you can find your balance between strictly defined vars and flexibility.

    Usage:
       class MyVars(FileAttrDictVars):
           documented_var: str

       vars = MyVars(Path("my_vars.txt"))
       vars["undocumented_var"] = "value1"
       vars.documented_var == "value2"

       # Produces "my_vars.txt" with:
       #    documented-var=value2
       #    undocumented_var=value1


    On read/write, it converts var names with `_name_from_external()`/`_external_name()` methods.
    They remove/add `_external_name_prefix` to the names.

    Attribute access also uses `_attr_to_var_name()` - by default it converts Python attribute names
    from snake_case to kebab-case.
    """

    def __init__(self, vars_file: Path, *, prefix: str = "") -> None:
        """Init the vars file and prefix."""
        self._external_name_prefix = prefix
        self._vars_file: Path = vars_file
        self._var_keys_cache: Optional[Dict[str, str]] = None

    def _external_name(self, name: str) -> str:
        """Convert variable name to the external form."""
        return self._external_name_prefix + name

    def _name_from_external(self, name: str) -> str:
        """Convert external variable name to the internal form."""
        return name[len(self._external_name_prefix) :]

    def __getattribute__(self, name: str) -> Any:
        try:
            return object.__getattribute__(self, name)
        except AttributeError as exc:
            type_hints = self.__class__.get_type_hints()
            if name in type_hints:
                var_name = self._attr_to_var_name(name)
                value = self[var_name]
                self.__dict__[var_name] = value
                return value
            raise AttributeError(f"Unknown {name}") from exc

    def __getitem__(self, key: str) -> str:
        try:
            return self._get_var_keys[key]
        except KeyError:
            self._get_var_keys[key] = ""
            self._save_var_file()
            print(f"Variable `{key}` not found in `{self._vars_file}`")
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
        type_hints = self.__class__.get_type_hints()
        if not name.startswith("_"):
            if name not in type_hints:
                raise AttributeError(f"Unknown {name}")
            self[self._attr_to_var_name(name)] = value
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
        if self._var_keys_cache is None:
            try:
                content = self._vars_file.read_text(encoding="utf-8")
                self._var_keys_cache = {
                    self._name_from_external(k): v
                    for k, v in (line.split("=", 1) for line in content.splitlines() if "=" in line)
                }
            except FileNotFoundError:
                self._var_keys_cache = {}
        return self._var_keys_cache

    def _save_var_file(self) -> None:
        self._vars_file.parent.mkdir(parents=True, exist_ok=True)
        lines: List[str] = [
            f"{self._external_name(key)}={value}" for key, value in self._get_var_keys.items()
        ]
        self._vars_file.write_text("\n".join(lines), encoding="utf-8")
