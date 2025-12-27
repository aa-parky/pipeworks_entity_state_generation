# GitHub Actions CI Setup Guide

This guide explains the three GitHub Actions workflows that have been configured for the `pipeworks-conditional-axis` project.

## Overview

Three automated workflows have been set up to ensure code quality and enable continuous integration:

1. **Tests** (`test.yml`) - Runs pytest on Python 3.12 and 3.13
2. **Lint & Type Check** (`lint.yml`) - Runs Ruff, Black, and MyPy
3. **Build & Publish** (`publish.yml`) - Builds and publishes to PyPI

## Workflow Files

### 1. `.github/workflows/test.yml` - Tests

**Purpose**: Run the test suite on multiple Python versions to ensure compatibility.

**Triggers**:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

**What it does**:
- Sets up Python 3.12 and 3.13 environments
- Installs the package with dev dependencies
- Runs pytest with coverage reporting
- Uploads coverage to Codecov (if using Codecov)

**Matrix Testing**: Tests run on both Python 3.12 and 3.13 to ensure compatibility.

### 2. `.github/workflows/lint.yml` - Linting & Type Checking

**Purpose**: Ensure code quality, formatting, and type safety.

**Triggers**:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

**What it does**:
- **Ruff Linter**: Checks for code style violations
- **Black Formatter**: Verifies code is properly formatted
- **MyPy Type Checker**: Performs static type checking

**Jobs** (run in parallel):
- `lint`: Checks code style with Ruff
- `format`: Checks formatting with Black
- `type-check`: Performs type checking with MyPy

### 3. `.github/workflows/publish.yml` - Build & Publish

**Purpose**: Build the package and publish to PyPI.

**Triggers**:
- When a GitHub release is created (automatic publish to PyPI)
- Manual workflow dispatch (publish to TestPyPI for testing)

**What it does**:
- Builds the distribution package
- Publishes to PyPI on release (requires PyPI token)
- Can publish to TestPyPI for testing (manual trigger)

**Environment**: Uses trusted publishing (OIDC) for secure PyPI authentication.

## Setup Instructions

### Step 1: Create the Workflow Files

Copy the three workflow files to your repository:

```bash
.github/workflows/
├── test.yml
├── lint.yml
└── publish.yml
```

### Step 2: Commit and Push

```bash
git add .github/
git commit -m "ci: add GitHub Actions workflows"
git push origin main
```

### Step 3: Verify Workflows

1. Go to your GitHub repository
2. Click on the **Actions** tab
3. You should see the workflows running

### Step 4: Set Up PyPI Publishing (Optional)

To enable automatic publishing to PyPI on release:

1. **Create a PyPI Account** (if you don't have one):
   - Go to https://pypi.org/account/register/
   - Create an account

2. **Configure Trusted Publishing**:
   - Go to https://pypi.org/manage/account/publishing/
   - Add a new pending publisher:
     - PyPI Project Name: `pipeworks-conditional-axis`
     - GitHub Repository Owner: `aa-parky`
     - Repository Name: `pipeworks_conditional_axis`
     - Workflow Name: `publish.yml`
     - Environment Name: `pypi`

3. **Create a Release on GitHub**:
   - Go to your repository
   - Click **Releases** → **Create a new release**
   - Tag version: `v1.0.0`
   - Release title: `Version 1.0.0`
   - Click **Publish release**
   - The workflow will automatically build and publish to PyPI

## Workflow Status Badges

You can add status badges to your README to show the CI status:

```markdown
[![Tests](https://github.com/aa-parky/pipeworks_conditional_axis/actions/workflows/test.yml/badge.svg)](https://github.com/aa-parky/pipeworks_conditional_axis/actions/workflows/test.yml)
[![Lint & Type Check](https://github.com/aa-parky/pipeworks_conditional_axis/actions/workflows/lint.yml/badge.svg)](https://github.com/aa-parky/pipeworks_conditional_axis/actions/workflows/lint.yml)
```

## Customization

### Changing Trigger Branches

To add more branches or change which branches trigger workflows, edit the `on:` section:

```yaml
on:
  push:
    branches: [main, develop, staging]  # Add more branches here
  pull_request:
    branches: [main, develop, staging]
```

### Changing Python Versions

To test on different Python versions, edit the `matrix.python-version`:

```yaml
strategy:
  matrix:
    python-version: ["3.11", "3.12", "3.13"]  # Add or remove versions
```

### Adding More Checks

You can add more jobs to the lint workflow:

```yaml
jobs:
  lint:
    # ... existing lint job ...

  security:
    name: Security check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install bandit
      - run: bandit -r src/
```

## Troubleshooting

### Workflow Not Running

- Check that the workflow file is in `.github/workflows/`
- Verify the YAML syntax is correct
- Check the trigger conditions (branches, events)
- Go to **Actions** tab to see error details

### Tests Failing

- Check the test output in the **Actions** tab
- Run tests locally: `pytest tests/ -v`
- Fix the issues and push again

### Linting Failures

- Run linters locally:
  - `ruff check src/ tests/`
  - `black --check src/ tests/`
  - `mypy src/`
- Fix issues and commit

### PyPI Publishing Not Working

- Verify the PyPI token is configured correctly
- Check that the version number is new (not already published)
- Ensure the package name matches in `pyproject.toml`

## Best Practices

1. **Always run tests locally before pushing**: `pytest tests/ -v`
2. **Use pre-commit hooks**: Catch issues before they reach CI
3. **Review CI failures**: Don't ignore CI failures in PRs
4. **Keep dependencies updated**: Periodically update tool versions
5. **Monitor workflow performance**: Optimize slow workflows

## Next Steps

1. Commit the workflow files to your repository
2. Push to GitHub and verify workflows run
3. Add status badges to your README
4. Configure PyPI publishing if you plan to publish to PyPI
5. Monitor the Actions tab for workflow results

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [PyPA Publishing Guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Black Documentation](https://black.readthedocs.io/)
- [MyPy Documentation](https://mypy.readthedocs.io/)
