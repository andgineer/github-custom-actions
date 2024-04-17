import os

from github_custom_actions.github_vars import GithubVars
import pytest


def test_github_vars_lazy_load():
    vars = GithubVars()
    with pytest.raises(AttributeError):
        assert vars.github_action == "test"
    os.environ["GITHUB_ACTION"] = "test"
    assert vars.github_action == "test"
    del os.environ["GITHUB_ACTION"]
    assert vars.github_action == "test"  # Cached value


def test_github_vars_undescribed_variable():
    vars = GithubVars()
    os.environ["GITHUB_UNKNOWN"] = "test"
    with pytest.raises(AttributeError, match=r"Undefined github_unknown"):
        assert vars.github_unknown == "test"


def test_github_vars_path_variable():
    vars = GithubVars()
    os.environ["GITHUB_OUTPUT"] = "a/b"
    assert str(vars.github_output.parent) == "a"
