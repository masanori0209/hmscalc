"""Adversarial and invariant tests for hmscalc.scheduling (all Python versions)."""

from __future__ import annotations

from datetime import date, datetime, timedelta

import pytest

from hmscalc.scheduling import (
    AvailabilitySlot,
    DateTimeRange,
    clip_interval,
    find_availability_across_days,
    find_availability_slots,
    find_availability_windows,
    free_time_gaps,
    merge_busy_intervals,
)


def _dt(text: str) -> datetime:
    return datetime.fromisoformat(text)


def _assert_slots_respect_buffers_and_busy(
    slots: list[AvailabilitySlot],
    busy: list[tuple[datetime, datetime]],
    window_start: datetime,
    window_end: datetime,
    duration: timedelta,
) -> None:
    """Every slot must fit in its gap and must not overlap merged busy time."""
    merged = merge_busy_intervals(busy)
    for slot in slots:
        assert slot.end - slot.start == duration
        assert slot.reserved_start == slot.start - slot.buffer_before
        assert slot.reserved_end == slot.end + slot.buffer_after
        assert slot.reserved_start >= slot.free_gap.start
        assert slot.reserved_end <= slot.free_gap.end
        assert slot.start >= window_start
        assert slot.end <= window_end
        for busy_range in merged:
            overlaps = slot.reserved_start < busy_range.end and slot.reserved_end > busy_range.start
            assert not overlaps, (
                f"slot {slot.start}–{slot.reserved_end} overlaps busy " f"{busy_range.start}–{busy_range.end}"
            )


def test_empty_busy_yields_full_window_gap() -> None:
    """With no busy blocks the entire window is one free gap."""
    window_start = _dt("2026-06-28 09:00")
    window_end = _dt("2026-06-28 18:00")
    gaps = free_time_gaps([], window_start, window_end)
    assert gaps == [DateTimeRange(window_start, window_end)]


def test_busy_covers_entire_window_no_gaps() -> None:
    """Busy covering the whole window leaves no availability."""
    busy = [(_dt("2026-06-28 09:00"), _dt("2026-06-28 18:00"))]
    gaps = free_time_gaps(busy, _dt("2026-06-28 09:00"), _dt("2026-06-28 18:00"))
    assert gaps == []
    assert (
        find_availability_slots(
            busy,
            _dt("2026-06-28 09:00"),
            _dt("2026-06-28 18:00"),
            duration="1:00",
        )
        == []
    )


def test_busy_outside_window_is_ignored() -> None:
    """Busy intervals completely outside the search window do not affect gaps."""
    busy = [(_dt("2026-06-27 09:00"), _dt("2026-06-27 10:00"))]
    gaps = free_time_gaps(busy, _dt("2026-06-28 09:00"), _dt("2026-06-28 12:00"))
    assert gaps == [DateTimeRange(_dt("2026-06-28 09:00"), _dt("2026-06-28 12:00"))]


def test_busy_unsorted_input_still_merges() -> None:
    """Merge must sort intervals before combining overlaps."""
    busy = [
        (_dt("2026-06-28 12:00"), _dt("2026-06-28 13:00")),
        (_dt("2026-06-28 09:00"), _dt("2026-06-28 10:00")),
        (_dt("2026-06-28 09:30"), _dt("2026-06-28 10:30")),
    ]
    merged = merge_busy_intervals(busy)
    assert len(merged) == 2
    assert merged[0].end == _dt("2026-06-28 10:30")


def test_back_to_back_busy_merges_no_interior_gap() -> None:
    """Adjacent busy blocks merge; there must be zero free time between them."""
    busy = [
        (_dt("2026-06-28 09:00"), _dt("2026-06-28 10:00")),
        (_dt("2026-06-28 10:00"), _dt("2026-06-28 11:00")),
    ]
    gaps = free_time_gaps(busy, _dt("2026-06-28 09:00"), _dt("2026-06-28 12:00"))
    assert gaps == [DateTimeRange(_dt("2026-06-28 11:00"), _dt("2026-06-28 12:00"))]


def test_one_minute_gap_too_short_for_buffered_hour() -> None:
    """A 1-minute gap cannot host 1h + 15m buffers on each side."""
    busy = [
        (_dt("2026-06-28 09:00"), _dt("2026-06-28 10:00")),
        (_dt("2026-06-28 10:01"), _dt("2026-06-28 12:00")),
    ]
    windows = find_availability_windows(
        busy,
        _dt("2026-06-28 09:00"),
        _dt("2026-06-28 18:00"),
        duration="1:00",
        buffer_before="0:15",
        buffer_after="0:15",
    )
    gap_starts = [window.free_gap.start for window in windows]
    assert _dt("2026-06-28 10:00") not in gap_starts


def test_exact_fit_gap_accepts_single_start() -> None:
    """Gap length exactly equal to duration + buffers allows one slot in that gap."""
    # gap 10:00–11:30 = 90min; 15 + 60 + 15 = 90
    busy = [
        (_dt("2026-06-28 09:00"), _dt("2026-06-28 10:00")),
        (_dt("2026-06-28 11:30"), _dt("2026-06-28 12:00")),
    ]
    windows = find_availability_windows(
        busy,
        _dt("2026-06-28 09:00"),
        _dt("2026-06-28 18:00"),
        duration="1:00",
        buffer_before="0:15",
        buffer_after="0:15",
    )
    tight = [window for window in windows if window.free_gap.end == _dt("2026-06-28 11:30")]
    assert len(tight) == 1
    assert tight[0].earliest_start == tight[0].latest_start == _dt("2026-06-28 10:15")


def test_zero_buffers_allows_back_to_back_meetings() -> None:
    """With zero buffers a meeting may start immediately after busy ends."""
    busy = [(_dt("2026-06-28 09:00"), _dt("2026-06-28 10:00"))]
    slots = find_availability_slots(
        busy,
        _dt("2026-06-28 09:00"),
        _dt("2026-06-28 12:00"),
        duration="0:30",
        buffer_before="0:00",
        buffer_after="0:00",
        step="0:30",
    )
    assert slots[0].start == _dt("2026-06-28 10:00")
    _assert_slots_respect_buffers_and_busy(
        slots,
        busy,
        _dt("2026-06-28 09:00"),
        _dt("2026-06-28 12:00"),
        timedelta(minutes=30),
    )


def test_gaps_partition_window_minus_busy() -> None:
    """Free gaps plus busy (clipped) must partition the search window."""
    window_start = _dt("2026-06-28 08:00")
    window_end = _dt("2026-06-28 20:00")
    busy = [
        (_dt("2026-06-28 09:00"), _dt("2026-06-28 10:30")),
        (_dt("2026-06-28 12:00"), _dt("2026-06-28 13:00")),
        (_dt("2026-06-28 17:00"), _dt("2026-06-28 21:00")),  # clipped at 20:00
    ]
    gaps = free_time_gaps(busy, window_start, window_end)
    merged = merge_busy_intervals(
        [clip for interval in busy if (clip := clip_interval(interval, window_start, window_end))]
    )

    total_gap = sum((gap.duration for gap in gaps), timedelta())
    total_busy = sum((item.duration for item in merged), timedelta())
    assert total_gap + total_busy == window_end - window_start


def test_all_generated_slots_satisfy_invariants() -> None:
    """Stress: many busy blocks; every returned slot must be valid."""
    window_start = _dt("2026-06-28 08:00")
    window_end = _dt("2026-06-28 20:00")
    busy = [
        (_dt("2026-06-28 08:30"), _dt("2026-06-28 09:15")),
        (_dt("2026-06-28 10:00"), _dt("2026-06-28 11:00")),
        (_dt("2026-06-28 11:00"), _dt("2026-06-28 11:45")),
        (_dt("2026-06-28 13:00"), _dt("2026-06-28 14:30")),
        (_dt("2026-06-28 16:00"), _dt("2026-06-28 16:15")),
        (_dt("2026-06-28 19:00"), _dt("2026-06-28 21:00")),
    ]
    duration = timedelta(hours=1)
    slots = find_availability_slots(
        busy,
        window_start,
        window_end,
        duration=duration,
        buffer_before="0:15",
        buffer_after="0:15",
        step="0:15",
    )
    assert len(slots) > 0
    _assert_slots_respect_buffers_and_busy(slots, busy, window_start, window_end, duration)
    assert slots == sorted(slots, key=lambda slot: slot.start)


def test_latest_start_slot_still_fits_buffers() -> None:
    """The last start time in a window must still leave room for buffers."""
    busy = [(_dt("2026-06-28 09:00"), _dt("2026-06-28 10:00"))]
    windows = find_availability_windows(
        busy,
        _dt("2026-06-28 09:00"),
        _dt("2026-06-28 12:00"),
        duration="1:00",
        buffer_before="0:15",
        buffer_after="0:15",
    )
    window = windows[0]
    last_slot = DateTimeRange(window.latest_start, window.latest_start + window.meeting_duration)
    assert last_slot.end + window.buffer_after <= window.free_gap.end


def test_invalid_window_raises() -> None:
    """window_start >= window_end is rejected."""
    with pytest.raises(ValueError, match="window_start must be before window_end"):
        free_time_gaps([], _dt("2026-06-28 18:00"), _dt("2026-06-28 09:00"))


def test_invalid_datetime_range_raises() -> None:
    """DateTimeRange rejects start >= end."""
    with pytest.raises(ValueError, match="start must be before end"):
        DateTimeRange(_dt("2026-06-28 10:00"), _dt("2026-06-28 10:00"))


def test_clip_interval_returns_none_when_disjoint() -> None:
    """Clipping a disjoint interval to the window yields None."""
    assert (
        clip_interval(
            (_dt("2026-06-28 13:00"), _dt("2026-06-28 14:00")),
            _dt("2026-06-28 09:00"),
            _dt("2026-06-28 12:00"),
        )
        is None
    )


def test_merge_idempotent() -> None:
    """merge(merge(x)) equals merge(x)."""
    busy = [
        (_dt("2026-06-28 09:00"), _dt("2026-06-28 10:00")),
        (_dt("2026-06-28 09:30"), _dt("2026-06-28 11:00")),
        (_dt("2026-06-28 14:00"), _dt("2026-06-28 15:00")),
    ]
    once = merge_busy_intervals(busy)
    twice = merge_busy_intervals(once)
    assert once == twice


def test_across_days_skips_invalid_daily_hours() -> None:
    """When daily_start >= daily_end no slots are produced for that day."""
    slots = find_availability_across_days(
        [],
        date(2026, 6, 28),
        date(2026, 6, 28),
        daily_start="18:00",
        daily_end="9:00",
        duration="1:00",
    )
    assert slots == []


def test_across_days_busy_spanning_midnight_only_affects_relevant_day() -> None:
    """Multi-day busy clipped per day must not wipe unrelated days."""
    busy = [(_dt("2026-06-28 17:00"), _dt("2026-06-29 10:00"))]
    slots_day2 = find_availability_across_days(
        busy,
        date(2026, 6, 29),
        date(2026, 6, 29),
        daily_start="9:00",
        daily_end="18:00",
        duration="1:00",
        buffer_before="0:15",
        buffer_after="0:15",
        step="1:00",
    )
    assert all(slot.start.date() == date(2026, 6, 29) for slot in slots_day2)
    assert slots_day2[0].start == _dt("2026-06-29 10:15")


def test_step_smaller_than_duration_allows_overlapping_starts() -> None:
    """Documented behavior: overlapping candidate meetings when step < duration."""
    busy = [(_dt("2026-06-28 09:00"), _dt("2026-06-28 10:00"))]
    slots = find_availability_slots(
        busy,
        _dt("2026-06-28 09:00"),
        _dt("2026-06-28 12:00"),
        duration="1:00",
        buffer_before="0:15",
        buffer_after="0:15",
        step="0:15",
    )
    assert len(slots) == 3
    assert slots[0].start < slots[1].start < slots[2].start
    assert slots[0].end > slots[1].start  # overlapping meetings


def test_iter_slots_rejects_non_positive_step() -> None:
    """AvailabilityWindow.iter_slots rejects zero/negative step."""
    window = find_availability_windows(
        [],
        _dt("2026-06-28 09:00"),
        _dt("2026-06-28 18:00"),
        duration="1:00",
    )[0]
    with pytest.raises(ValueError, match="step must be positive"):
        list(window.iter_slots(timedelta(0)))
