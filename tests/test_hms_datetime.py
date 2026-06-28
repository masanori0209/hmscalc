"""Tests for hmscalc.hms_datetime.HMSDateTime."""

from __future__ import annotations

from datetime import date, datetime, timedelta

from hmscalc import HMSDateTime, HMSTime


def test_from_strings() -> None:
    """Test construction from date and time strings."""
    value = HMSDateTime.from_strings("2026-06-28", "2:30:15")
    assert value.day == date(2026, 6, 28)
    assert value.time == HMSTime("2:30:15")


def test_to_datetime() -> None:
    """Test conversion to datetime."""
    value = HMSDateTime.from_strings("2026-06-28", "2:30:15")
    assert value.to_datetime() == datetime(2026, 6, 28, 2, 30, 15)


def test_from_datetime_roundtrip() -> None:
    """Test datetime roundtrip."""
    original = datetime(2026, 6, 28, 9, 15, 0)
    assert HMSDateTime.from_datetime(original).to_datetime() == original


def test_add_timedelta() -> None:
    """Test adding timedelta shifts datetime."""
    value = HMSDateTime.from_strings("2026-06-28", "1:00:00")
    shifted = value + timedelta(hours=2)
    assert shifted.time == HMSTime("3:00:00")


def test_subtract_timedelta() -> None:
    """Test subtracting timedelta."""
    value = HMSDateTime.from_strings("2026-06-28", "3:00:00")
    shifted = value - timedelta(hours=1)
    assert shifted.time == HMSTime("2:00:00")


def test_subtract_hms_datetime() -> None:
    """Test difference between two HMSDateTime values."""
    left = HMSDateTime.from_strings("2026-06-28", "3:00:00")
    right = HMSDateTime.from_strings("2026-06-28", "1:00:00")
    assert left - right == timedelta(hours=2)


def test_ordering() -> None:
    """Test HMSDateTime supports ordering."""
    early = HMSDateTime.from_strings("2026-06-01", "1:00")
    late = HMSDateTime.from_strings("2026-06-02", "0:00")
    assert early < late


def test_to_iso() -> None:
    """Test ISO-like serialization."""
    value = HMSDateTime.from_strings("2026-06-28", "2:30:15")
    assert value.to_iso() == "2026-06-28T02:30:15"


def test_combine_with_hms_time() -> None:
    """Test combine accepts an HMSTime duration object."""
    value = HMSDateTime.combine(date(2026, 6, 28), HMSTime("1:00"))
    assert value.time == HMSTime("1:00")


def test_add_wrong_type_returns_not_implemented() -> None:
    """Test unsupported add operand returns NotImplemented."""
    value = HMSDateTime.from_strings("2026-06-28", "1:00")
    assert value.__add__(1) is NotImplemented  # type: ignore[arg-type]


def test_sub_wrong_type_returns_not_implemented() -> None:
    """Test unsupported sub operand returns NotImplemented."""
    value = HMSDateTime.from_strings("2026-06-28", "1:00")
    assert value.__sub__(1) is NotImplemented  # type: ignore[arg-type]


def test_combine_with_lenient() -> None:
    """Test combine respects strict flag."""
    value = HMSDateTime.combine(date(2026, 6, 28), "1:90", strict=False)
    assert value.time == HMSTime("2:30:00")
