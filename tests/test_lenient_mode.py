"""Tests for lenient HMSTime parsing (strict=False)."""

from __future__ import annotations

import pytest

from hmscalc import HMSTime, InvalidTimeFormatError


def test_lenient_normalizes_overflow_minutes() -> None:
    """Test 1:90:00 normalizes to 2:30:00."""
    assert HMSTime("1:90:00", strict=False) == HMSTime("2:30:00")


def test_lenient_normalizes_overflow_seconds() -> None:
    """Test 0:01:90 normalizes to 0:02:30."""
    assert HMSTime("0:01:90", strict=False) == HMSTime("0:02:30")


def test_strict_still_rejects_overflow() -> None:
    """Test default strict mode rejects overflow."""
    with pytest.raises(InvalidTimeFormatError):
        HMSTime("1:90:00")


def test_parse_classmethod_lenient() -> None:
    """Test HMSTime.parse with strict=False."""
    assert HMSTime.parse("1:90:00", strict=False) == HMSTime("2:30:00")


def test_parse_many_lenient() -> None:
    """Test parse_many passes strict flag."""
    values = HMSTime.parse_many(["1:00", "0:90"], strict=False)
    assert values[1] == HMSTime("1:30:00")


def test_sum_strings_lenient() -> None:
    """Test sum_strings with lenient parsing."""
    assert HMSTime.sum_strings(["1:00", "0:90"], strict=False) == HMSTime("2:30:00")


def test_lenient_negative_overflow() -> None:
    """Test negative lenient values normalize."""
    assert HMSTime("-0:90", strict=False) == HMSTime("-1:30:00")


def test_lenient_invalid_format_still_raises() -> None:
    """Test malformed strings fail even in lenient mode."""
    with pytest.raises(InvalidTimeFormatError):
        HMSTime("not-a-time", strict=False)
