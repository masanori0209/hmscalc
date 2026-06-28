"""Tests for hmscalc.business_days."""

from __future__ import annotations

from datetime import date

import pytest

from hmscalc.business_days import (
    BusinessCalendar,
    add_business_days,
    business_day_range,
    count_business_days,
    is_business_day,
    next_business_day,
    previous_business_day,
)


def test_weekday_is_business_day() -> None:
    """Test Monday is a business day by default."""
    assert is_business_day(date(2026, 6, 29))  # Monday


def test_weekend_not_business_day() -> None:
    """Test Saturday and Sunday are excluded by default."""
    assert not is_business_day(date(2026, 6, 27))  # Saturday
    assert not is_business_day(date(2026, 6, 28))  # Sunday


def test_holiday_exclusion() -> None:
    """Test explicit holidays are excluded."""
    holiday = date(2026, 6, 29)
    cal = BusinessCalendar.weekdays_only(holidays=[holiday])
    assert not cal.is_business_day(holiday)
    assert cal.is_business_day(date(2026, 6, 30))


def test_business_day_range_skips_weekend() -> None:
    """Test range Fri–Mon yields Fri and Mon only."""
    days = business_day_range(date(2026, 6, 26), date(2026, 6, 29))
    assert days == [date(2026, 6, 26), date(2026, 6, 29)]


def test_count_business_days() -> None:
    """Test inclusive count across a week."""
    assert count_business_days(date(2026, 6, 22), date(2026, 6, 28)) == 5


def test_add_business_days_forward() -> None:
    """Test adding one business day from Friday lands on Monday."""
    assert add_business_days(date(2026, 6, 26), 1) == date(2026, 6, 29)


def test_add_business_days_backward() -> None:
    """Test subtracting one business day from Monday lands on Friday."""
    assert add_business_days(date(2026, 6, 29), -1) == date(2026, 6, 26)


def test_next_and_previous_business_day() -> None:
    """Test navigation helpers around a weekend."""
    assert next_business_day(date(2026, 6, 26)) == date(2026, 6, 29)
    assert previous_business_day(date(2026, 6, 29)) == date(2026, 6, 26)
    assert next_business_day(date(2026, 6, 29), inclusive=True) == date(2026, 6, 29)


def test_add_zero_returns_same_day() -> None:
    """Test adding zero business days is a no-op."""
    day = date(2026, 6, 27)
    assert add_business_days(day, 0) == day


def test_invalid_weekday_raises() -> None:
    """Test invalid weekday values are rejected."""
    with pytest.raises(ValueError, match="weekdays must be integers"):
        BusinessCalendar(weekdays=frozenset({7}))
