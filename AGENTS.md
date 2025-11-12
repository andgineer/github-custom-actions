# Repository Guidelines

## Project Structure & Module Organization
Source lives in `src/github_custom_actions/`, organized by action helpers, render utilities, and the `__about__.py` version file consumed by Hatch. Tests are in `tests/`, mirroring module names (`test_action_base.py`, etc.) and relying on `pytest` discovery. Supporting assets sit under `docs/src/<lang>/`, while automation helpers (version bumping, doc builds) are in `scripts/`. High-level Invoke recipes reside in `tasks.py`, and CI configs read from `pyproject.toml`, `pytest.ini`, and `invoke.yml`.

## Build, Test & Development Commands
Run `. ./activate.sh` to create/enter `.venv` with Python 3.8 and install dev dependencies via `uv`. Use `invoke --list` to discover helper tasks. Typical workflows: `invoke pre` for the full pre-commit suite, `pytest` (or `pytest tests/test_action_base.py -k render`) for targeted runs, `invoke reqs` to refresh dependency pins, and `invoke docs-en` to preview MkDocs locally after syncing images via `scripts/docs-render-config.sh`. Version bumps go through `invoke ver-release|feature|bug` which call the corresponding `scripts/verup.sh` automation.

## Coding Style & Naming Conventions
Follow standard PEP 8 with 4-space indentation and prefer explicit type hints for public APIs. `ruff` enforces a 99-character line limit (`pyproject.toml`) and should stay clean before committing; run it via `invoke pre` or directly with `ruff check .`. Modules use snake_case filenames, classes stay in PascalCase, and user-facing action inputs/outputs mirror GitHub Action casing conventions. Keep Jinja templates and action summaries in plain Markdown so they render cleanly inside GitHub summaries.

## Testing Guidelines
`pytest` is configured with `--doctest-modules` (`pytest.ini`), so keep docstrings executable. Add unit tests that mirror the structure under `tests/`, naming files `test_<module>.py` and functions `test_<behavior>`. When introducing an action helper, provide both a pure unit test and, where feasible, an integration-style test that exercises `ActionBase.run`. Maintain coverage parity with `main`; check the GitHub badges or run `pytest --cov=github_custom_actions` locally before pushing.

## Commit & Pull Request Guidelines
Recent history favors short, imperative summaries (`mypy`, `upload-artifact@v4`, `ruff lint`). Keep titles under ~60 chars and avoid punctuation unless referencing a tool. Reference issues in the body using `Closes #123` when applicable. Each PR should describe intent, list notable commands run (`invoke pre`, `pytest`), and link to doc previews or attach screenshots when altering rendered output. Do not push secrets or GitHub tokens; rely on local `.env` files ignored by git and double-check generated artifacts before committing.
