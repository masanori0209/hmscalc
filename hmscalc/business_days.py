"""Business-day calendar helpers with weekday and holiday rules."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Iterable, Iterator

DEFAULT_WEEKDAYS = frozenset({0, 1, 2, 3, 4})


@dataclass(frozen=True)
class BusinessCalendar:
    """Working-day calendar with configurable weekdays and holidays."""

    weekdays: frozenset[int] = DEFAULT_WEEKDAYS
    holidays: frozenset[date] = frozenset()

    def __post_init__(self) -> None:
        for weekday in self.weekdays:
            if not 0 <= weekday <= 6:
                raise ValueError("weekdays must be integers in 0..6 (Mon=0, Sun=6)")

    @classmethod
    def weekdays_only(cls, *, holidays: Iterable[date] = ()) -> BusinessCalendar:
        """Build a Mon–Fri calendar with optional holiday exclusions."""
        return cls(holidays=frozenset(holidays))

    def is_business_day(self, day: date) -> bool:
        """Return ``True`` when ``day`` is a configured working day."""
        return day.weekday() in self.weekdays and day not in self.holidays


def _calendar(calendar: BusinessCalendar | None) -> BusinessCalendar:
    return calendar if calendar is not None else BusinessCalendar()


def is_business_day(day: date, *, calendar: BusinessCalendar | None = None) -> bool:
    """Return whether ``day`` is a business day."""
    return _calendar(calendar).is_business_day(day)


def iter_business_days(
    start: date,
    end: date,
    *,
    calendar: BusinessCalendar | None = None,
) -> Iterator[date]:
    """Yield business days from ``start`` through ``end`` inclusive."""
    if start > end:
        return

    cal = _calendar(calendar)
    current = start
    while current <= end:
        if cal.is_business_day(current):
            yield current
        current += timedelta(days=1)


def business_day_range(
    start: date,
    end: date,
    *,
    calendar: BusinessCalendar | None = None,
) -> list[date]:
    """Return business days from ``start`` through ``end`` inclusive."""
    return list(iter_business_days(start, end, calendar=calendar))


def count_business_days(
    start: date,
    end: date,
    *,
    calendar: BusinessCalendar | None = None,
) -> int:
    """Count business days in the inclusive range ``[start, end]``."""
    return len(business_day_range(start, end, calendar=calendar))


def next_business_day(
    day: date,
    *,
    calendar: BusinessCalendar | None = None,
    inclusive: bool = False,
) -> date:
    """Return the next business day after ``day``, or including ``day`` when ``inclusive``."""
    cal = _calendar(calendar)
    current = day if inclusive else day + timedelta(days=1)
    while not cal.is_business_day(current):
        current += timedelta(days=1)
    return current


def previous_business_day(
    day: date,
    *,
    calendar: BusinessCalendar | None = None,
    inclusive: bool = False,
) -> date:
    """Return the previous business day before ``day``, or including ``day`` when ``inclusive``."""
    cal = _calendar(calendar)
    current = day if inclusive else day - timedelta(days=1)
    while not cal.is_business_day(current):
        current -= timedelta(days=1)
    return current


def add_business_days(
    day: date,
    count: int,
    *,
    calendar: BusinessCalendar | None = None,
) -> date:
    """Move ``count`` business days forward (positive) or backward (negative)."""
    if count == 0:
        return day

    cal = _calendar(calendar)
    current = day
    remaining = abs(count)
    step = timedelta(days=1) if count > 0 else timedelta(days=-1)

    while remaining > 0:
        current += step
        if cal.is_business_day(current):
            remaining -= 1
    return current
