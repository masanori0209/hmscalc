"""Unit tests for the HMSTime class and related exceptions in hmscalc.hms_time."""

import pytest

from hmscalc.exceptions import InvalidTimeFormatError, NotTimeStringError
from hmscalc.hms_time import HMSTime


def test_addition() -> None:
    """Test addition of two HMSTime objects."""
    a = HMSTime("1:30:15")
    b = HMSTime("2:15:45")
    assert str(a + b) == "3:46:00"

def test_subtraction() -> None:
    """Test subtraction of two HMSTime objects."""
    a = HMSTime("5:00:00")
    b = HMSTime("2:30:00")
    assert str(a - b) == "2:30:00"

def test_negative_result() -> None:
    """Test subtraction resulting in a negative HMSTime."""
    a = HMSTime("1:00")
    b = HMSTime("2:00")
    assert str(a - b) == "-1:00:00"

def test_str_format() -> None:
    """Test string formatting of HMSTime objects."""
    assert str(HMSTime("2:03")) == "2:03:00"
    assert str(HMSTime("1:02:03")) == "1:02:03"

def test_comparisons() -> None:
    """Test comparison operators for HMSTime objects."""
    a = HMSTime("1:00:00")
    b = HMSTime("0:59:59")
    assert a > b
    assert b < a
    assert a != b
    assert a == HMSTime("1:00")
    assert a >= HMSTime("1:00")
    assert b <= a

def test_to_methods() -> None:
    """Test conversion methods of HMSTime.

    (to_seconds, to_tuple, to_dict, to_minutes, to_hours).

    """
    t = HMSTime("1:02:03")
    assert t.to_seconds() == 3723
    assert t.to_tuple() == (1, 2, 3)
    assert t.to_dict() == {"hh": 1, "mm": 2, "ss": 3}
    assert abs(t.to_minutes() - 62.05) < 0.01
    assert abs(t.to_hours() - 1.034) < 0.01

def test_invalid_format() -> None:
    """Test that an invalid time string raises InvalidTimeFormatError."""
    with pytest.raises(InvalidTimeFormatError):
        HMSTime("invalid")

def test_non_string_input() -> None:
    """Test that a non-string input raises NotTimeStringError."""
    with pytest.raises(NotTimeStringError):
        HMSTime(123)  # type: ignore[arg-type]