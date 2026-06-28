"""Scheduling helpers: free gaps, availability windows, and buffered time slots."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from typing import Iterable, Iterator, Optional, Tuple, Union

from .business_days import BusinessCalendar, iter_business_days
from .dates import parse_datetime
from .hms_time import HMSTime

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    ZoneInfo = None  # type: ignore[misc, assignment]

DateTimeInput = Union[datetime, str]
IntervalInput = Union[Tuple[DateTimeInput, DateTimeInput], "DateTimeRange"]
TzInput = Union[str, "ZoneInfo"]


def _as_zoneinfo(tz: TzInput) -> ZoneInfo:
    if ZoneInfo is None:
        raise RuntimeError("zoneinfo is unavailable")
    if isinstance(tz, ZoneInfo):
        return tz
    if isinstance(tz, str):
        return ZoneInfo(tz)
    raise TypeError("expected timezone name or ZoneInfo")


def _as_datetime(value: DateTimeInput, tz: Optional[ZoneInfo] = None) -> datetime:
    if isinstance(value, datetime):
        dt = value
    elif isinstance(value, str):
        dt = parse_datetime(value)
    else:
        raise TypeError("expected datetime or parseable datetime string")

    if tz is None:
        return dt
    if dt.tzinfo is None:
        return dt.replace(tzinfo=tz)
    return dt.astimezone(tz)


def _as_timedelta(value: timedelta | str) -> timedelta:
    if isinstance(value, timedelta):
        return value
    if isinstance(value, str):
        return HMSTime(value).to_timedelta()
    raise TypeError("expected timedelta or HMSTime-compatible string")


@dataclass(frozen=True)
class DateTimeRange:
    """Inclusive interval ``[start, end]`` for scheduling."""

    start: datetime
    end: datetime

    def __post_init__(self) -> None:
        """Validate that the interval start precedes the end."""
        if self.start >= self.end:
            raise ValueError("start must be before end")

    @property
    def duration(self) -> timedelta:
        """Return the span of this interval."""
        return self.end - self.start


@dataclass(frozen=True)
class AvailabilityWindow:
    """Range of valid meeting start times inside one free gap."""

    earliest_start: datetime
    latest_start: datetime
    meeting_duration: timedelta
    buffer_before: timedelta
    buffer_after: timedelta
    free_gap: DateTimeRange

    def iter_slots(self, step: timedelta | None = None) -> Iterator[DateTimeRange]:
        """Yield concrete meeting slots from earliest to latest start."""
        if step is None:
            step = self.meeting_duration
        if step <= timedelta(0):
            raise ValueError("step must be positive")

        current = self.earliest_start
        while current <= self.latest_start:
            yield DateTimeRange(current, current + self.meeting_duration)
            current += step


@dataclass(frozen=True)
class AvailabilitySlot:
    """One bookable meeting slot including buffer context."""

    start: datetime
    end: datetime
    buffer_before: timedelta
    buffer_after: timedelta
    free_gap: DateTimeRange

    @property
    def reserved_start(self) -> datetime:
        """First datetime occupied including the leading buffer."""
        return self.start - self.buffer_before

    @property
    def reserved_end(self) -> datetime:
        """Last datetime occupied including the trailing buffer."""
        return self.end + self.buffer_after


def _normalize_interval(interval: IntervalInput, tz: Optional[ZoneInfo]) -> IntervalInput:
    if tz is None:
        return interval
    if isinstance(interval, DateTimeRange):
        return DateTimeRange(_as_datetime(interval.start, tz), _as_datetime(interval.end, tz))
    start, end = interval
    return (_as_datetime(start, tz), _as_datetime(end, tz))


def _normalize_busy(busy: Iterable[IntervalInput], tz: Optional[ZoneInfo]) -> list[IntervalInput]:
    if tz is None:
        return list(busy)
    return [_normalize_interval(interval, tz) for interval in busy]


def _as_range(value: IntervalInput) -> DateTimeRange:
    if isinstance(value, DateTimeRange):
        return value
    start, end = value
    return DateTimeRange(_as_datetime(start), _as_datetime(end))


def _time_on_date(day: date, value: time | str, tz: Optional[ZoneInfo] = None) -> datetime:
    if isinstance(value, time):
        combined = datetime.combine(day, value)
    else:
        parsed = HMSTime(value)
        hh, mm, ss = parsed.to_tuple()
        combined = datetime.combine(day, time(hh, mm, ss))
    if tz is not None:
        return combined.replace(tzinfo=tz)
    return combined


def merge_busy_intervals(intervals: Iterable[IntervalInput]) -> list[DateTimeRange]:
    """Merge overlapping busy intervals while preserving order."""
    sorted_intervals = sorted((_as_range(item) for item in intervals), key=lambda item: item.start)
    if not sorted_intervals:
        return []

    merged: list[DateTimeRange] = [sorted_intervals[0]]
    for current in sorted_intervals[1:]:
        previous = merged[-1]
        if current.start <= previous.end:
            merged[-1] = DateTimeRange(previous.start, max(previous.end, current.end))
        else:
            merged.append(current)
    return merged


def clip_interval(
    interval: IntervalInput,
    window_start: DateTimeInput,
    window_end: DateTimeInput,
) -> DateTimeRange | None:
    """Clip an interval to a window, returning ``None`` if nothing remains."""
    window_from = _as_datetime(window_start)
    window_to = _as_datetime(window_end)
    current = _as_range(interval)
    start = max(current.start, window_from)
    end = min(current.end, window_to)
    if start >= end:
        return None
    return DateTimeRange(start, end)


def free_time_gaps(
    busy: Iterable[IntervalInput],
    window_start: DateTimeInput,
    window_end: DateTimeInput,
) -> list[DateTimeRange]:
    """Return free gaps between busy intervals inside ``[window_start, window_end]``."""
    window_from = _as_datetime(window_start)
    window_to = _as_datetime(window_end)
    if window_from >= window_to:
        raise ValueError("window_start must be before window_end")

    clipped = [
        clipped_interval
        for interval in busy
        if (clipped_interval := clip_interval(interval, window_from, window_to)) is not None
    ]
    merged = merge_busy_intervals(clipped)

    gaps: list[DateTimeRange] = []
    cursor = window_from
    for busy_interval in merged:
        if cursor < busy_interval.start:
            gaps.append(DateTimeRange(cursor, busy_interval.start))
        cursor = max(cursor, busy_interval.end)
    if cursor < window_to:
        gaps.append(DateTimeRange(cursor, window_to))
    return gaps


def find_availability_windows(
    busy: Iterable[IntervalInput],
    window_start: DateTimeInput,
    window_end: DateTimeInput,
    *,
    duration: timedelta | str,
    buffer_before: timedelta | str = timedelta(0),
    buffer_after: timedelta | str = timedelta(0),
) -> list[AvailabilityWindow]:
    """Find windows where a meeting fits with buffers before and after."""
    meeting_duration = _as_timedelta(duration)
    lead = _as_timedelta(buffer_before)
    trail = _as_timedelta(buffer_after)
    if meeting_duration <= timedelta(0):
        raise ValueError("duration must be positive")

    required = lead + meeting_duration + trail
    windows: list[AvailabilityWindow] = []

    for gap in free_time_gaps(busy, window_start, window_end):
        if gap.duration < required:
            continue
        earliest_start = gap.start + lead
        latest_start = gap.end - trail - meeting_duration
        if earliest_start > latest_start:
            continue
        windows.append(
            AvailabilityWindow(
                earliest_start=earliest_start,
                latest_start=latest_start,
                meeting_duration=meeting_duration,
                buffer_before=lead,
                buffer_after=trail,
                free_gap=gap,
            )
        )
    return windows


def find_availability_slots(
    busy: Iterable[IntervalInput],
    window_start: DateTimeInput,
    window_end: DateTimeInput,
    *,
    duration: timedelta | str,
    buffer_before: timedelta | str = timedelta(0),
    buffer_after: timedelta | str = timedelta(0),
    step: timedelta | str | None = None,
) -> list[AvailabilitySlot]:
    """Return concrete meeting slots that fit with buffers in each free gap."""
    lead = _as_timedelta(buffer_before)
    trail = _as_timedelta(buffer_after)
    slot_step = _as_timedelta(step) if step is not None else _as_timedelta(duration)

    slots: list[AvailabilitySlot] = []
    for window in find_availability_windows(
        busy,
        window_start,
        window_end,
        duration=duration,
        buffer_before=lead,
        buffer_after=trail,
    ):
        for meeting in window.iter_slots(slot_step):
            slots.append(
                AvailabilitySlot(
                    start=meeting.start,
                    end=meeting.end,
                    buffer_before=lead,
                    buffer_after=trail,
                    free_gap=window.free_gap,
                )
            )
    return slots


def find_availability_across_days(
    busy: Iterable[IntervalInput],
    start_date: date,
    end_date: date,
    *,
    daily_start: time | str,
    daily_end: time | str,
    duration: timedelta | str,
    buffer_before: timedelta | str = timedelta(0),
    buffer_after: timedelta | str = timedelta(0),
    step: timedelta | str | None = None,
    tz: TzInput | None = None,
) -> list[AvailabilitySlot]:
    """Search for availability within daily working hours across multiple days."""
    if start_date > end_date:
        raise ValueError("start_date must be on or before end_date")

    zone = _as_zoneinfo(tz) if tz is not None else None
    normalized_busy = _normalize_busy(busy, zone)
    slots: list[AvailabilitySlot] = []
    current = start_date
    while current <= end_date:
        window_start = _time_on_date(current, daily_start, zone)
        window_end = _time_on_date(current, daily_end, zone)
        if window_start < window_end:
            slots.extend(
                find_availability_slots(
                    normalized_busy,
                    window_start,
                    window_end,
                    duration=duration,
                    buffer_before=buffer_before,
                    buffer_after=buffer_after,
                    step=step,
                )
            )
        current += timedelta(days=1)
    return slots


def find_availability_across_business_days(
    busy: Iterable[IntervalInput],
    start_date: date,
    end_date: date,
    *,
    calendar: BusinessCalendar | None = None,
    daily_start: time | str,
    daily_end: time | str,
    duration: timedelta | str,
    buffer_before: timedelta | str = timedelta(0),
    buffer_after: timedelta | str = timedelta(0),
    step: timedelta | str | None = None,
    tz: TzInput | None = None,
) -> list[AvailabilitySlot]:
    """Search for availability on business days only, skipping weekends and holidays."""
    if start_date > end_date:
        raise ValueError("start_date must be on or before end_date")

    zone = _as_zoneinfo(tz) if tz is not None else None
    normalized_busy = _normalize_busy(busy, zone)
    slots: list[AvailabilitySlot] = []
    for current in iter_business_days(start_date, end_date, calendar=calendar):
        window_start = _time_on_date(current, daily_start, zone)
        window_end = _time_on_date(current, daily_end, zone)
        if window_start < window_end:
            slots.extend(
                find_availability_slots(
                    normalized_busy,
                    window_start,
                    window_end,
                    duration=duration,
                    buffer_before=buffer_before,
                    buffer_after=buffer_after,
                    step=step,
                )
            )
    return slots


def datetime_gap_ranges(
    busy: Iterable[IntervalInput],
    window_start: DateTimeInput,
    window_end: DateTimeInput,
) -> list[DateTimeRange]:
    """Return free datetime gaps (alias for :func:`free_time_gaps`)."""
    return free_time_gaps(busy, window_start, window_end)
