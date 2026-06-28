"""Tests for the hmscalc CLI."""

from __future__ import annotations

import io
import subprocess
import sys

import pytest

from hmscalc.cli import main


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


def test_cli_main_direct_add(capsys: pytest.CaptureFixture[str]) -> None:
    """Test in-process CLI add for coverage under pytest-cov 7."""
    assert main(["add", "1:00", "2:00"]) == 0
    assert capsys.readouterr().out.strip() == "3:00:00"


def test_cli_main_direct_sub(capsys: pytest.CaptureFixture[str]) -> None:
    """Test in-process CLI sub for coverage under pytest-cov 7."""
    assert main(["sub", "2:00", "0:30"]) == 0
    assert capsys.readouterr().out.strip() == "1:30:00"


def test_cli_main_direct_invalid(capsys: pytest.CaptureFixture[str]) -> None:
    """Test in-process CLI error handling."""
    assert main(["add", "invalid"]) == 1
    assert "error:" in capsys.readouterr().err


def test_cli_avg() -> None:
    """Test CLI avg command."""
    result = _run_cli("avg", "1:00:00", "3:00:00")
    assert result.returncode == 0
    assert result.stdout.strip() == "2:00:00"


def test_cli_min_max() -> None:
    """Test CLI min and max commands."""
    min_result = _run_cli("min", "1:00:00", "3:00:00", "0:30:00")
    max_result = _run_cli("max", "1:00:00", "3:00:00", "0:30:00")
    assert min_result.stdout.strip() == "0:30:00"
    assert max_result.stdout.strip() == "3:00:00"


def test_cli_format_flag() -> None:
    """Test CLI --format output option."""
    result = _run_cli("--format", "HH:MM", "add", "1:30:00", "2:00:00")
    assert result.returncode == 0
    assert result.stdout.strip() == "3:30"


def test_cli_stdin_sum() -> None:
    """Test CLI reads durations from stdin."""
    result = subprocess.run(
        [sys.executable, "-m", "hmscalc", "sum"],
        input="1:00\n2:00\n3:00\n",
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "6:00:00"


def test_cli_main_stdin_dash(capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch) -> None:
    """Test CLI reads stdin when times argument is '-'."""
    stdin = io.StringIO("1:00\n2:00\n")
    stdin.isatty = lambda: False  # type: ignore[method-assign]
    monkeypatch.setattr("sys.stdin", stdin)
    assert main(["add", "-"]) == 0
    assert capsys.readouterr().out.strip() == "3:00:00"


def test_cli_main_stdin_skips_comments(capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch) -> None:
    """Test CLI stdin ignores blank lines and comments."""
    stdin = io.StringIO("# header\n\n1:00\n")
    stdin.isatty = lambda: False  # type: ignore[method-assign]
    monkeypatch.setattr("sys.stdin", stdin)
    assert main(["sum"]) == 0
    assert capsys.readouterr().out.strip() == "1:00:00"


def test_cli_main_no_times(capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch) -> None:
    """Test CLI errors when no times are provided."""
    stdin = io.StringIO("")
    stdin.isatty = lambda: True  # type: ignore[method-assign]
    monkeypatch.setattr("sys.stdin", stdin)
    assert main(["add"]) == 1
    assert "no time values" in capsys.readouterr().err


def test_cli_main_sub_one_value(capsys: pytest.CaptureFixture[str]) -> None:
    """Test in-process CLI sub with one value hits validation."""
    assert main(["sub", "1:00"]) == 1
    assert "at least two" in capsys.readouterr().err


def test_cli_main_format_padded(capsys: pytest.CaptureFixture[str]) -> None:
    """Test in-process CLI padded format output."""
    assert main(["--format", "HH:MM:SS:PADDED", "add", "1:00:00"]) == 0
    assert capsys.readouterr().out.strip() == "01:00:00"
