# Repository Guidelines

## Project Structure & Module Organization
- `src/kantharos_bot/` holds the Discord bot packages; commands live under `src/kantharos_bot/commands/` and shared helpers in `src/kantharos_bot/utils/`.
- `config/settings.toml` defines the Dynaconf base settings; copy `config/.secrets_template.toml` when provisioning secrets.
- `help_texts/` stores user-facing text snippets consumed by commands.
- `tests/` contains pytest suites mirroring the runtime package layout.

## Build, Test, and Development Commands
- `pdm install` resolves project and dev dependencies defined in `pyproject.toml`.
- `pdm run kantharos-bot` launches the bot via the `kantharos_bot.main:main` entry point.
- `pdm run pytest` executes the automated test suite with coverage hooks.
- `pdm run black .` and `pdm run isort .` apply formatting; pair with `pdm run pylint ./**/*.py` for static analysis.
- `pdm run pre-commit run --all-files` mirrors the full lint pipeline before pushing.

## Coding Style & Naming Conventions
- Format Python code with Black (line length 100) and isort using the `hug` profile; rely on `pre-commit` to enforce both.
- Follow Pylint’s defaults: modules and functions in `snake_case`, constants in `UPPER_CASE`, and keep lines under 100 characters.
- Place bot command modules under `commands/` and utility helpers under `utils/`; keep filenames descriptive (e.g., `match_tracker.py`).

## Testing Guidelines
- Write tests with pytest; locate new suites in `tests/`, named `test_<feature>.py`.
- Use fixtures to mock Discord and API clients; prefer deterministic data to external calls.
- Aim for branch-aware coverage (`coverage` is preconfigured) and verify with `pdm run coverage run -m pytest` followed by `pdm run coverage report` when touching critical modules.

## Commit & Pull Request Guidelines
- Follow the repository pattern of short, imperative commit subjects (e.g., `update docker workflow`).
- Ensure commits stay focused; stage related linting changes alongside code updates.
- In pull requests, include a concise summary, testing notes (`pdm run pytest` output), and reference relevant issues or screenshots for user-visible changes.

## Configuration & Secrets
- Store environment-specific overrides in `config/.secrets.toml`; never commit real tokens.
- When deploying or sharing the bot, provide instructions for generating API keys and updating Dynaconf layers securely.
