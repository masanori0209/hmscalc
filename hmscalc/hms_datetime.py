"""Combined calendar date and HMSTime duration."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Union

from . import dates
from .hms_time import HMSTime

DurationInput = Union[HMSTime, str]


@dataclass(frozen=True, order=True)
class HMSDateTime:
    """Calendar date paired with an :class:`HMSTime` duration or clock offset."""

    day: date
    time: HMSTime

    @classmethod
    def from_strings(
        cls,
        date_str: str,
        time_str: str,
        *,
        strict: bool = True,
    ) -> HMSDateTime:
        """Build from ``YYYY-MM-DD`` and HMS strings."""
        return cls(dates.parse_date(date_str), HMSTime(time_str, strict=strict))

    @classmethod
    def from_datetime(cls, value: datetime) -> HMSDateTime:
        """Split a :class:`datetime.datetime` into date and time-of-day."""
        midnight = datetime.combine(value.date(), datetime.min.time())
        delta = value - midnight
        return cls(value.date(), HMSTime.from_timedelta(delta))

    @classmethod
    def combine(cls, day: date, duration: DurationInput, *, strict: bool = True) -> HMSDateTime:
        """Combine a date with an HMS duration string or :class:`HMSTime`."""
        if isinstance(duration, str):
            time_value = HMSTime(duration, strict=strict)
        else:
            time_value = duration
        return cls(day, time_value)

    def to_datetime(self) -> datetime:
        """Return a naive :class:`datetime.datetime` for this value."""
        return dates.combine(self.day, str(self.time))

    def to_iso(self) -> str:
        """Return ``YYYY-MM-DDTHH:MM:SS`` without timezone."""
        return f"{self.day.isoformat()}T{self.time.format('HH:MM:SS:PADDED')}"

    def format_time(self, fmt: str = "HH:MM:SS") -> str:
        """Format the time component."""
        return self.time.format(fmt)

    def __add__(self, other: timedelta) -> HMSDateTime:
        """Add a timedelta to this value."""
        if not isinstance(other, timedelta):
            return NotImplemented
        return HMSDateTime.from_datetime(self.to_datetime() + other)

    def __sub__(self, other: Union[HMSDateTime, timedelta]) -> Union[HMSDateTime, timedelta]:
        """Subtract a timedelta or another HMSDateTime."""
        if isinstance(other, timedelta):
            return HMSDateTime.from_datetime(self.to_datetime() - other)
        if isinstance(other, HMSDateTime):
            return self.to_datetime() - other.to_datetime()
        return NotImplemented

    def __repr__(self) -> str:
        """Return the official string representation."""
        return f"HMSDateTime({self.day!r}, {self.time!r})"
