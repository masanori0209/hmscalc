"""Tests for hmscalc.dates calendar utilities."""

from __future__ import annotations

from datetime import date, datetime, timedelta

import pytest

from hmscalc import InvalidDateFormatError
from hmscalc.dates import (
    combine,
    date_range,
    days_in_month,
    gap_ranges,
    has_date_gaps,
    iter_dates,
    last_day_of_month,
    missing_dates,
    missing_datetimes,
    monthrange,
    parse_date,
    parse_datetime,
)


def test_parse_date() -> None:
    """Test parsing common date string formats."""
    assert parse_date("2026-06-28") == date(2026, 6, 28)
    assert parse_date("2026/06/28") == date(2026, 6, 28)


def test_parse_date_invalid() -> None:
    """Test invalid date strings raise errors."""
    with pytest.raises(InvalidDateFormatError):
        parse_date("2026-13-01")
    with pytest.raises(InvalidDateFormatError):
        parse_date("bad")
    with pytest.raises(InvalidDateFormatError):
        parse_date(123)  # type: ignore[arg-type]


def test_parse_datetime() -> None:
    """Test parsing datetime strings."""
    assert parse_datetime("2026-06-28 14:30") == datetime(2026, 6, 28, 14, 30, 0)
    assert parse_datetime("2026/06/28 14:30:15") == datetime(2026, 6, 28, 14, 30, 15)


def test_monthrange_and_last_day() -> None:
    """Test month length helpers including February leap year."""
    assert monthrange(2024, 2) == (3, 29)
    assert days_in_month(2024, 2) == 29
    assert last_day_of_month(2024, 2) == date(2024, 2, 29)
    assert last_day_of_month(2025, 2) == date(2025, 2, 28)
    assert last_day_of_month(2026, 6) == date(2026, 6, 30)


def test_date_range() -> None:
    """Test inclusive date range generation."""
    assert date_range(date(2026, 6, 1), date(2026, 6, 3)) == [
        date(2026, 6, 1),
        date(2026, 6, 2),
        date(2026, 6, 3),
    ]
    assert list(iter_dates(date(2026, 6, 5), date(2026, 6, 3))) == []


def test_missing_dates() -> None:
    """Test finding missing dates in a range."""
    present = [date(2026, 6, 1), date(2026, 6, 3), date(2026, 6, 5)]
    missing = missing_dates(present, date(2026, 6, 1), date(2026, 6, 5))
    assert missing == [date(2026, 6, 2), date(2026, 6, 4)]


def test_has_date_gaps() -> None:
    """Test gap detection for sorted date sequences."""
    assert has_date_gaps([date(2026, 6, 1), date(2026, 6, 2), date(2026, 6, 3)]) is False
    assert has_date_gaps([date(2026, 6, 1), date(2026, 6, 3)]) is True
    assert has_date_gaps([date(2026, 6, 1)]) is False


def test_gap_ranges() -> None:
    """Test gap ranges return contiguous missing intervals."""
    present = [date(2026, 6, 1), date(2026, 6, 5), date(2026, 6, 6)]
    assert gap_ranges(present, start=date(2026, 6, 1), end=date(2026, 6, 7)) == [
        (date(2026, 6, 2), date(2026, 6, 4)),
        (date(2026, 6, 7), date(2026, 6, 7)),
    ]


def test_combine() -> None:
    """Test combining date with HMSTime string."""
    assert combine(date(2026, 6, 28), "2:30:15") == datetime(2026, 6, 28, 2, 30, 15)


def test_missing_datetimes() -> None:
    """Test missing datetime slots at a fixed step."""
    start = datetime(2026, 6, 1, 9, 0)
    present = [start, start + timedelta(hours=2)]
    end = start + timedelta(hours=4)
    missing = missing_datetimes(present, start, end, step=timedelta(hours=2))
    assert missing == [start + timedelta(hours=4)]
