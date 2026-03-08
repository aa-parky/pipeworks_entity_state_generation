"""Version parity tests.

These tests ensure package version is sourced from project metadata and does
not drift between runtime exports and build configuration.
"""

from __future__ import annotations

import tomllib
from pathlib import Path

import condition_axis


def _read_pyproject_version() -> str:
    """Read authoritative project version from pyproject.toml."""

    pyproject_path = Path(__file__).resolve().parent.parent / "pyproject.toml"
    with pyproject_path.open("rb") as pyproject_file:
        pyproject_data = tomllib.load(pyproject_file)
    return str(pyproject_data["project"]["version"])


def test_exported_version_matches_pyproject() -> None:
    """`condition_axis.__version__` should always match pyproject metadata."""

    assert condition_axis.__version__ == _read_pyproject_version()
