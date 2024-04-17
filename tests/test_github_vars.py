import os

from github_custom_actions.github_vars import GithubVars
import pytest


def test_lazy_load():
    vars = GithubVars()
    with pytest.raises(AttributeError):
        vars.github_repository
    os.environ["GITHUB_REPOSITORY"] = "test"
    assert vars.github_repository == "test"
    del os.environ["GITHUB_REPOSITORY"]
    assert vars.github_repository == "test"  # Cached value
