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
