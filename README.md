[![Build Status](https://github.com/andgineer/github-custom-actions/workflows/CI/badge.svg)](https://github.com/andgineer/github-custom-actions/actions)
[![Coverage](https://raw.githubusercontent.com/andgineer/github-custom-actions/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/andgineer/github-custom-actions/blob/python-coverage-comment-action-data/htmlcov/index.html)
# github-custom-actions

Python package for creating [custom GitHub Actions](https://docs.github.com/en/actions/creating-actions/about-custom-actions). 

#### Example of usage

```python
from github_custom_actions import ActionBase, ActionInputs

class MyInputs(ActionInputs):
    my_input: str
    """My input description"""
    
    my_path: Path
    """My path description"""

class MyAction(ActionBase):
    def __init__(self):
        super().__init__(inputs=MyInputs())
        if self.inputs.my_path is None:
            raise ValueError("my_path is required")

    def main(self):
        self.inputs.my_path.mkdir(exist_ok=True)
        self.outputs["RUNNER_OS"] = self.vars.runner_os
        self.summary.text += (
            self.render(
                "### {{ inputs.my_input }}.\n"
                "Have a nice day!"
            )
        )

if __name__ == "__main__":
    MyAction().run()
```
# Documentation

[Github Custom Actions](https://andgineer.github.io/github-custom-actions/)

# Developers

Do not forget to run `. ./activate.sh`.

# Scripts
Install [invoke](https://docs.pyinvoke.org/en/stable/) preferably with [pipx](https://pypa.github.io/pipx/):

    pipx install invoke

For a list of available scripts run:

    invoke --list

For more information about a script run:

    invoke <script> --help

## Coverage report
* [Codecov](https://app.codecov.io/gh/andgineer/github-custom-actions/tree/main/src%2Fgithub_custom_actions)
* [Coveralls](https://coveralls.io/github/andgineer/github-custom-actions)

> Created with cookiecutter using [template](https://github.com/andgineer/cookiecutter-python-package)