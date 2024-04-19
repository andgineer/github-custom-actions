# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/andgineer/github-custom-actions/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                  |    Stmts |     Miss |   Cover |   Missing |
|------------------------------------------------------ | -------: | -------: | ------: | --------: |
| src/github\_custom\_actions/\_\_about\_\_.py          |        1 |        0 |    100% |           |
| src/github\_custom\_actions/action\_base.py           |       38 |       12 |     68% |25-26, 32-34, 52, 56-60, 64 |
| src/github\_custom\_actions/env\_attr\_dict\_vars.py  |       46 |        5 |     89% |73, 76, 82, 94, 97 |
| src/github\_custom\_actions/file\_attr\_dict\_vars.py |       71 |        0 |    100% |           |
| src/github\_custom\_actions/github\_vars.py           |       89 |        0 |    100% |           |
| src/github\_custom\_actions/inputs\_outputs.py        |       64 |        7 |     89% |93, 100-101, 104, 107, 110, 118 |
|                                             **TOTAL** |  **309** |   **24** | **92%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/andgineer/github-custom-actions/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/andgineer/github-custom-actions/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/andgineer/github-custom-actions/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/andgineer/github-custom-actions/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Fandgineer%2Fgithub-custom-actions%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/andgineer/github-custom-actions/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.