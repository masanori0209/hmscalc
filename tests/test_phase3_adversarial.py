"""Adversarial tests for business days, timezones, and Phase 3 scheduling."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

import pytest

from hmscalc import business_days, scheduling, tz
from hmscalc.business_days import BusinessCalendar, add_business_days, business_day_range
from hmscalc.scheduling import find_availability_across_business_days, find_availability_across_days


def test_holiday_bridge_skips_entire_week() -> None:
    """Test Mon holiday + default calendar skips Mon while Tue–Fri remain."""
    mon = date(2026, 6, 29)
    cal = BusinessCalendar.weekdays_only(holidays=[mon])
    days = business_day_range(date(2026, 6, 29), date(2026, 7, 3), calendar=cal)
    assert mon not in days
    assert days == [date(2026, 6, 30), date(2026, 7, 1), date(2026, 7, 2), date(2026, 7, 3)]


def test_add_business_days_over_long_holiday_run() -> None:
    """Test forward add skips consecutive holidays."""
    holidays = [date(2026, 6, 29), date(2026, 6, 30)]
    cal = BusinessCalendar.weekdays_only(holidays=holidays)
    assert add_business_days(date(2026, 6, 26), 1, calendar=cal) == date(2026, 7, 1)


def test_custom_weekdays_saturday_workday() -> None:
    """Test custom calendar can treat Saturday as a working day."""
    cal = BusinessCalendar(weekdays=frozenset({5}), holidays=frozenset())
    assert cal.is_business_day(date(2026, 6, 27))  # Saturday
    assert not cal.is_business_day(date(2026, 6, 28))  # Sunday


def test_iter_business_days_empty_range() -> None:
    """Test reversed range yields nothing."""
    assert business_day_range(date(2026, 7, 1), date(2026, 6, 1)) == []


def test_business_scheduling_skips_weekend_and_holiday() -> None:
    """Test availability search only on business days."""
    holiday = date(2026, 6, 29)  # Monday
    cal = BusinessCalendar.weekdays_only(holidays=[holiday])
    busy = [("2026-06-26 09:00", "2026-06-26 10:00")]  # Friday
    slots = find_availability_across_business_days(
        busy,
        date(2026, 6, 26),
        date(2026, 7, 1),
        calendar=cal,
        daily_start="9:00",
        daily_end="12:00",
        duration="1:00",
        buffer_before="0:15",
        buffer_after="0:15",
        step="1:00",
    )
    slot_dates = {slot.start.date() for slot in slots}
    assert date(2026, 6, 27) not in slot_dates  # Saturday
    assert date(2026, 6, 28) not in slot_dates  # Sunday
    assert holiday not in slot_dates
    assert date(2026, 6, 30) in slot_dates


def test_timezone_aware_scheduling_tokyo() -> None:
    """Test tz-aware daily windows produce aware slot timestamps."""
    busy = [("2026-06-28 09:00", "2026-06-28 10:00")]
    slots = find_availability_across_days(
        busy,
        date(2026, 6, 28),
        date(2026, 6, 28),
        daily_start="9:00",
        daily_end="18:00",
        duration="1:00",
        buffer_before="0:15",
        buffer_after="0:15",
        step="1:00",
        tz="Asia/Tokyo",
    )
    assert len(slots) >= 1
    assert slots[0].start.tzinfo == ZoneInfo("Asia/Tokyo")
    assert slots[0].start.hour == 10
    assert slots[0].start.minute == 15


def test_daily_window_invalid_bounds_raises() -> None:
    """Test daily_start after daily_end is rejected."""
    with pytest.raises(ValueError, match="daily_start must be before daily_end"):
        tz.daily_window(date(2026, 6, 28), "18:00", "9:00", "Asia/Tokyo")


def test_naive_to_utc_raises() -> None:
    """Test converting naive datetime to UTC is rejected."""
    with pytest.raises(ValueError, match="naive datetime"):
        tz.local_to_utc(datetime(2026, 6, 28, 9, 0))


def test_to_timezone_naive_raises() -> None:
    """Test converting naive datetime between zones is rejected."""
    with pytest.raises(ValueError, match="naive datetime"):
        tz.to_timezone(datetime(2026, 6, 28, 9, 0), "UTC")


def test_dst_spring_forward_daily_window() -> None:
    """Test US spring-forward day still yields ordered daily bounds."""
    # 2026-03-08 is US DST spring forward (2 AM -> 3 AM)
    start, end = tz.daily_window(date(2026, 3, 8), "9:00", "17:00", "America/New_York")
    assert start.tzinfo == ZoneInfo("America/New_York")
    assert end > start
    assert (end - start) == timedelta(hours=8)


def test_business_days_add_negative_large() -> None:
    """Test large backward add crosses multiple weekends."""
    result = add_business_days(date(2026, 7, 10), -10)
    assert business_days.is_business_day(result)
    assert result < date(2026, 7, 10)


def test_find_across_business_days_invalid_range() -> None:
    """Test reversed date range raises."""
    with pytest.raises(ValueError, match="start_date must be on or before end_date"):
        find_availability_across_business_days(
            [],
            date(2026, 7, 2),
            date(2026, 6, 1),
            daily_start="9:00",
            daily_end="18:00",
            duration="1:00",
        )
