# AGENTS.md

## Foundation Must-Dos (Org-Wide)

Read and apply these before repo-specific instructions:

- Local workspace path: `../.github/.github/docs/AGENT_FOUNDATION.md`
- Local workspace path: `../.github/.github/docs/TEST_TAGGING_AND_GITHUB_CHECKLIST.md`
- Canonical URL: `https://github.com/pipe-works/.github/blob/main/.github/docs/AGENT_FOUNDATION.md`
- Canonical URL: `https://github.com/pipe-works/.github/blob/main/.github/docs/TEST_TAGGING_AND_GITHUB_CHECKLIST.md`

Mandatory requirements:

1. Run the GitHub preflight checklist before any `gh` interaction, CI edits, or
   test-tag changes.
2. Preserve required checks (`All Checks Passed`, `Secret Scan (Gitleaks)`).
3. Do not weaken test-tag semantics to reduce runtime.
4. Keep CI optimization changes evidence-based (run IDs, timings, check states).

## Project Structure & Module Organization

Core library code lives in `src/condition_axis/`:

- `character_conditions.py` and `occupation_axis.py` implement axis systems.
- `_base.py` contains shared generation utilities.
- `__init__.py` exposes the public API.

Tests are in `tests/` (including `tests/test_examples.py` for runnable examples).
Usage demos are in `examples/`. Documentation sources are in `docs/` (Sphinx).
Packaging and tool configuration are in `pyproject.toml`, `pytest.ini`,
and `.pre-commit-config.yaml`.

## Build, Test, and Development Commands

Use Python 3.12+.

```bash
pip install -e ".[dev]"          # local dev install
pip install -e ".[dev,docs]"     # include docs tooling
pytest -v                         # run full test suite
pytest -m "not slow" -v           # skip slow tests
pytest --cov=condition_axis --cov-report=term-missing --cov-report=xml
ruff check src tests examples
black src tests examples
mypy src
pre-commit run --all-files
python -m build                   # build sdist/wheel
make -C docs html                 # build Sphinx docs
```

## Coding Style & Naming Conventions

Follow Black formatting (line length 100) and Ruff lint rules configured in
`pyproject.toml`. Use type hints on public functions and keep module-level
constants uppercase (for example, `CONDITION_AXES`, `WEIGHTS`). Use `snake_case`
for files, functions, and variables; use `PascalCase` for classes. Keep
docstrings concise and behavior-focused.

## Testing Guidelines

Pytest discovers tests with `test_*.py`, `Test*`, and `test_*` patterns.
Use markers consistently: `unit`, `integration`, `slow`, and `requires_model`.
Add unit tests for all behavior changes and update example tests when public
API behavior changes. CI enforces an 80% coverage threshold, so include
coverage-relevant tests with each PR.

## CI, Coverage, and Scheduling

- CI uses the shared reusable workflow (`.github/workflows/ci.yml`).
- Matrix/coverage lanes use fast marker routing (`not slow and not requires_model`).
- Weekly schedule (`cron`) runs a full-sweep CI pass on the default branch.
- Content-only skip behavior is not currently enabled in this repository.

## Commit & Pull Request Guidelines

Use Conventional Commits, consistent with project history:

- `feat(scope): ...`
- `fix(scope): ...`
- `chore: ...`
- `docs: ...`

Keep commits focused and descriptive. PRs should include: what changed, why it
changed, linked issue(s), and test evidence (commands run and results). Ensure
CI passes for lint, tests, security checks, docs, and packaging before merge.
