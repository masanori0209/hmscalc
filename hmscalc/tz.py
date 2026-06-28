"""Timezone helpers built on :mod:`zoneinfo` (stdlib)."""

from __future__ import annotations

from datetime import date, datetime, time, timezone
from typing import Union
from zoneinfo import ZoneInfo

from .dates import parse_datetime as parse_naive_datetime
from .hms_time import HMSTime

TzInput = Union[str, ZoneInfo]


def as_zoneinfo(tz: TzInput) -> ZoneInfo:
    """Coerce a timezone name or :class:`ZoneInfo` instance."""
    if isinstance(tz, ZoneInfo):
        return tz
    if isinstance(tz, str):
        return ZoneInfo(tz)
    raise TypeError("expected timezone name or ZoneInfo")


def parse_datetime(value: str, *, tz: TzInput | None = None) -> datetime:
    """Parse a datetime string and optionally attach a timezone."""
    naive = parse_naive_datetime(value)
    if tz is None:
        return naive
    return localize(naive, tz)


def localize(naive: datetime, tz: TzInput) -> datetime:
    """Attach ``tz`` to a naive datetime without shifting clock time."""
    if naive.tzinfo is not None:
        raise ValueError("datetime is already timezone-aware")
    return naive.replace(tzinfo=as_zoneinfo(tz))


def to_timezone(dt: datetime, tz: TzInput) -> datetime:
    """Convert an aware datetime to ``tz``."""
    if dt.tzinfo is None:
        raise ValueError("naive datetime cannot be converted; use localize() first")
    return dt.astimezone(as_zoneinfo(tz))


def local_to_utc(dt: datetime) -> datetime:
    """Convert an aware datetime to UTC."""
    if dt.tzinfo is None:
        raise ValueError("naive datetime cannot be converted to UTC")
    return dt.astimezone(timezone.utc)


def daily_window(
    day: date,
    daily_start: time | str,
    daily_end: time | str,
    tz: TzInput,
) -> tuple[datetime, datetime]:
    """Return a timezone-aware daily working window for ``day`` in ``tz``."""
    zone = as_zoneinfo(tz)
    start_dt = time_on_date(day, daily_start, zone)
    end_dt = time_on_date(day, daily_end, zone)
    if start_dt >= end_dt:
        raise ValueError("daily_start must be before daily_end")
    return start_dt, end_dt


def time_on_date(day: date, value: time | str, tz: TzInput) -> datetime:
    """Combine ``day`` and clock time in ``tz``."""
    zone = as_zoneinfo(tz)
    if isinstance(value, time):
        combined = datetime.combine(day, value)
    else:
        parsed = HMSTime(value)
        hh, mm, ss = parsed.to_tuple()
        combined = datetime.combine(day, time(hh, mm, ss))
    return combined.replace(tzinfo=zone)
