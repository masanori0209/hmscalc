"""Tests for the hmscalc CLI."""

from __future__ import annotations

import subprocess
import sys


def _run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "hmscalc", *args],
        capture_output=True,
        text=True,
        check=False,
    )


def test_cli_add() -> None:
    """Test CLI add command sums durations."""
    result = _run_cli("add", "1:30", "2:15", "0:45")
    assert result.returncode == 0
    assert result.stdout.strip() == "4:30:00"


def test_cli_sub() -> None:
    """Test CLI sub command subtracts durations."""
    result = _run_cli("sub", "2:00", "0:45")
    assert result.returncode == 0
    assert result.stdout.strip() == "1:15:00"


def test_cli_sum() -> None:
    """Test CLI sum command matches add behavior."""
    result = _run_cli("sum", "1:00", "2:00", "3:00")
    assert result.returncode == 0
    assert result.stdout.strip() == "6:00:00"


def test_cli_invalid_format() -> None:
    """Test CLI returns error on invalid time format."""
    result = _run_cli("add", "bad")
    assert result.returncode == 1
    assert "error:" in result.stderr


def test_cli_sub_requires_two_values() -> None:
    """Test CLI sub requires at least two time values."""
    result = _run_cli("sub", "1:00")
    assert result.returncode == 1
    assert "at least two" in result.stderr
