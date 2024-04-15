from pathlib import Path

from github_custom_actions.inputs_outputs import OutputProxy, InputProxy


class ActionBase:
    @property
    def output(self) -> OutputProxy:
        """Get Action Output."""
        return OutputProxy()

    @property
    def input(self) -> InputProxy:
        """Get Action Input."""
        return InputProxy()

    def get_input_path(self, name: str) -> Path:
        """Get Action Input value as Path."""
        path_str = self.input[name]
        if not path_str:
            raise ValueError(f"Parameter `{name}` cannot be empty.")
        return Path(path_str)
