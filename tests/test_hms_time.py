"""Unit tests for the HMSTime class and related exceptions in hmscalc.hms_time."""

import datetime
import operator

import pytest

from hmscalc import HMSTime, InvalidTimeFormatError, NotTimeStringError


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


def test_repr() -> None:
    """Test repr of HMSTime objects."""
    assert repr(HMSTime("1:02:03")) == "HMSTime('1:02:03')"


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
    assert t.to_dict() == {"hh": 1, "mm": 2, "ss": 3, "negative": False}
    assert abs(t.to_minutes() - 62.05) < 0.01
    assert abs(t.to_hours() - 1.034) < 0.01


def test_negative_to_methods() -> None:
    """Test conversion methods preserve sign information for negative values."""
    t = HMSTime("-1:00:00")
    assert t.to_seconds() == -3600
    assert t.is_negative is True
    assert t.to_tuple() == (1, 0, 0)
    assert t.to_dict() == {"hh": 1, "mm": 0, "ss": 0, "negative": True}


def test_invalid_format() -> None:
    """Test that an invalid time string raises InvalidTimeFormatError."""
    with pytest.raises(InvalidTimeFormatError):
        HMSTime("invalid")


def test_invalid_minute_second_range() -> None:
    """Test that minute or second values >= 60 raise InvalidTimeFormatError."""
    with pytest.raises(InvalidTimeFormatError):
        HMSTime("1:99:00")
    with pytest.raises(InvalidTimeFormatError):
        HMSTime("1:00:60")
    with pytest.raises(InvalidTimeFormatError):
        HMSTime("0:60:00")


def test_empty_string_raises() -> None:
    """Test that an empty string raises InvalidTimeFormatError."""
    with pytest.raises(InvalidTimeFormatError):
        HMSTime("")


def test_non_string_input() -> None:
    """Test that a non-string input raises NotTimeStringError."""
    with pytest.raises(NotTimeStringError):
        HMSTime(123)  # type: ignore[arg-type]


def test_arithmetic_type_error() -> None:
    """Test that arithmetic with non-HMSTime raises TypeError."""
    t = HMSTime("1:00:00")
    with pytest.raises(TypeError):
        _ = t + "2:00:00"
    with pytest.raises(TypeError):
        _ = t - "2:00:00"


def test_comparison_type_error() -> None:
    """Test that comparison with non-HMSTime raises TypeError."""
    t = HMSTime("1:00:00")
    with pytest.raises(TypeError):
        operator.lt(t, None)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        operator.gt(t, "1:00:00")


def test_from_seconds() -> None:
    """Test creating HMSTime from seconds directly."""
    t = HMSTime.from_seconds(3661)
    assert str(t) == "1:01:01"
    assert t.to_seconds() == 3661


def test_from_timedelta() -> None:
    """Test creating HMSTime from datetime.timedelta."""
    delta = datetime.timedelta(hours=1, minutes=30, seconds=15)
    t = HMSTime.from_timedelta(delta)
    assert str(t) == "1:30:15"
    assert t.to_timedelta() == delta


def test_package_import() -> None:
    """Test that HMSTime can be imported from the package root."""
    from hmscalc import HMSTime as ImportedHMSTime

    assert ImportedHMSTime("1:00:00").to_seconds() == 3600


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


def test_average() -> None:
    """Test average of multiple HMSTime objects."""
    times = [HMSTime("1:00:00"), HMSTime("3:00:00")]
    assert str(HMSTime.average(times)) == "2:00:00"


def test_average_rounds_to_nearest_second() -> None:
    """Test that average rounds to the nearest second."""
    times = [HMSTime("0:00:01"), HMSTime("0:00:02")]
    assert str(HMSTime.average(times)) == "0:00:02"


def test_average_empty_raises() -> None:
    """Test that average of empty iterable raises ValueError."""
    with pytest.raises(ValueError):
        HMSTime.average([])


def test_min_max() -> None:
    """Test min and max class methods."""
    times = [HMSTime("1:00:00"), HMSTime("3:00:00"), HMSTime("0:30:00")]
    assert str(HMSTime.min(times)) == "0:30:00"
    assert str(HMSTime.max(times)) == "3:00:00"


def test_min_max_empty_raises() -> None:
    """Test that min/max of empty iterable raises ValueError."""
    with pytest.raises(ValueError):
        HMSTime.min([])
    with pytest.raises(ValueError):
        HMSTime.max([])


def test_whitespace_trimmed() -> None:
    """Test that surrounding whitespace in input is ignored."""
    assert str(HMSTime(" 1:30:15 ")) == "1:30:15"
    assert str(HMSTime("\t2:00:00\n")) == "2:00:00"


def test_scalar_multiply() -> None:
    """Test scalar multiplication of HMSTime."""
    t = HMSTime("1:00:00")
    assert str(t * 2) == "2:00:00"
    assert str(3 * t) == "3:00:00"
    assert str(t * 0.5) == "0:30:00"


def test_scalar_divide() -> None:
    """Test scalar division of HMSTime."""
    t = HMSTime("1:30:00")
    assert str(t / 2) == "0:45:00"
    assert str(t / 4) == "0:22:30"


def test_scalar_divide_by_zero() -> None:
    """Test that division by zero raises ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError):
        HMSTime("1:00:00") / 0


def test_scalar_type_error() -> None:
    """Test that scalar ops with invalid types raise TypeError."""
    t = HMSTime("1:00:00")
    with pytest.raises(TypeError):
        _ = t * "2"
    with pytest.raises(TypeError):
        _ = t / "2"


def test_hashable() -> None:
    """Test that HMSTime can be used in sets and as dict keys."""
    a = HMSTime("1:00:00")
    b = HMSTime("2:00:00")
    assert len({a, b, a}) == 2
    d = {a: "one", b: "two"}
    assert d[a] == "one"
