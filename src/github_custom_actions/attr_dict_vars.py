import typing
from typing import Dict, Any


class AttrDictVars:
    """Common base class for accessing variables as attributes or dict."""

    _type_hints_cache: Dict[str, Dict[str, Any]] = {}
    _external_name_prefix = ""

    @classmethod
    def _get_type_hints(cls) -> Dict[str, Any]:
        class_name = cls.__name__
        if class_name not in cls._type_hints_cache:
            cls._type_hints_cache[class_name] = typing.get_type_hints(cls)
        return cls._type_hints_cache[class_name]

    def _attr_to_var_name(self, name: str) -> str:
        return name.replace("_", "-")
