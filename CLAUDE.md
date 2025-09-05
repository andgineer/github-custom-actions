# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python package for creating custom GitHub Actions. The main entry point is the `ActionBase` class which provides a framework for building GitHub Actions with typed inputs/outputs, environment variable access, and templating capabilities using Jinja2.

## Development Setup

Source code is in `src/github_custom_actions/`, tests in `tests/`. Always run `. ./activate.sh` before development to set up the environment.

## Common Commands

### Testing
```bash
python -m pytest --junitxml=pytest.xml --cov-report=term-missing:skip-covered --cov=src tests/
```

### Linting and Type Checking
```bash
source activate.sh   # Always run this first before any development commands
invoke pre           # Run pre-commit checks (ruff + mypy)
ruff check --fix    # Run ruff linter with fixes
```

**Important**: Always run `source activate.sh` before any development commands. Never run `mypy` directly - use `invoke pre` instead.

### Requirements Management
```bash
invoke reqs                    # Upgrade requirements and install
invoke compile-requirements   # Compile requirements.in to requirements.txt
```

### Building and Publishing
```bash
python -m build              # Build package
invoke version              # Show current version
invoke ver-release          # Bump release version
invoke ver-feature          # Bump feature version
invoke ver-bug             # Bump bug fix version
```

### Documentation
```bash
invoke docs-en    # Start docs server and open browser
invoke docs-ru    # Russian docs preview
```

## Core Architecture

- `ActionBase`: Main class for creating GitHub Actions. Subclass and implement `main()` method
- `ActionInputs`/`ActionOutputs`: Type-safe input/output handling for actions
- `GithubVars`: Access to GitHub environment variables (runner OS, workspace, etc.)
- Property descriptors for file-based properties (`summary`, `step_summary`)
- Jinja2 templating support via `render()` method

The package uses a descriptor-based approach for file properties, allowing actions to read/write GitHub's step summary and other files transparently.

## Code Style

- Line length: 100 characters (99 for tests)
- Uses ruff for linting with extensive rule set
- Type hints required (enforced by mypy)
- Pre-commit hooks enforce formatting and linting
- Tests exclude type checking but follow formatting rules
