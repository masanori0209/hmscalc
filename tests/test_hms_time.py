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


def test_sum_multiple_times() -> None:
    """Test summing multiple HMSTime objects using the sum class method."""
    times = [HMSTime("1:30:15"), HMSTime("2:15:45"), HMSTime("0:45:30"), HMSTime("1:00:00")]
    result = HMSTime.sum(times)
    assert str(result) == "5:31:30"


def test_sum_empty_list() -> None:
    """Test summing an empty list returns zero time."""
    result = HMSTime.sum([])
    assert str(result) == "0:00:00"


def test_sum_single_time() -> None:
    """Test summing a single time returns that time."""
    times = [HMSTime("2:30:45")]
    result = HMSTime.sum(times)
    assert str(result) == "2:30:45"


def test_sum_with_negative_times() -> None:
    """Test summing times that include negative values."""
    times = [HMSTime("5:00:00"), HMSTime("-2:30:00"), HMSTime("1:15:30")]
    result = HMSTime.sum(times)
    assert str(result) == "3:45:30"


def test_sum_all_negative() -> None:
    """Test summing all negative times results in negative total."""
    times = [HMSTime("-1:00:00"), HMSTime("-0:30:00"), HMSTime("-0:15:30")]
    result = HMSTime.sum(times)
    assert str(result) == "-1:45:30"


def test_sum_mixed_formats() -> None:
    """Test summing times with different input formats (HH:MM and HH:MM:SS)."""
    times = [
        HMSTime("1:30"),  # HH:MM format
        HMSTime("2:15:45"),  # HH:MM:SS format
        HMSTime("0:45"),  # HH:MM format
        HMSTime("1:00:15"),  # HH:MM:SS format
    ]
    result = HMSTime.sum(times)
    assert str(result) == "5:31:00"


def test_sum_large_values() -> None:
    """Test summing times that result in large hour values."""
    times = [HMSTime("23:59:59"), HMSTime("1:00:01"), HMSTime("48:30:30")]
    result = HMSTime.sum(times)
    assert str(result) == "73:30:30"


def test_sum_type_error() -> None:
    """Test that sum raises TypeError when given non-HMSTime objects."""
    with pytest.raises(TypeError):
        HMSTime.sum([HMSTime("1:00:00"), "2:00:00"])  # type: ignore[list-item]


def test_sum_not_iterable() -> None:
    """Test that sum raises TypeError when given non-iterable input."""
    with pytest.raises(TypeError):
        HMSTime.sum(HMSTime("1:00:00"))  # type: ignore[arg-type]
