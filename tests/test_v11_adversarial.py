"""Adversarial edge-case tests for v1.1 features (dates, HMSTime extensions)."""

from __future__ import annotations

import datetime

import pytest

from hmscalc import HMSTime, InvalidTimeFormatError, NotTimeStringError, dates


def test_sum_strings_empty_list() -> None:
    """sum_strings on empty input should match sum([])."""
    assert str(HMSTime.sum_strings([])) == "0:00:00"


def test_parse_many_rejects_non_iterable() -> None:
    """parse_many must reject non-iterables."""
    with pytest.raises(TypeError):
        HMSTime.parse_many(HMSTime("1:00:00"))  # type: ignore[arg-type]


def test_sum_strings_invalid_entry_raises() -> None:
    """One bad string in the list must fail the whole sum."""
    with pytest.raises(InvalidTimeFormatError):
        HMSTime.sum_strings(["1:00", "not-a-time"])


def test_timedelta_add_commutative_with_seconds() -> None:
    """Radd and add must agree for timedelta operands."""
    t = HMSTime("1:00:00")
    delta = datetime.timedelta(minutes=30)
    assert t + delta == delta + t


def test_timedelta_sub_does_not_support_rsub_from_timedelta() -> None:
    """Timedelta - HMSTime remains unsupported (NotImplemented)."""
    t = HMSTime("1:00:00")
    delta = datetime.timedelta(minutes=30)
    assert delta.__sub__(t) == NotImplemented


def test_abs_of_zero_unchanged() -> None:
    """abs(0) stays zero."""
    assert str(abs(HMSTime("0:00:00"))) == "0:00:00"
    assert str(abs(HMSTime("-0:00:00"))) == "0:00:00"


def test_padded_format_large_hours() -> None:
    """PADDED format must not truncate hours >= 100."""
    assert HMSTime("100:00:00").format("HH:MM:SS:PADDED") == "100:00:00"


def test_hh_mm_ss_consistent_with_to_tuple() -> None:
    """Properties must mirror to_tuple for positive and negative values."""
    for value in ("1:02:03", "-1:02:03", "0:00:01"):
        t = HMSTime(value)
        hh, mm, ss = t.to_tuple()
        assert (t.hh, t.mm, t.ss) == (hh, mm, ss)


def test_missing_dates_empty_present() -> None:
    """All dates in range are missing when present is empty."""
    start = dates.parse_date("2026-06-01")
    end = dates.parse_date("2026-06-03")
    assert dates.missing_dates([], start, end) == dates.date_range(start, end)


def test_gap_ranges_empty_present_full_range_is_gap() -> None:
    """With no present dates the entire range is one gap."""
    start = dates.parse_date("2026-06-01")
    end = dates.parse_date("2026-06-03")
    assert dates.gap_ranges([], start=start, end=end) == [(start, end)]


def test_has_date_gaps_duplicate_dates() -> None:
    """Duplicate dates must not create false gaps."""
    day = dates.parse_date("2026-06-01")
    assert dates.has_date_gaps([day, day, day]) is False


def test_monthrange_invalid_month() -> None:
    """Month must be 1..12."""
    with pytest.raises(ValueError, match="month must be"):
        dates.monthrange(2026, 0)
    with pytest.raises(ValueError, match="month must be"):
        dates.monthrange(2026, 13)


def test_last_day_matches_calendar_for_all_months_2024() -> None:
    """last_day_of_month must match calendar.monthrange for every month."""
    import calendar

    for month in range(1, 13):
        expected_day = calendar.monthrange(2024, month)[1]
        assert dates.last_day_of_month(2024, month).day == expected_day


def test_combine_negative_time_subtracts_from_midnight() -> None:
    """Negative HMSTime moves datetime backward from midnight."""
    result = dates.combine(dates.parse_date("2026-06-28"), "-1:00:00")
    assert result == datetime.datetime(2026, 6, 27, 23, 0, 0)


def test_missing_datetimes_invalid_range() -> None:
    """Start after end is rejected."""
    start = datetime.datetime(2026, 6, 2, 9, 0)
    end = datetime.datetime(2026, 6, 1, 9, 0)
    with pytest.raises(ValueError, match="start must be on or before end"):
        dates.missing_datetimes([], start, end)


def test_not_time_string_bool_not_int_hint() -> None:
    """Bool must not use the int-specific hint message."""
    with pytest.raises(NotTimeStringError, match="bool"):
        HMSTime(True)  # type: ignore[arg-type]
    with pytest.raises(NotTimeStringError, match="from_seconds"):
        HMSTime(3600)  # type: ignore[arg-type]
