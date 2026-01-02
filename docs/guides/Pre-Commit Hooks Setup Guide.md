# Pre-Commit Hooks Setup Guide

This guide walks you through setting up pre-commit hooks for the `pipeworks-conditional-axis` project. Pre-commit hooks automatically run code quality checks before each commit, ensuring code consistency and catching errors early.

## What Are Pre-Commit Hooks?

Pre-commit hooks are scripts that run automatically before you commit code to Git. They can check for issues, format code, and prevent commits that don't meet your project's standards. This saves time by catching problems before they enter your repository.

## What Hooks Are Configured?

The project's `.pre-commit-config.yaml` includes the following hooks:

| Hook | Purpose | Action |
|------|---------|--------|
| **Trailing Whitespace** | Removes trailing whitespace from files | Auto-fixes |
| **End of File Fixer** | Ensures files end with a newline | Auto-fixes |
| **YAML Checker** | Validates YAML syntax | Fails if invalid |
| **TOML Checker** | Validates TOML syntax | Fails if invalid |
| **JSON Checker** | Validates JSON syntax | Fails if invalid |
| **Merge Conflict Checker** | Detects unresolved merge conflicts | Fails if found |
| **Debug Statements** | Detects `breakpoint()` and debugger imports | Fails if found |
| **Black Formatter** | Formats Python code consistently | Auto-fixes |
| **Ruff Linter** | Checks for code style violations | Auto-fixes when possible |
| **MyPy Type Checker** | Performs static type checking | Fails if type errors |
| **Bandit Security** | Checks for security vulnerabilities | Fails if found |
| **Interrogate** | Checks docstring coverage (manual stage) | Informational |

## Step-by-Step Setup

### Step 1: Ensure Development Dependencies Are Installed

First, make sure you have all development dependencies installed, including `pre-commit`:

```bash
pip install -e ".[dev]"
```

This command installs the package in editable mode and includes all development tools. You can verify that `pre-commit` is installed by running:

```bash
pre-commit --version
```

You should see output like `pre-commit 3.x.x`.

### Step 2: Install the Git Hooks

Navigate to the root of your repository and install the pre-commit hooks:

```bash
cd /path/to/pipeworks_conditional_axis
pre-commit install
```

This command creates symbolic links in your `.git/hooks/` directory that will execute the hooks before each commit. You should see output like:

```
pre-commit installed at .git/hooks/pre-commit
```

### Step 3: Verify Installation

To verify that the hooks are installed correctly, check that the hook files exist:

```bash
ls -la .git/hooks/pre-commit
```

You should see a file named `pre-commit` in the `.git/hooks/` directory.

### Step 4: Test the Hooks (Optional but Recommended)

Before making your first commit, you can test all hooks on all files to see if there are any issues:

```bash
pre-commit run --all-files
```

This command runs all hooks on all files in the repository. It will show you any issues that need to be fixed. Many hooks will auto-fix issues (like formatting), while others will report errors that require manual intervention.

## Using Pre-Commit Hooks in Your Workflow

### Normal Commit Workflow

Once the hooks are installed, they run automatically before each commit:

```bash
git add .
git commit -m "Your commit message"
```

If all hooks pass, your commit will proceed normally. If any hook fails, the commit will be aborted, and you'll see output like:

```
Trim trailing whitespace.................................................................Passed
Fix end of file..........................................................................Passed
Check YAML..............................................................................Passed
Black code formatter....................................................................Failed
- hook id: black
- exit code: 1

Files were modified by this hook. Additional output:
reformatted src/condition_axis/example.py
```

### Handling Hook Failures

If a hook fails, follow these steps:

1.  **Review the output**: The hook will tell you what failed and why.
2.  **Fix the issues**: Many hooks auto-fix issues (like `black` reformatting). For others, you'll need to fix them manually.
3.  **Stage the fixed files**: If the hook auto-fixed files, stage them again:
    ```bash
    git add .
    ```
4.  **Retry the commit**: Run `git commit` again. The hooks will run again on the modified files.

### Running Hooks Manually

You can run hooks manually at any time without committing:

```bash
# Run all hooks on all files
pre-commit run --all-files

# Run a specific hook
pre-commit run black --all-files

# Run hooks only on staged files
pre-commit run
```

### Skipping Hooks (Not Recommended)

If you absolutely need to skip hooks for a commit, you can use the `--no-verify` flag:

```bash
git commit --no-verify -m "Your commit message"
```

**Warning**: Use this sparingly. Skipping hooks defeats their purpose and can allow issues to enter your repository.

## Common Issues and Solutions

### Issue: `pre-commit: command not found`

**Solution**: Pre-commit is not installed. Run:
```bash
pip install pre-commit
```

### Issue: Hooks are not running on commit

**Solution**: The hooks may not be installed. Run:
```bash
pre-commit install
```

### Issue: `black` keeps reformatting my code differently than I expect

**Solution**: Check the Black configuration in `pyproject.toml`. The project uses a line length of 100 characters. Ensure your editor is configured to match this.

### Issue: MyPy is failing with type errors

**Solution**: Add type annotations to your code or use `# type: ignore` comments for specific lines. See the MyPy documentation for more information.

### Issue: A hook is too strict for my use case

**Solution**: You can modify `.pre-commit-config.yaml` to adjust hook settings. For example, to skip a specific file from type checking:
```yaml
- id: mypy
  exclude: "^(tests/|docs/)"
```

## Advanced: Customizing Hooks

You can customize hook behavior by editing `.pre-commit-config.yaml`. Here are some common customizations:

### Disable a Hook Temporarily

Comment out the hook in `.pre-commit-config.yaml`:

```yaml
# - id: mypy
#   name: MyPy type checker
```

Then run:
```bash
pre-commit install
```

### Change Hook Arguments

Modify the `args` field in `.pre-commit-config.yaml`:

```yaml
- id: black
  args: ["--line-length=120"]  # Change line length to 120
```

### Run Hooks Only on Specific Stages

Hooks can run at different stages (commit, push, manual). To run a hook only on push:

```yaml
- id: mypy
  stages: [push]
```

## Uninstalling Pre-Commit Hooks

If you want to remove pre-commit hooks from your repository:

```bash
pre-commit uninstall
```

This removes the hook files from `.git/hooks/` but leaves the `.pre-commit-config.yaml` file intact.

## Resources

- **Pre-Commit Documentation**: https://pre-commit.com/
- **Pre-Commit Hooks Registry**: https://pre-commit.com/hooks.html
- **Black Documentation**: https://black.readthedocs.io/
- **Ruff Documentation**: https://docs.astral.sh/ruff/
- **MyPy Documentation**: https://mypy.readthedocs.io/

## Quick Reference

| Command | Purpose |
|---------|---------|
| `pre-commit install` | Install hooks into `.git/hooks/` |
| `pre-commit uninstall` | Remove hooks from `.git/hooks/` |
| `pre-commit run --all-files` | Run all hooks on all files |
| `pre-commit run <hook-id> --all-files` | Run a specific hook on all files |
| `git commit --no-verify` | Skip hooks for a commit (not recommended) |
| `pre-commit autoupdate` | Update hook versions to latest |

## Next Steps

1. Install pre-commit hooks using the steps above
2. Make a test commit to verify everything works
3. Start developing with confidence that code quality checks will run automatically
4. If you encounter issues, refer to the "Common Issues and Solutions" section above
