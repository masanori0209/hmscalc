"""hmscalc: A package for HMS (hours, minutes, seconds) calculations."""

from .exceptions import HMSTimeError, InvalidTimeFormatError, NotTimeStringError
from .hms_time import HMSTime

__all__ = [
    "HMSTime",
    "HMSTimeError",
    "InvalidTimeFormatError",
    "NotTimeStringError",
]
