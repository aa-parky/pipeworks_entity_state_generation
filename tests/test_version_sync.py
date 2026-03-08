"""Version parity tests.

These tests ensure package version is sourced from project metadata and does
not drift between runtime exports and build configuration.
"""

from __future__ import annotations

import tomllib
from pathlib import Path

import pytest

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


def test_resolve_package_version_prefers_distribution_metadata(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Resolver should return installed distribution metadata when available."""

    monkeypatch.setattr(condition_axis, "package_version", lambda _: "9.9.9")

    assert condition_axis._resolve_package_version() == "9.9.9"


def test_resolve_package_version_falls_back_to_pyproject(monkeypatch: pytest.MonkeyPatch) -> None:
    """Resolver should fall back to pyproject version when distribution is missing."""

    def _raise_not_found(_: str) -> str:
        raise condition_axis.PackageNotFoundError

    monkeypatch.setattr(condition_axis, "package_version", _raise_not_found)

    assert condition_axis._resolve_package_version() == _read_pyproject_version()


def test_resolve_package_version_returns_unknown_on_fallback_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Resolver should emit unknown sentinel when pyproject fallback cannot be parsed."""

    def _raise_not_found(_: str) -> str:
        raise condition_axis.PackageNotFoundError

    monkeypatch.setattr(condition_axis, "package_version", _raise_not_found)
    monkeypatch.setattr(condition_axis.tomllib, "load", lambda _: {})

    assert condition_axis._resolve_package_version() == "0.0.0+unknown"
