# Installation

Python package for creating [custom GitHub Actions](https://docs.github.com/en/actions/creating-actions/about-custom-actions). 

Supports Python 3.7 and higher for very only self-hosted action runners.

- [Example of usage](https://github.com/andgineer/allure-report)

## Installation

## Installing pipx
[`pipx`](https://pypa.github.io/pipx/) creates isolated environments to avoid conflicts with existing system packages.

=== "MacOS"
    In the terminal, execute:
    ```bash
    brew install pipx
    pipx ensurepath
    ```

=== "Linux"
    First, ensure Python is installed.

    Enter in the terminal:

    ```bash
    python3 -m pip install --user pipx
    python3 -m pipx ensurepath
    ```

=== "Windows"
    First, install Python if it's not already installed.

    In the command prompt, type (if Python was installed from the Microsoft Store, use `python3` instead of `python`):
    
    ```bash
    python -m pip install --user pipx
    ```

## Installing `github-custom-actions`:
In the terminal (command prompt), execute:

```bash
pipx install github-custom-actions
```

### Advanced

Use 
```bash
github-custom-actions --help
```
to see all available options.