"""Module for handling time in hours, minutes, and seconds (HMS) format."""

from __future__ import annotations

import re
from datetime import timedelta
from typing import Iterable

from .exceptions import InvalidTimeFormatError, NotTimeStringError

_ISO8601_DURATION_RE = re.compile(
    r"^(-?)P"
    r"(?:(\d+(?:\.\d+)?)Y)?"
    r"(?:(\d+(?:\.\d+)?)M)?"
    r"(?:(\d+(?:\.\d+)?)W)?"
    r"(?:(\d+(?:\.\d+)?)D)?"
    r"(?:T(?:(\d+(?:\.\d+)?)H)?(?:(\d+(?:\.\d+)?)M)?(?:(\d+(?:\.\d+)?)S)?)?$",
    re.IGNORECASE,
)
_SECONDS_PER_DAY = 86_400
_SECONDS_PER_WEEK = 7 * _SECONDS_PER_DAY
_SECONDS_PER_MONTH = 30 * _SECONDS_PER_DAY
_SECONDS_PER_YEAR = 365 * _SECONDS_PER_DAY
_SUPPORTED_FORMATS = frozenset({"HH:MM", "HH:MM:SS", "HH:MM:SS:PADDED"})


class HMSTime:
    """Class to represent and manipulate time in hours, minutes, and seconds (HMS) format.

    Args:
    ----
        time_str (str): Time string to parse.

    """

    def __init__(self, time_str: str, *, strict: bool = True):
        """Initialize HMSTime from a time string in 'HH:MM:SS' or 'HH:MM' format.

        Args:
        ----
            time_str (str): Time string to parse.
            strict (bool): When ``False``, overflow minutes/seconds are normalized
                (e.g. ``"1:90:00"`` → ``"2:30:00"``). Default is strict validation.

        """
        self.total_seconds = self._parse_time_string(time_str, strict=strict)

    @property
    def hh(self) -> int:
        """Return absolute hours component."""
        return self.to_tuple()[0]

    @property
    def mm(self) -> int:
        """Return absolute minutes component."""
        return self.to_tuple()[1]

    @property
    def ss(self) -> int:
        """Return absolute seconds component."""
        return self.to_tuple()[2]

    @property
    def is_negative(self) -> bool:
        """Return True if this time value is negative."""
        return self.total_seconds < 0

    def __add__(self, other: object) -> "HMSTime":
        """Add HMSTime or timedelta and return a new HMSTime object."""
        if isinstance(other, HMSTime):
            return HMSTime.from_seconds(self.total_seconds + other.total_seconds)
        if isinstance(other, timedelta):
            return HMSTime.from_seconds(self.total_seconds + int(other.total_seconds()))
        return NotImplemented

    def __radd__(self, other: object) -> "HMSTime":
        """Support timedelta + HMSTime."""
        if isinstance(other, timedelta):
            return self.__add__(other)
        return NotImplemented

    def __sub__(self, other: object) -> "HMSTime":
        """Subtract HMSTime or timedelta and return a new HMSTime object."""
        if isinstance(other, HMSTime):
            return HMSTime.from_seconds(self.total_seconds - other.total_seconds)
        if isinstance(other, timedelta):
            return HMSTime.from_seconds(self.total_seconds - int(other.total_seconds()))
        return NotImplemented

    def __abs__(self) -> "HMSTime":
        """Return the absolute value of this duration."""
        return HMSTime.from_seconds(abs(self.total_seconds))

    def __str__(self) -> str:
        """Return the string representation of the HMSTime object in 'HH:MM:SS' format.

        Returns
        -------
            str: The string representation of the HMSTime object.

        """
        total = abs(self.total_seconds)
        hh = total // 3600
        mm = (total % 3600) // 60
        ss = total % 60
        sign = "-" if self.total_seconds < 0 else ""
        return f"{sign}{hh}:{mm:02}:{ss:02}"

    def __repr__(self) -> str:
        """Return the official string representation of the HMSTime object."""
        return f"HMSTime('{self}')"

    def __eq__(self, other: object) -> bool:
        """Check if two HMSTime objects are equal."""
        if not isinstance(other, HMSTime):
            return NotImplemented
        return self.total_seconds == other.total_seconds

    def __lt__(self, other: object) -> bool:
        """Check if this HMSTime object is less than another."""
        if not isinstance(other, HMSTime):
            return NotImplemented
        return self.total_seconds < other.total_seconds

    def __le__(self, other: object) -> bool:
        """Check if this HMSTime object is less than or equal to another."""
        if not isinstance(other, HMSTime):
            return NotImplemented
        return self.total_seconds <= other.total_seconds

    def __gt__(self, other: object) -> bool:
        """Check if this HMSTime object is greater than another."""
        if not isinstance(other, HMSTime):
            return NotImplemented
        return self.total_seconds > other.total_seconds

    def __ge__(self, other: object) -> bool:
        """Check if this HMSTime object is greater than or equal to another."""
        if not isinstance(other, HMSTime):
            return NotImplemented
        return self.total_seconds >= other.total_seconds

    def __ne__(self, other: object) -> bool:
        """Check if two HMSTime objects are not equal."""
        if not isinstance(other, HMSTime):
            return NotImplemented
        return self.total_seconds != other.total_seconds

    def __hash__(self) -> int:
        """Return a hash based on total seconds."""
        return hash(self.total_seconds)

    def __mul__(self, other: object) -> "HMSTime":
        """Multiply this time by a numeric scalar."""
        if isinstance(other, (int, float)):
            return HMSTime.from_seconds(round(self.total_seconds * other))
        return NotImplemented

    def __rmul__(self, other: object) -> "HMSTime":
        """Support scalar * HMSTime."""
        if isinstance(other, (int, float)):
            return HMSTime.from_seconds(round(self.total_seconds * other))
        return NotImplemented

    def __truediv__(self, other: object) -> "HMSTime":
        """Divide this time by a numeric scalar."""
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("Cannot divide HMSTime by zero")
            return HMSTime.from_seconds(round(self.total_seconds / other))
        return NotImplemented

    @classmethod
    def _time_list(cls, times: Iterable["HMSTime"], *, empty_error: str | None = None) -> list["HMSTime"]:
        """Convert an iterable to a validated list of HMSTime objects."""
        try:
            time_list = list(times)
        except TypeError as e:
            raise TypeError("Input must be an iterable of HMSTime objects") from e
        if empty_error is not None and not time_list:
            raise ValueError(empty_error)
        if time_list and not all(isinstance(t, cls) for t in time_list):
            raise TypeError("All items must be HMSTime objects")
        return time_list

    @classmethod
    def parse(cls, time_str: str, *, strict: bool = True) -> "HMSTime":
        """Parse a time string with optional lenient overflow normalization."""
        return cls(time_str, strict=strict)

    @classmethod
    def parse_many(cls, strings: Iterable[str], *, strict: bool = True) -> list["HMSTime"]:
        """Parse an iterable of time strings into HMSTime objects."""
        try:
            return [cls(value, strict=strict) for value in strings]
        except TypeError as exc:
            raise TypeError("Input must be an iterable of strings") from exc

    @classmethod
    def sum_strings(cls, strings: Iterable[str], *, strict: bool = True) -> "HMSTime":
        """Parse and sum time strings in one call."""
        return cls.sum(cls.parse_many(strings, strict=strict))

    @classmethod
    def from_seconds(cls, total_seconds: int) -> "HMSTime":
        """Create an HMSTime object from a total number of seconds.

        Args:
        ----
            total_seconds (int): The total number of seconds.

        Returns:
        -------
            HMSTime: The corresponding HMSTime object.

        Raises:
        ------
            TypeError: If ``total_seconds`` is not an ``int`` (``bool`` is rejected).

        """
        if isinstance(total_seconds, bool) or not isinstance(total_seconds, int):
            raise TypeError("total_seconds must be an int")
        instance = cls.__new__(cls)
        instance.total_seconds = total_seconds
        return instance

    @classmethod
    def from_timedelta(cls, delta: timedelta) -> "HMSTime":
        """Create an HMSTime object from a datetime.timedelta.

        Args:
        ----
            delta (timedelta): The timedelta to convert.

        Returns:
        -------
            HMSTime: The corresponding HMSTime object.

        """
        return cls.from_seconds(int(delta.total_seconds()))

    @classmethod
    def from_iso8601(cls, duration: str) -> "HMSTime":
        """Create an HMSTime from an ISO 8601 duration string.

        Supports time-only (``PT1H30M15S``), date-only (``P1D``, ``P1W``), and combined
        forms (``P1DT2H``). Months and years use nominal lengths (30 days / 365 days).

        Args:
        ----
            duration (str): ISO 8601 duration string.

        Returns:
        -------
            HMSTime: The parsed duration.

        Raises:
        ------
            NotTimeStringError: If input is not a string.
            InvalidTimeFormatError: If the string is not a valid ISO 8601 duration.

        """
        if not isinstance(duration, str):
            raise NotTimeStringError(duration)

        duration = duration.strip()
        if not duration:
            raise InvalidTimeFormatError(duration)

        total_seconds = cls._parse_iso8601_duration(duration)
        return cls.from_seconds(total_seconds)

    @staticmethod
    def _parse_iso8601_duration(duration: str) -> int:
        match = _ISO8601_DURATION_RE.fullmatch(duration)
        if not match:
            raise InvalidTimeFormatError(duration)

        neg, years, months, weeks, days, hours, minutes, seconds = match.groups()
        components = (years, months, weeks, days, hours, minutes, seconds)
        if all(value is None for value in components):
            raise InvalidTimeFormatError(duration)

        if weeks is not None and any(value is not None for value in (years, months, days, hours, minutes, seconds)):
            raise InvalidTimeFormatError(duration)

        if weeks is None and hours is None and minutes is None and seconds is None:
            if years is None and months is None and days is None:
                raise InvalidTimeFormatError(duration)

        total = 0.0
        if years is not None:
            total += float(years) * _SECONDS_PER_YEAR
        if months is not None:
            total += float(months) * _SECONDS_PER_MONTH
        if weeks is not None:
            total += float(weeks) * _SECONDS_PER_WEEK
        if days is not None:
            total += float(days) * _SECONDS_PER_DAY
        if hours is not None:
            total += float(hours) * 3600
        if minutes is not None:
            total += float(minutes) * 60
        if seconds is not None:
            total += float(seconds)

        total_seconds = round(total)
        if neg:
            total_seconds = -total_seconds
        return total_seconds

    @classmethod
    def sum(cls, times: Iterable["HMSTime"]) -> "HMSTime":
        """Sum multiple HMSTime objects and return a new HMSTime object.

        Args:
        ----
            times (Iterable[HMSTime]): An iterable of HMSTime objects to sum.

        Returns:
        -------
            HMSTime: The sum of all the times.

        Raises:
        ------
            TypeError: If the input is not iterable or contains non-HMSTime objects.

        """
        try:
            total_seconds = 0
            for time_obj in cls._time_list(times):
                total_seconds += time_obj.total_seconds
            return cls.from_seconds(total_seconds)
        except TypeError as e:
            if "not iterable" in str(e):
                raise TypeError("Input must be an iterable of HMSTime objects") from e
            raise

    @classmethod
    def average(cls, times: Iterable["HMSTime"]) -> "HMSTime":
        """Return the average of multiple HMSTime objects, rounded to the nearest second.

        Args:
        ----
            times (Iterable[HMSTime]): An iterable of HMSTime objects.

        Returns:
        -------
            HMSTime: The average time.

        Raises:
        ------
            TypeError: If the input is not iterable or contains non-HMSTime objects.
            ValueError: If the iterable is empty.

        """
        time_list = cls._time_list(times, empty_error="Cannot compute average of an empty iterable")
        total_seconds = sum(t.total_seconds for t in time_list)
        return cls.from_seconds(round(total_seconds / len(time_list)))

    @classmethod
    def min(cls, times: Iterable["HMSTime"]) -> "HMSTime":
        """Return the minimum HMSTime from an iterable.

        Args:
        ----
            times (Iterable[HMSTime]): An iterable of HMSTime objects.

        Returns:
        -------
            HMSTime: The smallest time value.

        Raises:
        ------
            TypeError: If the input is not iterable or contains non-HMSTime objects.
            ValueError: If the iterable is empty.

        """
        time_list = cls._time_list(times, empty_error="Cannot compute min of an empty iterable")
        return min(time_list, key=lambda t: t.total_seconds)

    @classmethod
    def max(cls, times: Iterable["HMSTime"]) -> "HMSTime":
        """Return the maximum HMSTime from an iterable.

        Args:
        ----
            times (Iterable[HMSTime]): An iterable of HMSTime objects.

        Returns:
        -------
            HMSTime: The largest time value.

        Raises:
        ------
            TypeError: If the input is not iterable or contains non-HMSTime objects.
            ValueError: If the iterable is empty.

        """
        time_list = cls._time_list(times, empty_error="Cannot compute max of an empty iterable")
        return max(time_list, key=lambda t: t.total_seconds)

    @staticmethod
    def _parse_time_string(time_str: str, *, strict: bool = True) -> int:
        """Parse a time string and return the total number of seconds.

        Args:
        ----
            time_str (str): Time string to parse.
            strict (bool): When ``False``, minutes and seconds may exceed 59.

        Returns:
        -------
            int: Total number of seconds represented by the string.

        Raises:
        ------
            NotTimeStringError: If input is not a string.
            InvalidTimeFormatError: If the string format is invalid.

        """
        if not isinstance(time_str, str):
            raise NotTimeStringError(time_str)

        time_str = time_str.strip()
        if not time_str:
            raise InvalidTimeFormatError(time_str)

        match = re.fullmatch(r"(-)?(\d+):(\d{1,2})(?::(\d{1,2}))?", time_str)
        if not match:
            raise InvalidTimeFormatError(time_str)
        neg, hh, mm, ss = match.groups()
        hh = int(hh)
        mm = int(mm)
        ss = int(ss) if ss is not None else 0

        if strict and (mm >= 60 or ss >= 60):
            raise InvalidTimeFormatError(time_str)

        total = hh * 3600 + mm * 60 + ss
        return -total if neg else total

    def format(self, fmt: str = "HH:MM:SS") -> str:
        """Format this duration as a string.

        ``HH:MM:SS`` matches :meth:`__str__`. ``HH:MM`` omits seconds.

        Args:
        ----
            fmt (str): ``"HH:MM"`` or ``"HH:MM:SS"``.

        Returns:
        -------
            str: Formatted duration.

        Raises:
        ------
            ValueError: If ``fmt`` is not supported.

        """
        if fmt not in _SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported format: {fmt!r}. Use 'HH:MM', 'HH:MM:SS', or 'HH:MM:SS:PADDED'."
            )
        if fmt == "HH:MM:SS":
            return str(self)
        hh, mm, ss = self.to_tuple()
        sign = "-" if self.is_negative else ""
        if fmt == "HH:MM:SS:PADDED":
            return f"{sign}{hh:02}:{mm:02}:{ss:02}"
        return f"{sign}{hh}:{mm:02}"

    def to_iso8601(self) -> str:
        """Return an ISO 8601 duration string (``P…`` / ``PT…`` / ``P…T…``)."""
        if self.total_seconds == 0:
            return "PT0S"
        sign = "-" if self.is_negative else ""
        total = abs(self.total_seconds)

        days, remainder = divmod(total, _SECONDS_PER_DAY)
        hh, remainder = divmod(remainder, 3600)
        mm, ss = divmod(remainder, 60)

        if days and not (hh or mm or ss):
            if days % 7 == 0:
                return f"{sign}P{days // 7}W"
            return f"{sign}P{days}D"

        time_parts: list[str] = []
        if hh:
            time_parts.append(f"{hh}H")
        if mm:
            time_parts.append(f"{mm}M")
        if ss or not time_parts:
            time_parts.append(f"{ss}S")

        if days:
            return f"{sign}P{days}DT{''.join(time_parts)}"
        return f"{sign}PT{''.join(time_parts)}"

    def to_seconds(self) -> int:
        """Return the total number of seconds represented by this HMSTime object."""
        return self.total_seconds

    def to_minutes(self) -> float:
        """Return the total number of minutes represented by this HMSTime object."""
        return self.total_seconds / 60

    def to_hours(self) -> float:
        """Return the total number of hours represented by this HMSTime object."""
        return self.total_seconds / 3600

    def to_timedelta(self) -> timedelta:
        """Return this time as a datetime.timedelta."""
        return timedelta(seconds=self.total_seconds)

    def to_tuple(self) -> tuple[int, int, int]:
        """Return the time as a tuple of (hours, minutes, seconds).

        Components are absolute values; use :attr:`is_negative` or :meth:`to_seconds`
        to determine sign.
        """
        total = abs(self.total_seconds)
        hh = total // 3600
        mm = (total % 3600) // 60
        ss = total % 60
        return (hh, mm, ss)

    def to_dict(self) -> dict[str, int | bool]:
        """Return the time as a dictionary with keys 'hh', 'mm', 'ss', and 'negative'."""
        hh, mm, ss = self.to_tuple()
        return {"hh": hh, "mm": mm, "ss": ss, "negative": self.is_negative}
