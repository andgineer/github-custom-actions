from pathlib import Path

from github_custom_actions.inputs_outputs import ActionOutputs, ActionInputs


class ActionBase:
    @property
    def output(self) -> ActionOutputs:
        """Get Action Output."""
        return ActionOutputs()

    @property
    def input(self) -> ActionInputs:
        """Get Action Input."""
        return ActionInputs()

    def get_input_path(self, name: str) -> Path:
        """Get Action Input value as Path."""
        path_str = self.input[name]
        if not path_str:
            raise ValueError(f"Parameter `{name}` cannot be empty.")
        return Path(path_str)
