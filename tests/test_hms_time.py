import pytest
from hmscalc.hms_time import HMSTime
from hmscalc.exceptions import (
    InvalidTimeFormatError,
    NotTimeStringError,
)

def test_addition():
    a = HMSTime("1:30:15")
    b = HMSTime("2:15:45")
    assert str(a + b) == "3:46:00"

def test_subtraction():
    a = HMSTime("5:00:00")
    b = HMSTime("2:30:00")
    assert str(a - b) == "2:30:00"

def test_negative_result():
    a = HMSTime("1:00")
    b = HMSTime("2:00")
    assert str(a - b) == "-1:00:00"

def test_str_format():
    assert str(HMSTime("2:03")) == "2:03:00"
    assert str(HMSTime("1:02:03")) == "1:02:03"

def test_comparisons():
    a = HMSTime("1:00:00")
    b = HMSTime("0:59:59")
    assert a > b
    assert b < a
    assert a != b
    assert a == HMSTime("1:00")
    assert a >= HMSTime("1:00")
    assert b <= a

def test_to_methods():
    t = HMSTime("1:02:03")
    assert t.to_seconds() == 3723
    assert t.to_tuple() == (1, 2, 3)
    assert t.to_dict() == {"hh": 1, "mm": 2, "ss": 3}
    assert abs(t.to_minutes() - 62.05) < 0.01
    assert abs(t.to_hours() - 1.034) < 0.01

def test_invalid_format():
    with pytest.raises(InvalidTimeFormatError):
        HMSTime("invalid")

def test_non_string_input():
    with pytest.raises(NotTimeStringError):
        HMSTime(123)