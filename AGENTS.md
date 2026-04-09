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

## Repo Identity

This repository currently publishes the Python package
`pipeworks-conditional-axis` from the workspace
`pipeworks_entity_state_generation`.

The current codebase is best understood as:

- a deterministic Python library under `src/condition_axis/`
- an optional FastAPI adapter in the repo root at `entity_api.py`
- a future Luminal-host candidate that should be treated deliberately, not as
  an already-hosted service

Do not assume the repo name, package name, import path, and service name are
fully normalized yet. The naming cleanup to a `pipeworks-entity-state-generation`
shape is future work unless the current task explicitly includes it.

## Luminal Host Posture

Follow the current host policy in
`/home/aapark/dotfiles/docs/policies/luminal_host_service_topology_policy.md`.

That policy means:

- `luminal.local` is a shared multi-project host, not a single-project box
- repo-specific runtime environments should be explicit and isolated
- browser-facing services should not invent direct-port access as the canonical
  model
- localhost-bound backends behind nginx are the normal target posture when a
  service is intentionally hosted
- hostnames, systemd units, and nginx vhosts should be introduced only when the
  rollout is explicit and justified

For this repository, that translates to:

- create and use its own dedicated virtual environment under
  `/srv/work/pipeworks/venvs/`
- do not treat `entity_api.py` as an already-approved long-running Luminal
  service unless the current task explicitly performs that rollout
- keep host-environment planning separate from ad hoc library hacking

## Dedicated Virtual Environment

The intended Luminal repo-specific environment for this repository is:

- `/srv/work/pipeworks/venvs/pw-entity-state-generation`

Use that path for repo-local development, validation, and any future host
promotion work. Do not reuse `pw-core`, `pw-mud-server`, `pw-namegen-api`, or
other neighboring PipeWorks environments for this repo.

Expected setup shape on Luminal:

```bash
sudo -u pipeworks /usr/bin/python3 -m venv /srv/work/pipeworks/venvs/pw-entity-state-generation
/srv/work/pipeworks/venvs/pw-entity-state-generation/bin/python -m pip install --upgrade pip
/srv/work/pipeworks/venvs/pw-entity-state-generation/bin/python -m pip install -e '.[dev]'
```

If docs tooling is needed:

```bash
/srv/work/pipeworks/venvs/pw-entity-state-generation/bin/python -m pip install -e '.[dev,docs]'
```

When writing runbooks, docs, or rollout notes for Luminal, prefer that exact
venv path unless there is an explicit migration decision that changes it.

## Project Structure

The actual source layout is:

- `src/condition_axis/__init__.py` exposes the public package API
- `src/condition_axis/_base.py` holds shared sampling and normalization helpers
- `src/condition_axis/character_conditions.py` implements character-state axis
  generation
- `src/condition_axis/occupation_axis.py` implements occupation-axis generation
- `entity_api.py` provides the FastAPI HTTP adapter around the library

Other important repo areas:

- `tests/` contains unit, integration, example, and version-sync coverage
- `examples/` contains runnable usage demos
- `docs/` contains the Sphinx documentation source
- `pyproject.toml` is the primary packaging and tool configuration file
- `pytest.ini` exists and is still active for pytest discovery/addopts

Do not copy assumptions from other PipeWorks repos that use a `src/<package>/web`
or multi-app service layout. This repo is flatter and currently mixes library
and API adapter concerns in one repository.

## Build, Test, and Development Commands

Prefer the dedicated environment binaries explicitly:

```bash
/srv/work/pipeworks/venvs/pw-entity-state-generation/bin/python -m pip install -e '.[dev]'
/srv/work/pipeworks/venvs/pw-entity-state-generation/bin/python -m pip install -e '.[dev,docs]'
/srv/work/pipeworks/venvs/pw-entity-state-generation/bin/python -m pytest -v
/srv/work/pipeworks/venvs/pw-entity-state-generation/bin/python -m pytest -m "not slow" -v
/srv/work/pipeworks/venvs/pw-entity-state-generation/bin/python -m pytest --cov=condition_axis --cov-report=term-missing --cov-report=xml
/srv/work/pipeworks/venvs/pw-entity-state-generation/bin/python -m ruff check src tests examples entity_api.py
/srv/work/pipeworks/venvs/pw-entity-state-generation/bin/python -m black src tests examples entity_api.py
/srv/work/pipeworks/venvs/pw-entity-state-generation/bin/python -m mypy src
/srv/work/pipeworks/venvs/pw-entity-state-generation/bin/pre-commit run --all-files
/srv/work/pipeworks/venvs/pw-entity-state-generation/bin/python -m build
make -C docs html
```

For quick local API verification without host rollout:

```bash
/srv/work/pipeworks/venvs/pw-entity-state-generation/bin/python -m uvicorn entity_api:app --host 127.0.0.1 --port 8400
```

Use localhost binding for ad hoc API runs unless the task explicitly requires a
different posture.

## Coding Style And Naming Conventions

Follow the tool configuration in `pyproject.toml`:

- Black line length is `100`
- Ruff targets Python `3.12`
- Mypy is enabled for `src`

General repo conventions:

- use type hints on public functions and stable adapter contracts
- keep module-level constants uppercase
- use `snake_case` for modules, functions, and variables
- use `PascalCase` for classes and Pydantic/FastAPI models
- keep docstrings concise and behavior-focused

Because this repo feeds deterministic generation and adapter contracts:

- avoid casual renaming of payload keys or axis labels
- treat API response fields as compatibility-sensitive
- preserve deterministic behavior for seeded generation unless the task
  explicitly changes the contract

## Testing Guidelines

Pytest markers currently present in `pytest.ini` are:

- `unit`
- `integration`
- `slow`

There are also example coverage tests and version-sync checks in `tests/`.

When changing behavior:

- add or update unit tests first for deterministic logic changes
- update `tests/test_entity_api.py` for adapter contract changes
- update `tests/test_examples.py` when example behavior or public usage changes
- keep coverage-sensitive changes accompanied by relevant tests

Do not remove or relabel slow/integration tests merely to make CI faster.

## API And Service Guidance

`entity_api.py` is an adapter surface, not proof that this repo already has an
approved Luminal production shape.

If the task is about local development only:

- use localhost-bound ad hoc runs
- keep changes repo-scoped
- do not invent nginx/systemd/certificate assets unless requested

If the task is about promoting this repo into the Luminal host environment:

- prefer a dedicated repo-specific venv first
- define the backend bind, hostname, config ownership, and service boundaries
  explicitly
- align with the Luminal host topology policy before creating a vhost or unit
- document host-owned config/runtime paths outside the repo rather than
  smuggling them into source control as if they were app defaults

## CI, Coverage, And Release Notes

This repo currently carries:

- GitHub Actions CI
- coverage reporting via `pytest-cov` and `codecov.yml`
- release tracking via `release-please-config.json` and `CHANGELOG.md`

When touching CI, release, or coverage behavior:

- preserve org-required checks
- keep release automation inputs coherent
- do not silently change package identity, release naming, or coverage scope
  unless the task explicitly calls for it

## Commit And Pull Request Guidance

Use Conventional Commits consistent with the surrounding PipeWorks repos, for
example:

- `feat(api): ...`
- `fix(axes): ...`
- `fix(config): ...`
- `docs(agents): ...`
- `chore(ci): ...`

Keep commits scoped to one concern. PRs should include:

- what changed
- why it changed
- any host-topology impact on Luminal
- the exact validation commands run

Because this repo uses squash merges together with `release-please`, the PR
title must itself use a releasable Conventional Commit prefix such as
`feat(...)`, `fix(...)`, `perf(...)`, or `docs(...)`. A non-conventional squash
merge title on `main` can prevent the next release PR from being generated.

If a change starts introducing the dedicated Luminal environment for this repo,
call that out explicitly in the PR so neighboring PipeWorks repos are not left
guessing which venv or host posture is now canonical.
