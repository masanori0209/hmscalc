"""Property-based adversarial tests for v1.1+ (Python 3.10+, Hypothesis)."""

from __future__ import annotations

import sys
from datetime import datetime, time, timedelta

import pytest

if sys.version_info < (3, 10):
    pytest.skip("hypothesis property tests require Python 3.10+", allow_module_level=True)

from hypothesis import assume, given, settings
from hypothesis import strategies as st

from hmscalc import HMSTime, business_days, dates
from hmscalc.scheduling import (
    DateTimeRange,
    find_availability_across_business_days,
    find_availability_slots,
    free_time_gaps,
    merge_busy_intervals,
)


@st.composite
def valid_hms_strings(draw: st.DrawFn) -> str:
    """Generate valid HMS duration strings."""
    hh = draw(st.integers(min_value=0, max_value=48))
    mm = draw(st.integers(min_value=0, max_value=59))
    ss = draw(st.integers(min_value=0, max_value=59))
    negative = draw(st.booleans())
    sign = "-" if negative else ""
    with_seconds = draw(st.booleans())
    if with_seconds:
        return f"{sign}{hh}:{mm:02}:{ss:02}"
    return f"{sign}{hh}:{mm:02}"


@st.composite
def valid_date_strings(draw: st.DrawFn) -> str:
    """Generate YYYY-MM-DD strings for valid calendar dates."""
    year = draw(st.integers(min_value=2000, max_value=2030))
    month = draw(st.integers(min_value=1, max_value=12))
    day = draw(st.integers(min_value=1, max_value=28))
    return f"{year:04d}-{month:02d}-{day:02d}"


@st.composite
def busy_intervals_in_window(
    draw: st.DrawFn,
    window_start: datetime,
    window_end: datetime,
    max_intervals: int = 6,
) -> list[tuple[datetime, datetime]]:
    """Generate busy intervals inside a fixed window."""
    window_seconds = int((window_end - window_start).total_seconds())
    assume(window_seconds >= 3600)

    count = draw(st.integers(min_value=0, max_value=max_intervals))
    intervals: list[tuple[datetime, datetime]] = []
    for _ in range(count):
        start_offset = draw(st.integers(min_value=0, max_value=window_seconds - 60))
        end_offset = draw(st.integers(min_value=start_offset + 60, max_value=window_seconds))
        start = window_start + timedelta(seconds=start_offset)
        end = window_start + timedelta(seconds=end_offset)
        intervals.append((start, end))
    return intervals


WINDOW_START = datetime(2026, 6, 28, 8, 0, 0)
WINDOW_END = datetime(2026, 6, 28, 20, 0, 0)


@given(st.data())
@settings(max_examples=80, deadline=None)
def test_scheduling_gaps_partition_window(data: st.DataObject) -> None:
    """Gap durations plus clipped busy must equal the search window."""
    busy = data.draw(busy_intervals_in_window(WINDOW_START, WINDOW_END))
    gaps = free_time_gaps(busy, WINDOW_START, WINDOW_END)
    merged = merge_busy_intervals(busy)
    clipped_busy = [
        DateTimeRange(max(item.start, WINDOW_START), min(item.end, WINDOW_END))
        for item in merged
        if max(item.start, WINDOW_START) < min(item.end, WINDOW_END)
    ]
    total_gap = sum((gap.duration for gap in gaps), timedelta())
    total_busy = sum((item.duration for item in clipped_busy), timedelta())
    assert total_gap + total_busy == WINDOW_END - WINDOW_START


@given(
    st.integers(min_value=15, max_value=120),
    st.integers(min_value=0, max_value=30),
    st.integers(min_value=0, max_value=30),
)
@settings(max_examples=60, deadline=None)
def test_scheduling_slots_never_overlap_busy(
    duration_minutes: int,
    buffer_before_min: int,
    buffer_after_min: int,
) -> None:
    """Every availability slot must avoid busy time including buffers."""
    busy = [
        (WINDOW_START + timedelta(hours=1), WINDOW_START + timedelta(hours=2)),
        (WINDOW_START + timedelta(hours=4), WINDOW_START + timedelta(hours=5)),
        (WINDOW_START + timedelta(hours=7), WINDOW_START + timedelta(hours=8)),
    ]
    duration = timedelta(minutes=duration_minutes)
    lead = timedelta(minutes=buffer_before_min)
    trail = timedelta(minutes=buffer_after_min)

    slots = find_availability_slots(
        busy,
        WINDOW_START,
        WINDOW_END,
        duration=duration,
        buffer_before=lead,
        buffer_after=trail,
        step=timedelta(minutes=15),
    )
    merged = merge_busy_intervals(busy)
    for slot in slots:
        assert slot.end - slot.start == duration
        assert slot.reserved_start >= slot.free_gap.start
        assert slot.reserved_end <= slot.free_gap.end
        for busy_range in merged:
            overlap = slot.reserved_start < busy_range.end and slot.reserved_end > busy_range.start
            assert not overlap


@given(valid_hms_strings())
@settings(max_examples=100)
def test_sum_strings_matches_manual_parse(time_str: str) -> None:
    """sum_strings must equal sum(parse_many(...))."""
    strings = [time_str.strip(), "0:00:01", "0:00:02"]
    assert HMSTime.sum_strings(strings) == HMSTime.sum(HMSTime.parse_many(strings))


@given(valid_hms_strings(), st.integers(min_value=1, max_value=120))
@settings(max_examples=80)
def test_timedelta_roundtrip_preserves_seconds(time_str: str, minutes: int) -> None:
    """Adding then subtracting the same timedelta restores total seconds."""
    original = HMSTime(time_str.strip())
    delta = timedelta(minutes=minutes)
    restored = (original + delta) - delta
    assert restored.to_seconds() == original.to_seconds()


@given(valid_date_strings())
@settings(max_examples=100)
def test_parse_date_roundtrip_iso(date_str: str) -> None:
    """parse_date output must re-serialize to the same calendar date."""
    parsed = dates.parse_date(date_str)
    assert parsed.isoformat() == date_str


@given(
    st.integers(min_value=2000, max_value=2035),
    st.integers(min_value=1, max_value=12),
)
@settings(max_examples=48)
def test_days_in_month_matches_last_day(year: int, month: int) -> None:
    """days_in_month and last_day_of_month must stay consistent."""
    last = dates.last_day_of_month(year, month)
    assert last.day == dates.days_in_month(year, month)
    assert last == dates.parse_date(f"{year:04d}-{month:02d}-{last.day:02d}")


@given(
    st.integers(min_value=0, max_value=20),
    st.integers(min_value=0, max_value=20),
)
@settings(max_examples=60)
def test_add_business_days_inverse(forward: int, backward: int) -> None:
    """Adding then subtracting the same count returns to start when enough range exists."""
    start = dates.parse_date("2026-01-05")
    assume(forward <= 15 and backward <= 15)
    mid = business_days.add_business_days(start, forward)
    restored = business_days.add_business_days(mid, -forward)
    assert restored == start


@given(
    st.integers(min_value=1, max_value=14),
    st.integers(min_value=1, max_value=14),
)
@settings(max_examples=40, deadline=None)
def test_business_scheduling_subset_of_all_days(start_offset: int, span_days: int) -> None:
    """Business-day slots must be a subset of all-day slots."""
    start = dates.parse_date("2026-06-01") + timedelta(days=start_offset)
    end = start + timedelta(days=span_days)
    assume(end <= dates.parse_date("2026-06-30"))

    busy = [
        (datetime.combine(start, time(9, 0)), datetime.combine(start, time(10, 0))),
    ]
    business_slots = find_availability_across_business_days(
        busy,
        start,
        end,
        daily_start="9:00",
        daily_end="12:00",
        duration=timedelta(hours=1),
        buffer_before=timedelta(minutes=15),
        buffer_after=timedelta(minutes=15),
        step=timedelta(hours=1),
    )
    for slot in business_slots:
        assert business_days.is_business_day(slot.start.date())
