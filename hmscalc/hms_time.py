import re
from .exceptions import InvalidTimeFormatError, NotTimeStringError


class HMSTime:
    def __init__(self, time_str: str):
        self.total_seconds = self._parse_time_string(time_str)

    def __add__(self, other: "HMSTime") -> "HMSTime":
        return HMSTime.from_seconds(self.total_seconds + other.total_seconds)

    def __sub__(self, other: "HMSTime") -> "HMSTime":
        return HMSTime.from_seconds(self.total_seconds - other.total_seconds)

    def __str__(self) -> str:
        total = abs(self.total_seconds)
        hh = total // 3600
        mm = (total % 3600) // 60
        ss = total % 60
        sign = "-" if self.total_seconds < 0 else ""
        return f"{sign}{hh}:{mm:02}:{ss:02}"

    def __repr__(self) -> str:
        return f"HMSTime('{self}')"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HMSTime):
            return NotImplemented
        return self.total_seconds == other.total_seconds

    def __lt__(self, other: "HMSTime") -> bool:
        return self.total_seconds < other.total_seconds

    def __le__(self, other: "HMSTime") -> bool:
        return self.total_seconds <= other.total_seconds

    def __gt__(self, other: "HMSTime") -> bool:
        return self.total_seconds > other.total_seconds

    def __ge__(self, other: "HMSTime") -> bool:
        return self.total_seconds >= other.total_seconds

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, HMSTime):
            return NotImplemented
        return self.total_seconds != other.total_seconds

    @classmethod
    def from_seconds(cls, total_seconds: int) -> "HMSTime":
        instance = cls.__new__(cls)
        instance.total_seconds = total_seconds
        return instance

    @staticmethod
    def _parse_time_string(time_str: str) -> int:
        if not isinstance(time_str, str):
            raise NotTimeStringError(time_str)

        match = re.fullmatch(r"(-)?(\d+):(\d{1,2})(?::(\d{1,2}))?", time_str)
        if not match:
            raise InvalidTimeFormatError(time_str)
        neg, hh, mm, ss = match.groups()
        hh = int(hh)
        mm = int(mm)
        ss = int(ss) if ss is not None else 0

        total = hh * 3600 + mm * 60 + ss
        return -total if neg else total

    def to_seconds(self) -> int:
        return self.total_seconds

    def to_minutes(self) -> float:
        return self.total_seconds / 60

    def to_hours(self) -> float:
        return self.total_seconds / 3600

    def to_tuple(self) -> tuple[int, int, int]:
        total = abs(self.total_seconds)
        hh = total // 3600
        mm = (total % 3600) // 60
        ss = total % 60
        return (hh, mm, ss)

    def to_dict(self) -> dict:
        hh, mm, ss = self.to_tuple()
        return {"hh": hh, "mm": mm, "ss": ss}
