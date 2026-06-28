"""Tests for hmscalc.scheduling availability search."""

from __future__ import annotations

from datetime import date, datetime, timedelta

import pytest

from hmscalc.scheduling import (
    AvailabilitySlot,
    DateTimeRange,
    find_availability_across_days,
    find_availability_slots,
    find_availability_windows,
    free_time_gaps,
    merge_busy_intervals,
)


def _dt(text: str) -> datetime:
    return datetime.fromisoformat(text)


def test_merge_busy_intervals() -> None:
    """Test overlapping busy intervals are merged."""
    busy = [
        (_dt("2026-06-28 09:00"), _dt("2026-06-28 10:30")),
        (_dt("2026-06-28 10:00"), _dt("2026-06-28 11:00")),
    ]
    merged = merge_busy_intervals(busy)
    assert len(merged) == 1
    assert merged[0].start == _dt("2026-06-28 09:00")
    assert merged[0].end == _dt("2026-06-28 11:00")


def test_free_time_gaps() -> None:
    """Test free gaps between busy blocks."""
    busy = [
        (_dt("2026-06-28 09:00"), _dt("2026-06-28 10:00")),
        (_dt("2026-06-28 12:00"), _dt("2026-06-28 13:00")),
    ]
    gaps = free_time_gaps(busy, _dt("2026-06-28 09:00"), _dt("2026-06-28 18:00"))
    assert len(gaps) == 2
    assert gaps[0] == DateTimeRange(_dt("2026-06-28 10:00"), _dt("2026-06-28 12:00"))
    assert gaps[1] == DateTimeRange(_dt("2026-06-28 13:00"), _dt("2026-06-28 18:00"))


def test_find_availability_windows_with_buffers() -> None:
    """Test 1-hour meeting with 15-minute buffers in a 2-hour gap."""
    busy = [
        (_dt("2026-06-28 09:00"), _dt("2026-06-28 10:00")),
        (_dt("2026-06-28 12:00"), _dt("2026-06-28 13:00")),
    ]
    windows = find_availability_windows(
        busy,
        _dt("2026-06-28 09:00"),
        _dt("2026-06-28 18:00"),
        duration="1:00:00",
        buffer_before="0:15",
        buffer_after="0:15",
    )
    assert len(windows) == 2
    assert windows[0].earliest_start == _dt("2026-06-28 10:15")
    assert windows[0].latest_start == _dt("2026-06-28 10:45")
    assert windows[1].earliest_start == _dt("2026-06-28 13:15")
    assert windows[1].latest_start == _dt("2026-06-28 16:45")


def test_find_availability_slots_step() -> None:
    """Test discrete slots at 15-minute steps."""
    busy = [(_dt("2026-06-28 09:00"), _dt("2026-06-28 10:00"))]
    slots = find_availability_slots(
        busy,
        _dt("2026-06-28 09:00"),
        _dt("2026-06-28 12:00"),
        duration="1:00:00",
        buffer_before="0:15",
        buffer_after="0:15",
        step="0:15",
    )
    assert [slot.start for slot in slots] == [
        _dt("2026-06-28 10:15"),
        _dt("2026-06-28 10:30"),
        _dt("2026-06-28 10:45"),
    ]
    first = slots[0]
    assert isinstance(first, AvailabilitySlot)
    assert first.reserved_start == _dt("2026-06-28 10:00")
    assert first.reserved_end == _dt("2026-06-28 11:30")


def test_gap_too_short_for_duration_and_buffers() -> None:
    """Test gaps shorter than duration plus buffers are excluded."""
    busy = [
        (_dt("2026-06-28 09:00"), _dt("2026-06-28 10:00")),
        (_dt("2026-06-28 10:30"), _dt("2026-06-28 12:00")),
    ]
    windows = find_availability_windows(
        busy,
        _dt("2026-06-28 09:00"),
        _dt("2026-06-28 18:00"),
        duration="1:00:00",
        buffer_before="0:15",
        buffer_after="0:15",
    )
    assert len(windows) == 1
    assert windows[0].free_gap.start == _dt("2026-06-28 12:00")


def test_find_availability_across_days() -> None:
    """Test multi-day search within daily working hours."""
    busy = [
        (_dt("2026-06-28 09:00"), _dt("2026-06-28 10:00")),
        (_dt("2026-06-29 14:00"), _dt("2026-06-29 15:00")),
    ]
    slots = find_availability_across_days(
        busy,
        date(2026, 6, 28),
        date(2026, 6, 29),
        daily_start="9:00",
        daily_end="18:00",
        duration="1:00",
        buffer_before="0:15",
        buffer_after="0:15",
        step="1:00",
    )
    assert slots[0].start == _dt("2026-06-28 10:15")
    assert any(slot.start.date() == date(2026, 6, 29) for slot in slots)


def test_string_datetime_inputs() -> None:
    """Test scheduling accepts datetime strings for busy and window bounds."""
    busy = [("2026-06-28 09:00", "2026-06-28 10:00")]
    slots = find_availability_slots(
        busy,
        "2026-06-28 09:00",
        "2026-06-28 12:00",
        duration="1:00",
        buffer_before="0:15",
        buffer_after="0:15",
        step="0:15",
    )
    assert slots[0].start == _dt("2026-06-28 10:15")


def test_invalid_duration() -> None:
    """Test invalid duration raises ValueError."""
    with pytest.raises(ValueError, match="duration must be positive"):
        find_availability_windows(
            [],
            _dt("2026-06-28 09:00"),
            _dt("2026-06-28 18:00"),
            duration=timedelta(0),
        )
