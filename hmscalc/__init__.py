"""hmscalc: A package for HMS (hours, minutes, seconds) calculations.

Public API
----------
HMSTime
    Core type for HH:MM / HH:MM:SS duration arithmetic.
HMSTimeError
    Base exception for hmscalc errors.
InvalidTimeFormatError
    Raised for malformed time strings.
NotTimeStringError
    Raised when input is not a string.

See README.md for usage examples.
"""

from .exceptions import HMSTimeError, InvalidTimeFormatError, NotTimeStringError
from .hms_time import HMSTime

__all__ = [
    "HMSTime",
    "HMSTimeError",
    "InvalidTimeFormatError",
    "NotTimeStringError",
]
