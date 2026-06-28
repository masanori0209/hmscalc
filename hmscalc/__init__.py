"""hmscalc: A package for HMS (hours, minutes, seconds) calculations.

Public API
----------
HMSTime
    Core type for HH:MM / HH:MM:SS duration arithmetic.
HMSDateTime
    Combined calendar date and HMSTime value.
HMSTimeError
    Base exception for hmscalc errors.
InvalidTimeFormatError
    Raised for malformed time strings.
NotTimeStringError
    Raised when input is not a string.
InvalidDateFormatError
    Raised for malformed date or datetime strings.
dates
    Calendar helpers: month end, date ranges, gap detection, parse_date.
business_days
    Business-day calendar: weekdays, holidays, add/count business days.
buckets
    Weekly and monthly duration aggregation.
scheduling
    Availability search with buffers for meeting scheduling.
tz
    Timezone helpers: parse with tz, localize, daily windows (zoneinfo).
pandas_extra
    Optional pandas helpers (requires ``hmscalc[pandas]``).

See README.md for usage examples.
"""

from . import buckets, business_days, dates, pandas_extra, scheduling, tz
from .buckets import BucketTotal
from .dates import InvalidDateFormatError
from .exceptions import HMSTimeError, InvalidTimeFormatError, NotTimeStringError
from .hms_datetime import HMSDateTime
from .hms_time import HMSTime

__all__ = [
    "HMSTime",
    "HMSDateTime",
    "BucketTotal",
    "HMSTimeError",
    "InvalidDateFormatError",
    "InvalidTimeFormatError",
    "NotTimeStringError",
    "buckets",
    "business_days",
    "dates",
    "pandas_extra",
    "scheduling",
    "tz",
]
