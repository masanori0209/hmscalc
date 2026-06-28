"""Calendar date and datetime utilities for hmscalc."""

from __future__ import annotations

import calendar
import re
from datetime import date, datetime, timedelta
from typing import Iterable, Iterator

from .exceptions import HMSTimeError
from .hms_time import HMSTime

_DATE_RE = re.compile(r"^(\d{4})[-/](\d{1,2})[-/](\d{1,2})$")
_DATETIME_RE = re.compile(
    r"^(\d{4})[-/](\d{1,2})[-/](\d{1,2})[ T](\d{1,2}):(\d{1,2})(?::(\d{1,2}))?$",
)


class InvalidDateFormatError(HMSTimeError):
    """Exception raised for invalid date or datetime strings."""

    def __init__(self, value: str) -> None:
        """Initialize with the invalid input."""
        super().__init__(f"Invalid date format: '{value}'")


def parse_date(value: str) -> date:
    """Parse ``YYYY-MM-DD`` or ``YYYY/MM/DD`` into a :class:`datetime.date`."""
    if not isinstance(value, str):
        raise InvalidDateFormatError(str(value))

    value = value.strip()
    match = _DATE_RE.fullmatch(value)
    if not match:
        raise InvalidDateFormatError(value)

    year, month, day = (int(part) for part in match.groups())
    try:
        return date(year, month, day)
    except ValueError as exc:
        raise InvalidDateFormatError(value) from exc


def parse_datetime(value: str) -> datetime:
    """Parse ``YYYY-MM-DD HH:MM[:SS]`` or slash-separated variants."""
    if not isinstance(value, str):
        raise InvalidDateFormatError(str(value))

    value = value.strip()
    match = _DATETIME_RE.fullmatch(value)
    if not match:
        raise InvalidDateFormatError(value)

    year, month, day, hour, minute, second = match.groups()
    second_val = int(second) if second is not None else 0
    try:
        return datetime(int(year), int(month), int(day), int(hour), int(minute), second_val)
    except ValueError as exc:
        raise InvalidDateFormatError(value) from exc


def monthrange(year: int, month: int) -> tuple[int, int]:
    """Return ``(weekday_of_first_day, days_in_month)`` like :func:`calendar.monthrange`."""
    if not 1 <= month <= 12:
        raise ValueError("month must be in 1..12")
    return calendar.monthrange(year, month)


def days_in_month(year: int, month: int) -> int:
    """Return the number of days in the given month."""
    return monthrange(year, month)[1]


def last_day_of_month(year: int, month: int) -> date:
    """Return the last calendar day of the given month."""
    return date(year, month, days_in_month(year, month))


def iter_dates(start: date, end: date, *, step_days: int = 1) -> Iterator[date]:
    """Yield each date from ``start`` through ``end`` inclusive."""
    if start > end:
        return
    if step_days <= 0:
        raise ValueError("step_days must be positive")

    current = start
    delta = timedelta(days=step_days)
    while current <= end:
        yield current
        current += delta


def date_range(start: date, end: date, *, step_days: int = 1) -> list[date]:
    """Return a list of dates from ``start`` through ``end`` inclusive."""
    return list(iter_dates(start, end, step_days=step_days))


def missing_dates(present: Iterable[date], start: date, end: date) -> list[date]:
    """Return dates in ``[start, end]`` that are absent from ``present``."""
    if start > end:
        raise ValueError("start must be on or before end")
    present_set = set(present)
    return [day for day in date_range(start, end) if day not in present_set]


def has_date_gaps(present: Iterable[date]) -> bool:
    """Return ``True`` if consecutive sorted dates are more than one day apart."""
    unique = sorted(set(present))
    if len(unique) < 2:
        return False
    return any((later - earlier).days > 1 for earlier, later in zip(unique, unique[1:]))


def gap_ranges(
    present: Iterable[date],
    *,
    start: date | None = None,
    end: date | None = None,
) -> list[tuple[date, date]]:
    """Return inclusive gap ranges ``(first_missing, last_missing)`` between present dates."""
    unique = sorted(set(present))
    if not unique:
        if start is not None and end is not None:
            if start > end:
                raise ValueError("start must be on or before end")
            return [(start, end)]
        return []

    range_start = start if start is not None else unique[0]
    range_end = end if end is not None else unique[-1]
    if range_start > range_end:
        raise ValueError("start must be on or before end")

    present_set = set(unique)
    gaps: list[tuple[date, date]] = []
    gap_start: date | None = None

    for day in date_range(range_start, range_end):
        if day in present_set:
            if gap_start is not None:
                gaps.append((gap_start, day - timedelta(days=1)))
                gap_start = None
            continue
        if gap_start is None:
            gap_start = day

    if gap_start is not None:
        gaps.append((gap_start, range_end))

    return gaps


def combine(date_value: date, time_str: str) -> datetime:
    """Combine a calendar date with an :class:`HMSTime` duration string."""
    base = datetime.combine(date_value, datetime.min.time())
    return base + HMSTime(time_str).to_timedelta()


def missing_datetimes(
    present: Iterable[datetime],
    start: datetime,
    end: datetime,
    *,
    step: timedelta = timedelta(days=1),
) -> list[datetime]:
    """Return datetimes in ``[start, end]`` at ``step`` intervals that are absent."""
    if start > end:
        raise ValueError("start must be on or before end")
    if step <= timedelta(0):
        raise ValueError("step must be positive")

    present_set = set(present)
    missing: list[datetime] = []
    current = start
    while current <= end:
        if current not in present_set:
            missing.append(current)
        current += step
    return missing
