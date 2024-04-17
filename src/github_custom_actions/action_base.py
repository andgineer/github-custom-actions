import sys
import traceback

from github_custom_actions.inputs_outputs import ActionOutputs, ActionInputs
from github_custom_actions.github_vars import GithubVars


class ActionBase:
    """Base class for GitHub Actions.

    Implement main() method in the subclass.
    """

    def __init__(self, inputs: ActionInputs = ActionInputs()):
        self.inputs = inputs
        self.outputs = ActionOutputs()
        self.vars = GithubVars()

    def main(self) -> None:
        """Main method."""
        raise NotImplementedError

    def run(self) -> None:
        """Run main method."""
        try:
            self.main()
        except Exception:  # pylint: disable=broad-except
            traceback.print_exc(file=sys.stderr)
            sys.exit(1)
