"""Python package for creating custom GitHub Actions.

The file is mandatory for build system to find the package.
"""

from github_custom_actions.inputs_outputs import ActionInputs, ActionOutputs
from github_custom_actions.action_base import ActionBase
from github_custom_actions.github_vars import GithubVars
from github_custom_actions.__about__ import __version__

__all__ = ["ActionInputs", "ActionOutputs", "ActionBase", "GithubVars", "__version__"]
