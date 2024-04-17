import os

from github_custom_actions.github_vars import GithubVars
import pytest


def test_github_vars_lazy_load(monkeypatch):
    vars = GithubVars()

    monkeypatch.delenv("GITHUB_ACTION", raising=False)
    with pytest.raises(AttributeError):
        assert vars.github_action == "test"

    monkeypatch.setenv("GITHUB_ACTION", "test")
    assert vars.github_action == "test"

    monkeypatch.delenv("GITHUB_ACTION")
    assert vars.github_action == "test"  # Cached value


def test_github_vars_unknown():
    vars = GithubVars()
    os.environ["GITHUB_UNKNOWN"] = "test"
    with pytest.raises(AttributeError, match=r"Unknown github_unknown"):
        assert vars.github_unknown == "test"


def test_github_vars_path_variable(monkeypatch):
    vars = GithubVars()
    monkeypatch.setenv("GITHUB_OUTPUT", "a/b")
    assert str(vars.github_output.parent) == "a"


def test_github_vars_empty_path(monkeypatch):
    vars = GithubVars()
    monkeypatch.setenv("GITHUB_OUTPUT", "")
    assert vars.github_output is None
