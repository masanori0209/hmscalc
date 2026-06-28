"""Tests for ISO 8601 date components in duration parsing."""

from __future__ import annotations

import pytest

from hmscalc import HMSTime, InvalidTimeFormatError


def test_from_iso8601_one_day() -> None:
    """Test P1D equals 24 hours."""
    assert HMSTime.from_iso8601("P1D") == HMSTime("24:00:00")
    assert HMSTime.from_iso8601("P1D").to_seconds() == 86_400


def test_from_iso8601_one_week() -> None:
    """Test P1W equals seven days."""
    assert HMSTime.from_iso8601("P1W") == HMSTime("168:00:00")


def test_from_iso8601_combined_date_and_time() -> None:
    """Test P1DT2H combines date and time sections."""
    assert HMSTime.from_iso8601("P1DT2H") == HMSTime("26:00:00")


def test_from_iso8601_nominal_month() -> None:
    """Test P1M uses nominal 30-day month."""
    assert HMSTime.from_iso8601("P1M").to_seconds() == 30 * 86_400


def test_from_iso8601_nominal_year() -> None:
    """Test P1Y uses nominal 365-day year."""
    assert HMSTime.from_iso8601("P1Y").to_seconds() == 365 * 86_400


def test_to_iso8601_emits_days() -> None:
    """Test whole-day durations serialize as PnD."""
    assert HMSTime("24:00:00").to_iso8601() == "P1D"


def test_to_iso8601_emits_weeks() -> None:
    """Test whole-week durations serialize as PnW."""
    assert HMSTime("168:00:00").to_iso8601() == "P1W"


def test_to_iso8601_combined_output() -> None:
    """Test mixed day and time output uses PnDT form."""
    assert HMSTime("26:00:00").to_iso8601() == "P1DT2H"


def test_iso8601_week_cannot_mix_with_other_parts() -> None:
    """Test P1W1D is rejected."""
    with pytest.raises(InvalidTimeFormatError):
        HMSTime.from_iso8601("P1W1D")


def test_iso8601_date_roundtrip() -> None:
    """Test P1DT1H30M15S round-trips."""
    original = HMSTime.from_iso8601("P1DT1H30M15S")
    assert HMSTime.from_iso8601(original.to_iso8601()) == original
